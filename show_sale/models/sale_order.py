# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    is_show = fields.Boolean("Is Show", related="type_id.is_show", store=True)
    show_project_id = fields.Many2one(
        "project.project",
        "Show",
        ondelete="restrict",
    )

    @api.onchange("show_place_id")
    def onchange_show_place(self):
        self.show_place_maximum_capacity = self.show_place_id.show_place_maximum_capacity

    @api.onchange("show_project_id")
    def onchange_show_project(self):
        self.analytic_account_id = self.show_project_id.analytic_account_id
