# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MusicalCatalog(models.Model):

    _name = 'musical.catalog'
    _description = 'External Catalogs'
    _order = 'sequence'

    sequence = fields.Integer()
    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    reference_unique = fields.Boolean(
        help='If this box is checked, the Catalog Reference ("Code" field) on '
        'Recordings must be unique.'
    )
