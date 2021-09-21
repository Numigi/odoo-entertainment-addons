# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Project(models.Model):

    _inherit = "project.project"

    contribution_base_ids = fields.Many2many(
        "hr.contribution.base",
        "hr_employee_contribution_base_rel",
        "employee_id",
        "base_id",
        "Contribution Bases",
    )

    show_contribution_ids = fields.One2many(
        "project.show.contribution",
        "project_id",
        "Contributions",
    )

    @api.constrains("contribution_base_ids")
    def _check_contribution_bases(self):
        for project in self:
            types = project.mapped("contribution_base_ids.type_id")
            if len(types) != len(project.contribution_base_ids):
                raise ValidationError(_(
                    "You may not select multiple applicable contributions "
                    "of the same type."
                ))

    def compute_show_contributions(self):
        self.show_contribution_ids = None
        for show in self:
            show._compute_show_contributions()

    def _compute_show_contributions(self):
        for employee in self._iter_employees_for_contributions():
            self._compute_employee_contributions(employee)

    def _compute_employee_contributions(self, employee):
        for base in self._iter_contribution_bases(employee):
            self._create_show_contribution(base, employee)

    def _create_show_contribution(self, base, employee):
        vals = self._get_show_contribution_values(base, employee)
        self.write({"show_contribution_ids": [(0, 0, vals)]})

    def _get_show_contribution_values(self, base, employee):
        return {
            "partner_id": employee.address_id.id,
            "employee_id": employee.id,
            "base_amount": base.amount,
            "code": base.type_id.code,
            "register_id": base.type_id.register_id.id,
        }

    def _iter_contribution_bases(self, employee):
        for base in self.contribution_base_ids:
            if base.type_id in employee.contribution_type_ids:
                yield base

    def _iter_employees_for_contributions(self):
        partners = self.mapped("show_member_ids.partner_id")
        for partner in partners:
            employee = self._get_employee_from_partner(partner)
            if not employee:
                raise ValidationError(_(
                    "All partners must have a related employee "
                    "in order to compute the contribution bases."
                    "The partner {} has no related employee."
                ).format(partner.display_name))
            yield employee

    def _get_employee_from_partner(self, partner):
        return self.env["hr.employee"].search(
            [
                ("address_id", "=", partner.id),
            ], limit=1
        )
