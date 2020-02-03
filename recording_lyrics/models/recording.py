# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class Recording(models.Model):

    _inherit = 'recording'

    language_id = fields.Many2one('recording.language', ondelete='restrict')

    lyrics = fields.Text()
    language_ids = fields.One2many(
        'recording.language.rate',
        'recording_id',
        'Languages',
    )

    @api.model
    def create(self, vals):
        record = super().create(vals)

        if record.sound_recording_id:
            record._propagate_lyrics_from_sound_recording()
            record._propagate_language_percentages_from_sound_recording()

        return record

    @api.multi
    def write(self, vals):
        super().write(vals)

        if 'lyrics' in vals:
            for record in self:
                record._propagate_lyrics_to_video_recordings()

        if 'language_ids' in vals:
            for record in self:
                record._propagate_language_percentages_to_video_recordings()

        if vals.get('sound_recording_id'):
            for record in self:
                record._propagate_lyrics_from_sound_recording()
                record._propagate_language_percentages_from_sound_recording()

        return True

    def _propagate_lyrics_to_video_recordings(self):
        for video in self.video_recording_ids:
            video._propagate_lyrics_from_sound_recording()

    def _propagate_language_percentages_to_video_recordings(self):
        for video in self.video_recording_ids:
            video._propagate_language_percentages_from_sound_recording()

    @api.onchange('sound_recording_id')
    def _propagate_lyrics_from_sound_recording(self):
        self.lyrics = self.sound_recording_id.lyrics

    @api.onchange('sound_recording_id')
    def _propagate_language_percentages_from_sound_recording(self):
        percentages = self.env['recording.language.rate']

        for item in self.sound_recording_id.language_ids:
            percentages |= percentages.new({
                'sequence': item.sequence,
                'language_id': item.language_id.id,
                'percentage': item.percentage,
            })

        self.language_ids = percentages
