# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectPriceMixin(models.AbstractModel):

    _name = "project.price.mixin"
    _description = "Project Price Mixin"

    project_id = fields.Many2one("project.project", required=True, index=True, ondelete="cascade")
    segment_id = fields.Many2one("show.customer.segment", "Customer Segment", required=True)
    price = fields.Monetary()
    currency_id = fields.Many2one(
        "res.currency",
        related="project_id.sale_currency_id",
        store=True,
    )
