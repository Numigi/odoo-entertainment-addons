# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductionTitle(models.Model):
    _name = "production.title"
    _description = "Production Title"
    _order = "name"

    name = fields.Text(translate=True, required=True)
    type_id = fields.Many2one(
        "production.type", ondelete="restrict", string="Production Type"
    )
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)
