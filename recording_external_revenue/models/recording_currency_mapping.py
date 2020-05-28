# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class RecordingCurrencyMapping(models.Model):
    _name = "recording.currency.mapping"
    _description = "Recording Currency Mapping"
    _order = "label"
    _rec_name = "label"

    label = fields.Char(required=True, unique=True, string="Label")
    currency_id = fields.Many2one("res.currency", ondelete="restrict", required=True)

    _sql_constraints = [
        ("unique_label", "unique (label)", "Only one currency can be mapped per label.")
    ]

    @api.model
    def map(self, label):
        currency = self.search([('label', '=', label)]).currency_id
        if not currency:
            raise ValidationError(_(
                "No currency found for the label {}"
            ).format(label))
        return currency
