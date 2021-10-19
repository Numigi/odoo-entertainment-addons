# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectShowContribution(models.Model):

    _name = "project.show.contribution"
    _description = "Project Show Contribution"
    _order = "sequence"

    sequence = fields.Integer()

    project_id = fields.Many2one(
        "project.project", ondelete="cascade", required=True, index=True
    )

    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )

    register_id = fields.Many2one(
        "hr.contribution.register", "Contribution Register", required=True
    )

    code = fields.Char(
        "Contribution Code",
        required=True,
    )

    base_amount = fields.Monetary("Base Amount")
    rate = fields.Float()
    coefficient = fields.Float(default=1)
    amount = fields.Monetary("Contribution Amount", compute="_compute_amount", store=True)
    currency_id = fields.Many2one(related="project_id.currency_id")

    @api.depends("coefficient", "rate", "base_amount")
    def _compute_amount(self):
        for line in self:
            line.amount = line.base_amount * line.rate * line.coefficient
