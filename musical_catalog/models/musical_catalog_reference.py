# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MusicalCatalogReference(models.Model):

    _name = 'musical.catalog.reference'
    _description = 'External Catalog References'
    _order = 'sequence'

    sequence = fields.Integer()
    catalog_id = fields.Many2one('musical.catalog', required=True)
    code = fields.Char(required=True)
