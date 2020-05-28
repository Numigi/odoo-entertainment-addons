# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class RecordingRevenueTypeMapping(models.Model):
    _name = "recording.revenue.type.mapping"
    _description = "Recording Revenue Type Mapping"
    _order = "label"
    _rec_name = "label"

    label = fields.Char(required=True, unique=True, string="Label")
    product_id = fields.Many2one(
        "product.product", ondelete="restrict", required=True,
        domain="[('type', '=', 'service')]",
    )

    _sql_constraints = [
        ("unique_label", "unique (label)", "Only one product can be mapped per label.")
    ]

    @api.model
    def map(self, label):
        revenue_type = self.search([('label', '=', label)]).product_id
        if not revenue_type:
            raise ValidationError(_(
                "No revenue type found for the label {}"
            ).format(label))
        return revenue_type
