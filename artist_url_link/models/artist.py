# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Artist(models.Model):

    _inherit = 'artist'

    url_link_ids = fields.One2many(
        'artist.url.link',
        'artist_id',
        'URL Links',
    )
