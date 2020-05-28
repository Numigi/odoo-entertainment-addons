# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class RecordingCountryStateMapping(models.Model):
    _name = "recording.country.state.mapping"
    _description = "Recording Country State Mapping"
    _order = "label"
    _rec_name = "label"

    label = fields.Char(required=True, unique=True, string="Label")
    country_id = fields.Many2one("res.country", ondelete="restrict", required=True)
    state_id = fields.Many2one(
        "res.country.state", ondelete="restrict", required=True,
        domain="[('country_id', '=', country_id)]",
    )

    @api.onchange("country_id")
    def _empty_state_if_not_match_country(self):
        if self.country_id != self.state_id.country_id:
            self.state_id = None

    _sql_constraints = [
        ("unique_label_country", "unique (label, country_id)",
            "Only one state / province can be mapped per label and country.")
    ]

    @api.model
    def map(self, country, label):
        state = self.search(
            [("country_id", "=", country.id), ("label", "=", label)]
        ).state_id
        if not state:
            raise ValidationError(_(
                "No state/province found for the label {}"
            ).format(label))
        return state
