# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ShowAppearanceType(models.Model):
    _name = "show.appearance.type"
    _description = "Show Appearance Type"

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
