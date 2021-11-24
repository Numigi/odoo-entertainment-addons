# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectShowMember(models.Model):

    _name = "project.show.member"
    _description = "Project Show Member"
    _rec_name = "partner_id"
    _order = "sequence"

    sequence = fields.Integer()

    project_id = fields.Many2one(
        comodel_name="project.project", required=True, ondelete="cascade", index=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        domain="[('company_type', '=', 'person')]",
        required=True,
    )
    role_id = fields.Many2one(comodel_name="project.show.role", required=True)
    main_artist = fields.Boolean()

    _sql_constraints = [
        (
            "project_partner_uniq",
            "UNIQUE (project_id, partner_id)",
            "A user can only select the same partner on a project once in the Partner field of the Team tab!",
        )
    ]

    @api.onchange("role_id")
    def onchange_role_id(self):
        self.main_artist = self.role_id.main_artist
