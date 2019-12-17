# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ExternalCatalogueReference(models.Model):
    _name = 'musical.artwork.external.catalogue.reference'
    _description = 'Musical Artwork External Catalogue Reference'
    _rec_name = 'code'

    code = fields.Char(required=True)
    active = fields.Boolean(default=True)
    musical_artwork_id = fields.Many2one('musical.artwork')


class MusicalArtworkLanguage(models.Model):
    _name = 'musical.artwork.language'
    _description = 'Musical Artwork Language'

    language_id = fields.Many2one("recording.language", required=True)
    percentage = fields.Integer("%", required=True)
    musical_artwork_id = fields.Many2one('musical.artwork')

    _sql_constraints = [
        (
            'language_per_musical_artwork',
            'unique (language_id,musical_artwork_id)',
            'A language can be selected only once for a given musical artwork.'
        ),
    ]


class RecordingMusicalArtwork(models.Model):
    _inherit = 'recording'

    musical_artwork_id = fields.Many2one('musical.artwork')


class MusicalArtwork(models.Model):
    _name = 'musical.artwork'
    _description = 'Musical Artwork'
    _rec_name = 'title'

    title = fields.Char(required=True)
    active = fields.Boolean(default=True)
    iswc = fields.Char('ISWC', required=True)
    recording_ids = fields.One2many('recording', 'musical_artwork_id', string='Recordings')
    catalogue_reference = fields.Char(required=True)
    external_catalogue_reference_ids = fields.One2many(
        'musical.artwork.external.catalogue.reference',
        'musical_artwork_id',
        string='External Catalogue References',
    )
    language_ids = fields.One2many(
        'musical.artwork.language',
        'musical_artwork_id',
        string='Languages'
    )
    lyrics = fields.Text()

    _sql_constraints = [
        (
            'catalogue_reference', 'unique (catalogue_reference)',
            'The catalogue reference has to be unique.'
        ),
        (
            'iswc_unique',
            'unique (iswc)',
            'A work already has this ISWC. A ISWC can only be linked to a single work.'
        ),
    ]

    related_recording_count = fields.Integer(compute='_compute_related_recording_count')

    def _compute_related_recording_count(self):
        for rec in self:
            rec.related_recording_count = self.env['recording'].search(
                [('musical_artwork_id', '=', rec.id)],
                count=True
            )
