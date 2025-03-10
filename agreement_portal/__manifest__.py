# Copyright (C) 2022 Rafnix Guzman rafnixg
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Agreement Portal",
    "summary": "Show a portal for Agreement",
    "version": "14.0.1.0.2",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/contract",
    "category": "Agreement",
    "author": "Odoo Community Association (OCA), Rafnixg",
    "depends": ["base", "portal", "website", "agreement"],
    "data": [
        "security/ir.model.access.csv",
        "security/agreement_security.xml",
        "views/agreement_portal_templates.xml",
    ],
    "demo": [],
}
