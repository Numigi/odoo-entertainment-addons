# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):

    _inherit = "project.project"

    show_sale_amount = fields.Monetary()

    show_fee_ids = fields.One2many("project.show.fee", "project_id", "Show Fees")
    show_fee_note = fields.Text(string="Notes")

    def compute_show_fees(self):
        for project in self:
            project._check_can_compute_show_fees()
            project._compute_show_fees()

    def _check_can_compute_show_fees(self):
        if (
            not self.project_type_id
            or not self.show_member_ids
        ):
            raise ValidationError(
                _(
                    "Could not compute the fees for the show {show}. "
                    "The computation of fees is based on the type of project, "
                    "the amount of sales and the members of the show. "
                    "These data must be filled in."
                ).format(show=self.display_name)
            )

        if not self.parent_id.show_fee_ids:
            raise ValidationError(
                _(
                    "Could not compute the fees for the show {show}. "
                    "The computation of fees is based on the data configured in "
                    "the fees tab of the tour. "
                    "There is no data defined in the fees tab of the parent project ({tour})."
                ).format(show=self.display_name, tour=self.parent_id.display_name)
            )

    def _compute_show_fees(self):
        result = []

        for fee in self.parent_id.show_fee_ids:
            show_fees = fee._compute_fees(self)
            result.extend(show_fees)

        self.write(
            {
                "show_fee_ids": [
                    (5, 0),
                    *((0, 0, dict(vals, sequence=i)) for i, vals in enumerate(result)),
                ]
            }
        )
