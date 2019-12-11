# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Recording(models.Model):

    _inherit = 'recording'

    lyrics = fields.Text()
    lyrics_language_ids = fields.One2many(
        'recording.language.rate',
        'recording_id',
        'Languages',
    )
