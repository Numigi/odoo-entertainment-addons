# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class DiffuserRole(models.Model):

    _name = "diffuser.role"
    _description = "Diffuser Role"

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
