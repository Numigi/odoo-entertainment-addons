# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RecordingExternalCatalogReference(models.Model):

    _name = 'recording.external.catalog.reference'
    _description = 'External Catalog Reference for Recordings'
    _order = 'sequence'

    recording_id = fields.Many2one(
        'recording',
        ondelete='cascade',
        required=True,
    )
    sequence = fields.Integer()
    code = fields.Char(required=True)
