# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import sys
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class ProjectShowFee(models.Model):

    _name = "project.show.fee"
    _description = "Project Show Fee"
    _order = "sequence"

    project_id = fields.Many2one(
        "project.project", ondelete="cascade", required=True, index=True
    )

    sequence = fields.Integer()

    partner_id = fields.Many2one("res.partner", ondelete="restrict")

    role_id = fields.Many2one("project.show.role", ondelete="restrict", required=True)
    project_type_id = fields.Many2one("project.type", ondelete="restrict")

    min_sale_amount = fields.Monetary()
    max_sale_amount = fields.Monetary()
    currency_id = fields.Many2one("res.currency", related="project_id.currency_id")

    amount = fields.Monetary(required=True)

    @api.constrains("role_id", "project_type_id")
    def _check_tour_fees_duplicates(self):
        tour_fees = self.filtered(lambda f: f.project_id.show_type == "tour")

        for fee in tour_fees.mapped("project_id.show_fee_ids"):
            fee._check_single_tour_fees_duplicates()

    def _check_single_tour_fees_duplicates(self):
        for fee in self._find_fees_with_same_role():
            self._check_incompatible_project_type(fee)
            self._check_incompatible_sale_range(fee)

    def _find_fees_with_same_role(self):
        return self.project_id.show_fee_ids.filtered(
            lambda f: f.role_id == self.role_id and f != self
        )

    def _check_incompatible_project_type(self, fee):
        if self._has_incompatible_project_type(fee):
            generic_message = self._get_incompatible_fee_message(fee)
            raise ValidationError(
                _(
                    "{}\n\n"
                    "If a fee has no project type, "
                    "another fee can not be defined with the same role "
                    "but no project type."
                ).format(generic_message)
            )

    def _check_incompatible_sale_range(self, fee):
        if self._has_incompatible_sale_range(fee):
            generic_message = self._get_incompatible_fee_message(fee)
            raise ValidationError(
                _(
                    "{}\n\n"
                    "Multiple fees with the same role and project type "
                    "can not have overlapping ranges of sales (Min / Max)."
                ).format(generic_message)
            )

    def _get_incompatible_fee_message(self, fee):
        return _(
            "Two fee entries with the same role ({role}) are incompatible "
            "with one another.\n\n"
            "\t- {fee_1}"
            "\t- {fee_2}"
        ).format(
            fee_1=self.display_name,
            fee_2=fee.display_name,
            role=self.role_id.display_name,
        )

    def _has_incompatible_project_type(self, fee):
        return (not fee.project_type_id and self.project_type_id) or (
            fee.project_type_id and not self.project_type_id
        )

    def _has_incompatible_sale_range(self, fee):
        if self.project_type_id != fee.project_type_id:
            return False

        return self._overlaps_sale_range(fee)

    def _overlaps_sale_range(self, fee):
        min_1 = self.min_sale_amount
        max_1 = self.max_sale_amount or sys.maxsize

        min_2 = fee.min_sale_amount
        max_2 = fee.max_sale_amount or sys.maxsize

        if _lte(min_1, min_2) and _lt(min_2, max_1):
            return True

        if _lt(min_1, max_2) and _lte(max_2, max_1):
            return True

        return False

    def _make_show_fees(self, show):
        result = self.browse([])

        if self._matches_show(show):
            result |= self._make_member_fees(show)

        return result

    def _make_member_fees(self, show):
        result = self.browse([])

        for member in show.show_member_ids:
            if self._matches_member(member):
                result |= self._make_single_member_fee(show, member)

        return result

    def _make_single_member_fee(self, show, member):
        return self.new(
            {
                "amount": self.amount,
                "partner_id": member.partner_id.id,
                "project_type_id": self.project_type_id.id,
                "role_id": self.role_id.id,
                "min_sale_amount": self.min_sale_amount,
                "max_sale_amount": self.max_sale_amount,
            }
        )

    def _matches_show(self, show):
        if not self._matches_sale_amount(show.show_sale_amount):
            return False

        return not self.project_type_id or show.project_type_id == self.project_type_id

    def _matches_sale_amount(self, amount):
        if self.max_sale_amount:
            return _lte(self.min_sale_amount, amount) and _lt(
                amount, self.max_sale_amount
            )
        else:
            return _lte(self.min_sale_amount, amount)

    def _matches_member(self, member):
        return not self.role_id or member.role_id == self.role_id


def _lt(float_1, float_2):
    return float_compare(float_1, float_2, 2) == -1


def _lte(float_1, float_2):
    return float_compare(float_1, float_2, 2) in (-1, 0)
