# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

decimal_precision = (12, 2)


class MusicalArtworkDistributionLine(models.Model):
    _name = 'musical.artwork.distribution.line'
    _description = 'Musical Artwork Distribution Line'

    active = fields.Boolean(default=True)
    partner_id = fields.Many2one('res.partner')
    role_id = fields.Many2one('musical.artwork.role')
    percentage = fields.Float('%', digits=decimal_precision)
    is_managed = fields.Boolean('Managed', default=True)
    distribution_id = fields.Many2one('musical.artwork.distribution')


class MusicalArtworkDistribution(models.Model):
    _name = 'musical.artwork.distribution'
    _description = 'Musical Artwork Distribution'

    active = fields.Boolean(default=True)

    musical_artwork_id = fields.Many2one('musical.artwork')
    country_group_id = fields.Many2one('res.country.group')
    line_ids = fields.One2many('musical.artwork.distribution.line', 'distribution_id')

    total_distribution_key = fields.Float(
        digits=decimal_precision,
        readonly=True,
        compute='_compute_total_distribution_key'
    )

    @api.depends('line_ids')
    def _compute_total_distribution_key(self):
        for record in self:
            record.total_distribution_key = sum(record.line_ids.mapped('percentage'))
