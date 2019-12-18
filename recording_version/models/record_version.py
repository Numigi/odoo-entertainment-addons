# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RecordVersion(models.Model):

    _name = 'record.version'
    _description = 'Version'

    name = fields.Char(string='Name', required=1, translate=True)
    active = fields.Boolean(string='Active', default=True)
