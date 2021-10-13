# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductionType(models.Model):
    _name = "production.type"
    _description = "Production Type"
    _order = "name"

    name = fields.Text(translate=True, required=True)
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)
