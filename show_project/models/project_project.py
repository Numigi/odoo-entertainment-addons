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
    show_place_id = fields.Many2one(
        comodel_name="res.partner",
        domain="[('type', '=', 'show_site')]",
        string="Venue",
    )
    show_place_maximum_capacity = fields.Integer(
        related="show_place_id.show_place_maximum_capacity",
        string="Maximum Capacity"
    )
    show_place_configuration = fields.Char(
        related="show_place_id.show_place_configuration_id.name",
        string="Configuration of Room"
    )
    show_place_minor_restriction = fields.Boolean(
        related="show_place_id.show_place_minor_restriction",
        store=True,
        string="Minors Restriction"
    )
    show_place_distance_from_montreal = fields.Integer(
        related="show_place_id.show_place_distance_from_montreal",
        store=True,
        string="Distance from Montreal",
    )
    show_place_notes = fields.Text(
        string="Notes",
    )
    previous_show_id = fields.Many2one(
        comodel_name="project.project",
        domain="[('parent_id', '=', parent_id), ('project_type', '=', 'show')]",
        compute="_compute_show_id",
        store=True,
    )
    next_show_id = fields.Many2one(
        comodel_name="project.project",
        domain="[('parent_id', '=', parent_id), ('project_type', '=', 'show')]",
        compute="_compute_show_id",
        store=True,
    )

    @api.depends("parent_id", "parent_id.child_ids", "parent_id.child_ids.show_date",
                 "project_type", "show_date")
    def _compute_show_id(self):
        for project in self:
            if project.project_type == "show" and project.show_date:
                show_projects = \
                    (project.parent_id.child_ids - project).filtered(
                        lambda r: r.project_type == "show" and r.show_date)
                previous_show_projects = \
                    show_projects.filtered(
                        lambda r: r.show_date <= project.show_date
                    )
                next_show_projects = \
                    show_projects.filtered(
                        lambda r: r.show_date >= project.show_date
                    )
                if previous_show_projects:
                    project.previous_show_id = previous_show_projects.sorted("show_date", reverse=True)[0]
                else:
                    project.previous_show_id = False
                if next_show_projects:
                    project.next_show_id = next_show_projects.sorted("show_date")[0]
                else:
                    project.next_show_id = False
            else:
                project.previous_show_id = False
                project.next_show_id = False

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

    @api.onchange("show_place_id")
    def _onchange_show_place_id(self):
        if self.show_place_id:
            self.show_place_notes = self.show_place_id.show_place_notes
