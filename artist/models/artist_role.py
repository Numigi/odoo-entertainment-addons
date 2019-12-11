# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ArtistRole(models.Model):

    _name = 'artist.role'
    _description = 'Artist Role'

    sequence = fields.Integer()
    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
