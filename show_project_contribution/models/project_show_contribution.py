# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


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

    employee_id = fields.Many2one(
        "hr.employee",
        required=True,
    )

    register_id = fields.Many2one(
        "hr.contribution.register", "Contribution Register", required=True
    )

    code = fields.Char(
        "Contribution Code",
        required=True,
    )

    base_amount = fields.Float("Base Amount")
