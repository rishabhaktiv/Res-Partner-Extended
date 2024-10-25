# -*- coding: utf-8 -*-

from odoo import models


class ActionMoveExtended(models.Model):
    _inherit = "account.move"

    def button_cancel(self):
        """Method to update the loyalty points of the partner"""
        res = super().button_cancel()
        partner_extended_id = self.env["res.partner.extended"].search(
            [("partner_id", "=", self.partner_id.id)]
        )
        if partner_extended_id and partner_extended_id.loyalty_points > 0:
            partner_extended_id.loyalty_points -= 1
        return res
