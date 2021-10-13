# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Lead(models.Model):
    _inherit = "crm.lead"

    production_title_id = fields.Many2one("production.title", ondelete="restrict")
    production_type_id = fields.Many2one(
        "production.type",
        related="production_title_id.type_id",
        readonly=True,
        store=True,
        string="Production Type",
    )
