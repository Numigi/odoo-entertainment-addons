# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrderServiceFee(models.Model):

    _name = "sale.order.service.fee"
    _description = "Sale Order Service Fee"

    order_id = fields.Many2one(
        "sale.order", required=True, index=True, ondelete="cascade"
    )
    segment_id = fields.Many2one(
        "show.customer.segment", "Customer Segment", required=True
    )
    price = fields.Monetary()
    currency_id = fields.Many2one("res.currency", related="order_id.currency_id")
