# -*- coding: utf-8 -*-

from odoo import models


class SaleOrderExtended(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """Method to update the loyalty points for the partner based on the
        order"""
        res = super().action_confirm()
        partner_extended_id = self.env["res.partner.extended"].search(
            [("partner_id", "=", self.partner_id.id)]
        )
        if partner_extended_id and partner_extended_id.loyalty_points > 0:
            partner_extended_id.loyalty_points += 1
        return res
