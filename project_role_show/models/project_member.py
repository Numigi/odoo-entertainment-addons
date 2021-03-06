# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProjectMember(models.Model):
    _name = "project.member"
    _description = "Project Member"
    _rec_name = "partner_id"

    project_id = fields.Many2one(
        comodel_name="project.project",
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        domain="[('company_type', '=', 'person'), ('is_artist', '=', True)]",
        required=True,
    )
    role_id = fields.Many2one(
        comodel_name="project.tour.role",
        required=True,
    )

    _sql_constraints = [
        (
            'project_partner_uniq',
            'UNIQUE (project_id,partner_id)',
            'A user can only select the same partner on a project once in the Partner field of the Team tab!'
        ),
    ]
