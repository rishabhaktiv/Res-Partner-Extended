# -*- coding: utf-8 -*-

{
    "name": "Contact Customization",
    "version": "17.0.0.0.1",
    "category": "Sale/Invoice",
    "summary": "Contact Customization",
    "description": """
        Contact Customization
        """,
    "author": "Aktiv Software",
    "company": "Aktiv Software",
    "website": "https://www.aktivsoftware.com",
    "depends": [
        "sale_management",
        "account",
        "auth_signup",
        "mail",
        "contacts",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/res_partner_extended_security.xml",
        "data/ir_cron.xml",
        "data/email_temaplate.xml",
        "views/res_partner_extended_views.xml",
        "views/res_partner_extended_menus.xml",
        "views/res_region_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "LGPL-3",
}
