# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class Employee(models.Model):

    _inherit = "hr.employee"

    contribution_type_ids = fields.Many2many(
        "hr.contribution.type",
        "hr_employee_contribution_type_rel",
        "employee_id",
        "type_id",
        "Contribution Types",
        groups="hr.group_hr_manager",
    )
