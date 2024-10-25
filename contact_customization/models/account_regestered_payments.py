# -*- coding: utf-8 -*-

from odoo import models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def action_create_payments(self):
        """Method to update the loyalty points based on the current account"""
        res = super().action_create_payments()
        move_id = self.env["account.move"].search(
            [("name", "=", self.communication)]
        )
        if move_id:
            partner_extended_id = self.env["res.partner.extended"].search(
                [("partner_id", "=", move_id.partner_id.id)]
            )
            if partner_extended_id and partner_extended_id.loyalty_points > 0:
                partner_extended_id.loyalty_points += 1
        return res
