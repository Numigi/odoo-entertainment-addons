# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    project_member_ids = fields.One2many(
        comodel_name="project.member",
        inverse_name="project_id",
    )

    @api.onchange("parent_id")
    def _onchange_parent_id(self):
        if self.show_type == "show" and self.parent_id:
            # Remove all the old records.
            self.project_member_ids = [(5, 0, 0)]
            # Add new records from project member list of parent project
            self.project_member_ids = [
                (0, 0, {"partner_id": pm.partner_id.id, "role_id": pm.role_id.id})
                for pm in self.parent_id.project_member_ids
            ]
