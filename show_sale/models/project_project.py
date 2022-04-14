# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class Project(models.Model):

    _inherit = "project.project"

    show_sale_order_ids = fields.One2many(
        "sale.order",
        "show_project_id",
    )

    show_sale_order_count = fields.Integer(compute="_compute_show_sale_order_count")

    def _compute_show_sale_order_count(self):
        for project in self:
            project.show_sale_order_count = len(project.show_sale_order_ids)
