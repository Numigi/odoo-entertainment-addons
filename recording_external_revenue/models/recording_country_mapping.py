# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class RecordingCountryMapping(models.Model):
    _name = "recording.country.mapping"
    _description = "Recording Country Mapping"
    _order = "label"
    _rec_name = "label"

    label = fields.Char(required=True, unique=True, string="Label")
    country_id = fields.Many2one("res.country", ondelete="restrict", required=True)

    _sql_constraints = [
        ("unique_label", "unique (label)", "Only one country can be mapped per label.")
    ]

    @api.model
    def map(self, label):
        country = self.search([('label', '=', label)]).country_id
        if not country:
            raise ValidationError(_(
                "No country found for the label {}"
            ).format(label))
        return country
