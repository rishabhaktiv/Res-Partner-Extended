# -*- coding: utf-8 -*-

from odoo import models


class SaleOrderCancel(models.TransientModel):
    _inherit = "sale.order.cancel"

    def action_cancel(self):
        """Method to update the loyalty points for the partner based on the
        order cancellation"""
        res = super().action_cancel()
        partner_extended_id = self.env["res.partner.extended"].search(
            [("partner_id", "=", self.order_id.partner_id.id)]
        )
        if partner_extended_id and partner_extended_id.loyalty_points > 0:
            partner_extended_id.loyalty_points -= 1
        return res

    def action_send_mail_and_cancel(self):
        """Method to update the loyalty points for the partner based on the
                order cancellation and send the mail"""
        res = super().action_send_mail_and_cancel()
        partner_extended_id = self.env["res.partner.extended"].search(
            [("partner_id", "=", self.order_id.partner_id.id)]
        )
        if partner_extended_id and partner_extended_id.loyalty_points > 0:
            partner_extended_id.loyalty_points -= 1
        return res
