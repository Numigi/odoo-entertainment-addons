# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RecordLanguage(models.Model):

    _name = 'recording.language'
    _description = 'Language'
    _order = 'sequence'

    sequence = fields.Integer()
    name = fields.Char(string='Name', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    active = fields.Boolean(default=True)
