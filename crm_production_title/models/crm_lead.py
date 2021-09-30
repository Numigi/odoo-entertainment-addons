# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Lead(models.Model):
    _inherit = "crm.lead"

    production_title_id = fields.Many2one("production.title", ondelete="restrict")
    production_type_id = fields.Many2one(
        "production.type", compute="_compute_production_type_id", readonly=True
    )

    @api.depends("production_title_id")
    def _compute_production_type_id(self):
        for rec in self:
            rec.production_type_id = rec.production_title_id.production_type_id
