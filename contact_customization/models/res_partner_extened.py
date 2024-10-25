import re
from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError


class ResPartnerExtended(models.Model):
    _name = "res.partner.extended"
    _inherit = ["res.partner"]

    active = fields.Boolean(default=True)
    channel_ids = fields.Many2many(
        "discuss.channel",
        "discuss_channel_member_extended",
        "res_partner_extended_id",
        "extended_channel_id",
        string="Extended Channels",
        copy=False,
        ondelete="cascade",
    )
    starred_message_ids = fields.Many2many(
        "mail.message", "mail_message_res_partner_starred_extended_rel"
    )

    partner_id = fields.Many2one("res.partner", string="Partner")
    secondary_email = fields.Char(string="Secondary Email")
    social_facebook = fields.Char(string="Social Facebook")
    social_twitter = fields.Char(string="Social Twitter")
    social_linkedin = fields.Char(string="Social LinkedIn")
    date_first_contact = fields.Date(
        string="Date First Contact", default=fields.Date.today()
    )
    loyalty_points = fields.Integer(string="Loyalty Points", default=0)
    preferred_language_id = fields.Many2one(
        "res.lang",
        string="Preferred Language",
        default=lambda self: self.env["res.lang"].search(
            [("code", "=", self.env.user.lang)], limit=1
        ),
    )
    is_vip = fields.Boolean(string="Is VIP", default=False)
    birthday_reminder = fields.Date(string="Birthday Reminder", default=False)
    region = fields.Many2one("res.region", string="Region")
    partner_rating = fields.Integer(string="Partner Rating")

    @api.constrains("secondary_email")
    def check_email(self):
        """Method to check the email address"""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, self.secondary_email):
            raise ValidationError("Email pattern is not a valid")

    def unlink(self):
        """Prevent deletion of records if the partner is marked as VIP"""
        if self.is_vip:
            raise ValidationError("Cannot delete VIP Partner")
        else:
            return super(ResPartnerExtended, self).unlink()

    @api.depends("is_company", "parent_id.commercial_partner_id")
    def _compute_commercial_partner(self):
        """
            Compute the commercial partner for the current partner record.
            The commercial partner is the company if the partner is a company,
            or it is inherited from the parent company's commercial partner.
            """
        for partner in self:
            if partner.is_company or not partner.parent_id:
                partner.partner_id.commercial_partner_id = partner.partner_id
            else:
                partner.commercial_partner_id = (
                    (partner.parent_id.commercial_partner_id.id)
                    if partner._origin
                    else False
                )

    #
    @api.depends("user_ids.share", "user_ids.active")
    def _compute_partner_share(self):
        """
            Compute the 'partner_share' field for partners.
            This field indicates
            whether the partner is shared between multiple users.
            It depends on whether the partner's associated users have the
            'share' or 'active' flags.
            """
        super_partner = self.env["res.users"].browse(SUPERUSER_ID).partner_id
        if super_partner in self.partner_id:
            super_partner.partner_share = False
        for partner in self.partner_id - super_partner:
            partner.partner_share = not partner.user_ids or not any(
                not user.share for user in partner.user_ids
            )

    def init(self):
        """Pass"""
        pass

    def action_send_email(self):
        """Method to send an email"""
        mail_template = self.env.ref(
            "contact_customization" ".mail_template_birthday_reminder"
        )
        mail_template.send_mail(self.id, force_send=True)

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        """Hide the fields based on the user group."""
        arch, view = super(ResPartnerExtended, self)._get_view(
            view_id, view_type, **options
        )
        if self.env.user and not self.env.user.has_group(
            "contact_customization.group_vip_manager"
        ):
            field_list = [
                "is_vip",
                "loyalty_points",
                "social_facebook",
                "social_twitter",
                "social_linkedin",
            ]
            for field in field_list:
                # Correct the XPath query to use string interpolation properly
                for node in arch.xpath(f"//field[@name='{field}']"):
                    node.set("invisible", "1")
        return arch, view
