# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductProduct(models.Model):

    _inherit = 'product.product'

    musical_relation = fields.Selection(
        related='product_tmpl_id.musical_relation',
    )
    recording_id = fields.Many2one(
        related='product_tmpl_id.recording_id',
    )
    artist_id = fields.Many2one(
        related='product_tmpl_id.artist_id',
    )

    recording_release_date = fields.Date(
        related='product_tmpl_id.recording_release_date',
    )
    sale_date = fields.Date(
        related='product_tmpl_id.sale_date',
    )
    commercialization_date = fields.Date(
        related='product_tmpl_id.commercialization_date',
    )

    catalogue_reference = fields.Char(
        related='product_tmpl_id.catalogue_reference',
    )

    musical_catalog_reference_ids = fields.One2many(
        related='product_tmpl_id.musical_catalog_reference_ids',
    )
