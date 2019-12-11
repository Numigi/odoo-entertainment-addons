# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ArtistMember(models.Model):

    _name = 'artist.member'
    _description = 'Artist Member'
    _order = 'sequence'

    sequence = fields.Integer()
    artist_id = fields.Many2one(
        'artist', 'Artist', index=True, required=True,
    )
    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True,
    )
    role_id = fields.Many2one('artist.role', ondelete='restrict')
    date_from = fields.Date()
    date_to = fields.Date()
    active = fields.Boolean(default=True)
