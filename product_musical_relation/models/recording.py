# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Recording(models.Model):

    _inherit = 'recording'

    related_product_count = fields.Integer(
        compute='_compute_related_product_count'
    )

    def _compute_related_product_count(self):
        for rec in self:
            rec.related_product_count = self.env['product.template'].search([
                ('recording_id', '=', rec.id),
            ], count=True)
