# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ArtistTag(models.Model):

    _name = 'artist.tag'
    _description = 'Artist Tag'

    sequence = fields.Integer()
    name = fields.Char(required=True, translate=True)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(default=True)
