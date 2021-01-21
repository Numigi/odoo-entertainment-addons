# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    show_type = fields.Selection(
        selection=[
            ('standard', 'Standard'),
            ('tour', 'Tour'),
            ('show', 'Show'),
        ],
        default='standard',
    )
    formula = fields.Char()
    show_date = fields.Date()
    expected_parent_show_type = fields.Char(
        compute="_compute_expected_parent_show_type",
        store=True,
    )
    parent_id = fields.Many2one(
        domain="[('show_type', '=', expected_parent_show_type)]",
    )

    @api.depends("show_type")
    def _compute_expected_parent_show_type(self):
        for project in self:
            parent_show_type = ''
            if project.show_type == "standard":
                parent_show_type = "standard"
            elif project.show_type == "show":
                parent_show_type = "tour"
            project.expected_parent_show_type = parent_show_type

    @api.model
    def _set_show_type_vals(self, vals):
        # If project type is `tour`, parent_id should be False
        if vals.get("show_type") == "tour":
            vals.update({"parent_id": False})
        return vals

    @api.model
    def create(self, vals):
        vals = self._set_show_type_vals(vals)
        return super(ProjectProject, self).create(vals)

    @api.multi
    def write(self, vals):
        vals = self._set_show_type_vals(vals)
        return super(ProjectProject, self).write(vals)
