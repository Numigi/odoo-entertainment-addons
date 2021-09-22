# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectShowPerDiem(models.Model):

    _name = "project.show.perdiem"
    _description = "Project Show Per Diem"
    _order = "sequence"

    sequence = fields.Integer()

    project_id = fields.Many2one(
        "project.project", ondelete="cascade", required=True, index=True
    )

    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )

    perdiem_type_id = fields.Many2one(
        "project.perdiem.type",
        "Type",
        required=True,
    )

    quantity = fields.Float("Quantity")
    unit_amount = fields.Monetary("Unit Amount")
    amount = fields.Monetary("Amount", compute="_compute_amount", store=True)
    currency_id = fields.Many2one(related="project_id.currency_id")

    @api.depends("quantity", "unit_amount")
    def _compute_amount(self):
        for perdiem in self:
            perdiem.amount = perdiem.unit_amount * perdiem.quantity
