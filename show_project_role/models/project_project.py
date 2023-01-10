# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProject(models.Model):

    _inherit = "project.project"

    show_member_ids = fields.One2many(
        comodel_name="project.show.member", inverse_name="project_id"
    )
    show_members_note = fields.Text(string="Notes")

    @api.onchange("parent_id")
    def _onchange_tour_propagate_members(self):
        if self.show_type == "show" and self.parent_id:
            self.show_member_ids = [(5, 0, 0)] + [
                (0, 0, self._copy_show_member_vals(member))
                for member in self.parent_id.show_member_ids
            ]

    def _copy_show_member_vals(self, member):
        return {
            "partner_id": member.partner_id.id,
            "role_id": member.role_id.id,
            "main_artist": member.main_artist,
        }
