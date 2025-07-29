# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Recording(models.Model):

    _inherit = 'recording'

    sound_copyright = fields.Char()
    copyright = fields.Char()

    contributor_ids = fields.One2many(
        'recording.contributor',
        'recording_id',
        'Contributors',
    )
