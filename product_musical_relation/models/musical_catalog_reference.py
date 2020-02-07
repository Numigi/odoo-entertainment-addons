# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MusicalCatalogReference(models.Model):

    _inherit = 'musical.catalog.reference'

    product_template_id = fields.Many2one('product.template', ondelete='cascade')
