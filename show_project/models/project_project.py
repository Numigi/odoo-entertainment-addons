# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    project_type = fields.Selection(
        selection=[
            ('standard', 'Standard'),
            ('tour', 'Tour'),
            ('show', 'Show'),
        ],
        default='standard',
    )
    formula = fields.Char()
    show_date = fields.Date()

    @api.model
    def _set_project_type_vals(self, vals):
        # If project type is `tour`, parent_id should be False
        if vals.get("project_type") == "tour":
            vals.update({"parent_id": False})
        return vals

    @api.model
    def create(self, vals):
        vals = self._set_project_type_vals(vals)
        return super(ProjectProject, self).create(vals)

    @api.multi
    def write(self, vals):
        vals = self._set_project_type_vals(vals)
        return super(ProjectProject, self).write(vals)

    @api.model
    def get_project_domain(self, project_type):
        domain = [
            ("project_type", "=", project_type),
        ]
        return domain

    @api.onchange("project_type")
    def _onchange_project_type(self):
        if self.project_type:
            domain = []
            # project type standard can only have standard parent project
            if self.project_type == "standard":
                domain = self.get_project_domain("standard")
            # project type show can only have tour parent project
            elif self.project_type == "show":
                domain = self.get_project_domain("tour")
            # set False when project_type is tour
            elif self.project_type == "tour":
                self.parent_id = False
            return {"domain": {"parent_id": domain}}
