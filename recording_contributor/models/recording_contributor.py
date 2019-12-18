# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RecordingContributor(models.Model):

    _name = 'recording.contributor'
    _description = 'Recording Contributor'
    _order = 'sequence'

    sequence = fields.Integer()
    recording_id = fields.Many2one(
        'recording',
        'Recording',
        required=True,
        index=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        'Partner',
        required=True,
    )
    role_id = fields.Many2one(
        'recording.contributor.role',
        'Role',
        required=True,
    )
    date = fields.Date()
