# -*- coding: utf-8 -*-

from odoo import models, fields


class ResRegion(models.Model):
    _name = "res.region"
    _rec_name = "region_name"

    region_name = fields.Char(string="Region Name")
