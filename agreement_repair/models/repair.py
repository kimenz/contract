# Copyright (C) 2021 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class Repair(models.Model):
    _inherit = "repair.order"

    agreement_id = fields.Many2one("agreement", "Agreement")
    serviceprofile_id = fields.Many2one("agreement.serviceprofile", "Service Profile")
    partner_agreement_id = fields.Many2one(
        "res.partner", "Agreement Partner", compute="_compute_partner_agreement_id",
    )

    def _get_partner(self, partner_id):
        while partner_id.parent_id:
            partner_id = partner_id.parent_id
        return partner_id

    def _compute_partner_agreement_id(self):
        for rec in self:
            rec.partner_agreement_id = rec._get_partner(rec.partner_id)
        