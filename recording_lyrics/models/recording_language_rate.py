# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RecordLanguageRate(models.Model):

    _name = 'recording.language.rate'
    _description = 'Language Rate (Recording)'

    sequence = fields.Integer()
    recording_id = fields.Many2one(
        'recording', ondelete='cascade', required=True, index=True,
    )
    language_id = fields.Many2one(
        'recording.language', ondelete='restrict', required=True,
    )
    percentage = fields.Integer("%", required=True)
