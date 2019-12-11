# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RecordingCompany(models.Model):

    _name = 'recording.company'
    _description = 'Record Company'
    _order = 'sequence'

    sequence = fields.Integer()
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
