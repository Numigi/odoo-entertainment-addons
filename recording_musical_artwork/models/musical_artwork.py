# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MusicalArtwork(models.Model):

    _inherit = 'musical.artwork'

    recording_ids = fields.One2many('recording', 'musical_artwork_id', string='Recordings')
    related_recording_count = fields.Integer(compute='_compute_related_recording_count')

    def _compute_related_recording_count(self):
        for rec in self:
            rec.related_recording_count = self.env['recording'].search(
                [('musical_artwork_id', '=', rec.id)],
                count=True
            )
