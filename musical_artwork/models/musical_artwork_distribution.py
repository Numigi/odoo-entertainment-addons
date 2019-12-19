# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare

decimal_precision = (12, 2)


class MusicalArtworkDistributionLine(models.Model):
    _name = 'musical.artwork.distribution.line'
    _description = 'Musical Artwork Distribution Line'
    _order = 'sequence'

    sequence = fields.Integer()
    partner_id = fields.Many2one('res.partner', ondelete='restrict')
    role_id = fields.Many2one('musical.artwork.role', ondelete='restrict')
    percentage = fields.Float('%', digits=decimal_precision)
    is_managed = fields.Boolean('Managed', default=True)
    distribution_id = fields.Many2one('musical.artwork.distribution', index=True)


class MusicalArtworkDistribution(models.Model):
    _name = 'musical.artwork.distribution'
    _description = 'Musical Artwork Distribution'

    active = fields.Boolean(default=True)

    name = fields.Char(readonly=True, string="Reference")

    musical_artwork_id = fields.Many2one(
        'musical.artwork', required=True, ondelete='restrict', index=True,
    )
    country_group_id = fields.Many2one(
        'res.country.group', ondelete='restrict',
    )
    line_ids = fields.One2many(
        'musical.artwork.distribution.line', 'distribution_id',
        copy=True,
    )

    total_distribution_key = fields.Float(
        "Distribution Key Total",
        digits=decimal_precision,
        readonly=True,
        store=True,
        compute='_compute_total_distribution_key',
    )

    @api.depends('line_ids.percentage')
    def _compute_total_distribution_key(self):
        for record in self:
            record.total_distribution_key = sum(record.line_ids.mapped('percentage'))

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.name = self.env['ir.sequence'].next_by_code(self._name)
        return record

    @api.constrains('total_distribution_key')
    def _check_total_distribution_key(self):
        for record in self:
            if float_compare(record.total_distribution_key, 100, 2):
                raise ValidationError(_(
                    "The sum of the distribution key lines is not equal to 100. "
                    "The distribution key must have a total of 100%."
                ))
