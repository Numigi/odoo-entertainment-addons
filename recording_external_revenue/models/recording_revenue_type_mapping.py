# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


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
