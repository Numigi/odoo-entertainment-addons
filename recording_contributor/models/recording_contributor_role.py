# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RecordingContributorRole(models.Model):

    _name = 'recording.contributor.role'
    _description = 'Recording Contributor Role'
    _order = 'sequence'

    sequence = fields.Integer()
    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
