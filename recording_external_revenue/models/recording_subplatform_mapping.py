# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class RecordingSubplatformMapping(models.Model):
    _name = "recording.subplatform.mapping"
    _description = "Recording Subplatform Mapping"
    _order = "label"
    _rec_name = "label"

    label = fields.Char(required=True, unique=True, string="Label")
    platform_id = fields.Many2one(
        "recording.platform", ondelete="restrict", required=True
    )
    subplatform_id = fields.Many2one(
        "recording.subplatform",
        ondelete="restrict",
        required=True,
        domain="[('platform_id', '=', platform_id)]",
    )

    @api.onchange("platform_id")
    def _empty_subplatform_if_not_match_platform(self):
        if self.platform_id != self.subplatform_id.platform_id:
            self.subplatform_id = None

    _sql_constraints = [
        (
            "unique_label_and_platform",
            "unique (label, platform_id)",
            "Only one subplatform can be mapped per label and platform.",
        )
    ]

    @api.model
    def map(self, platform, label):
        subplatform = self.search(
            [("platform_id", "=", platform.id), ("label", "=", label)]
        ).subplatform_id
        if not subplatform:
            raise ValidationError(_(
                "No subplatform found for the label {}"
            ).format(label))
        return subplatform
