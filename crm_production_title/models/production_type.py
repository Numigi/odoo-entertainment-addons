# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductionType(models.Model):
    _name = "production.type"
    _description = "Production Type"
    _order = "name"

    name = fields.Text(translate=True, required=True)
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)
