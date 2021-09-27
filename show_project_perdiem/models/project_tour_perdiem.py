# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectTourPerDiem(models.Model):

    _name = "project.tour.perdiem.config"
    _description = "Project Tour Per Diem"
    _order = "sequence"

    sequence = fields.Integer()

    project_id = fields.Many2one(
        "project.project", ondelete="cascade", required=True, index=True
    )

    type_id = fields.Many2one(
        "project.perdiem.type",
        "Type",
        required=True,
    )

    unit_amount = fields.Monetary("Unit Amount")
    currency_id = fields.Many2one(related="project_id.currency_id")
