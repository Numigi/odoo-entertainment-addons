# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class RecordingPlatformMapping(models.Model):
    _name = "recording.platform.mapping"
    _description = "Recording Platform Mapping"
    _order = 'label'
    _rec_name = 'label'

    label = fields.Char(required=True, unique=True, string="Label")
    platform_id = fields.Many2one(
        "recording.platform", ondelete="restrict", required=True,
    )

    _sql_constraints = [
        ('unique_label',
         'unique (label)',
         'Only one platform can be mapped per label.')
    ]

    @api.model
    def map(self, label):
        platform = self.search([('label', '=', label)]).platform_id
        if not platform:
            raise ValidationError(_(
                "No platform found for the label {}"
            ).format(label))
        return platform
