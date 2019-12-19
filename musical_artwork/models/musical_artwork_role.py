# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MusicalArtworkRole(models.Model):
    _name = 'musical.artwork.role'
    _description = 'Musical Artwork Role'
    _rec_name = "name"
    _order = 'sequence'

    sequence = fields.Integer()
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    code = fields.Char(required=True)
