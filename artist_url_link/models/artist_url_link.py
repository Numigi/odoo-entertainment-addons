# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ArtistUrlLink(models.Model):

    _name = 'artist.url.link'
    _description = 'Artist URL Link'

    artist_id = fields.Many2one('artist', 'Artist', required=True)
    type_id = fields.Many2one('url.link.type', 'Link Type', required=True)
    url = fields.Char(string='URL', required=True)
    notes = fields.Text()
