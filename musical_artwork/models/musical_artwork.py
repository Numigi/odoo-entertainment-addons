# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MusicalArtworkLanguage(models.Model):
    _name = 'musical.artwork.language'
    _description = 'Musical Artwork Language'
    _order = 'sequence'

    sequence = fields.Integer()
    language_id = fields.Many2one("recording.language", required=True)
    percentage = fields.Integer("%", required=True)
    musical_artwork_id = fields.Many2one(
        'musical.artwork', ondelete='cascade', required=True, index=True,
    )

    _sql_constraints = [
        (
            'language_per_musical_artwork',
            'unique (language_id,musical_artwork_id)',
            'A language can be selected only once for a given musical artwork.'
        ),
    ]


class MusicalArtwork(models.Model):
    _name = 'musical.artwork'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Musical Artwork'
    _rec_name = 'title'

    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda s: s.env.user.company_id,
    )
    title = fields.Char(
        required=True,
        track_visibility="onchange",
    )
    active = fields.Boolean(
        default=True,
        track_visibility="onchange",
    )
    iswc = fields.Char(
        'ISWC',
        track_visibility="onchange",
    )
    catalogue_reference = fields.Char(
        track_visibility="onchange",
    )
    musical_catalog_reference_ids = fields.One2many(
        'musical.catalog.reference',
        'musical_artwork_id',
        'External Catalog References',
    )

    language_ids = fields.One2many(
        'musical.artwork.language',
        'musical_artwork_id',
        string='Languages',
        copy=True,
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


class MusicalArtworkWithDistributionKeys(models.Model):

    _inherit = 'musical.artwork'

    distribution_key_count = fields.Integer(compute='_compute_distribution_key_count')

    def _compute_distribution_key_count(self):
        for artwork in self:
            artwork.distribution_key_count = self.env['musical.artwork.distribution'].search([
                ('musical_artwork_id', '=', artwork.id),
            ], count=True)
