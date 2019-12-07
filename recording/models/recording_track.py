# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RecordingTrack(models.Model):

    _name = 'recording.track'
    _description = 'Recording Track'
    _order = 'sequence'

    sequence = fields.Integer()
    recording_group_id = fields.Many2one(
        'recording', 'Recording Group', index=True,
        required=True,
    )
    volume = fields.Char()
    track = fields.Char()
    recording_id = fields.Many2one(
        'recording', 'Recording', required=True,
    )
