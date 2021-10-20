# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectShowPerDiemConfig(models.Model):

    _name = "project.show.perdiem.config"
    _description = "Project Show Per Diem Configuration"
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

    quantity = fields.Float("Quantity")
