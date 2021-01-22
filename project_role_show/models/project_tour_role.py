# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProjectTourRole(models.Model):
    _name = "project.tour.role"
    _description = "Project Tour Role"
    _order = "name"

    name = fields.Char(
        translate=True,
        required=True,
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            'name_uniq',
            'UNIQUE (name)',
            'Role with such name already exists!'
        ),
    ]
