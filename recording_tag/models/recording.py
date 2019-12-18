# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Recording(models.Model):

    _inherit = 'recording'

    tag_ids = fields.Many2many(
        'recording.tag',
        'recording_tag_rel',
        'recording_id',
        'tag_id',
        string='Tags',
        ondelete='restrict',
    )
