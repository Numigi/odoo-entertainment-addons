# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class Recording(models.Model):

    _inherit = 'recording'

    product_template_ids = fields.One2many(
        'product.template',
        'recording_id',
    )

    related_product_count = fields.Integer(
        compute='_compute_related_product_count'
    )

    def _compute_related_product_count(self):
        for rec in self:
            rec.related_product_count = len(rec.product_template_ids)

    @api.multi
    def write(self, vals):
        super().write(vals)
        if 'artist_id' in vals:
            for product in self.mapped('product_template_ids'):
                product._propagate_artist_from_recording()
        return True
