# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Recording(models.Model):

    _inherit = 'recording'

    url_link_ids = fields.One2many(
        'recording.url.link',
        'recording_id',
        'URL Links',
    )
