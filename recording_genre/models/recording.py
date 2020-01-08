# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Recording(models.Model):

    _inherit = 'recording'

    genre_id = fields.Many2one(
        'recording.genre',
        ondelete='restrict',
    )

    explicit_content = fields.Boolean()
