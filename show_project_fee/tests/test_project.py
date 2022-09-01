# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from ddt import ddt, data, unpack
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class ProjectShowFeeCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = cls.env["res.partner"].create({"name": "Partner 1"})
        cls.partner_2 = cls.env["res.partner"].create({"name": "Partner 2"})

        cls.role_1 = cls.env["project.show.role"].create({"name": "Main Artist"})
        cls.role_2 = cls.env["project.show.role"].create({"name": "Musician"})

        cls.project_type_1 = cls.env["project.type"].create({"name": "Running-In"})
        cls.project_type_2 = cls.env["project.type"].create({"name": "Festival"})

        cls.tour = cls.env["project.project"].create(
            {"name": "Super Tour", "show_type": "tour"}
        )

        cls.amount = 100
        cls.sale_amount = 150

        cls.fee = cls.env["project.show.fee"].create(
            {
                "project_id": cls.tour.id,
                "role_id": cls.role_1.id,
                "project_type_id": cls.project_type_1.id,
                "amount": cls.amount,
                "min_sale_amount": cls.sale_amount - 25,
                "max_sale_amount": cls.sale_amount + 25,
            }
        )

        cls.show = cls.env["project.project"].create(
            {
                "name": "Super Show",
                "show_type": "show",
                "parent_id": cls.tour.id,
                "project_type_id": cls.project_type_1.id,
                "show_sale_amount": cls.sale_amount,
            }
        )
        cls.member_1 = cls.env["project.show.member"].create(
            {
                "role_id": cls.role_1.id,
                "partner_id": cls.partner_1.id,
                "project_id": cls.show.id,
            }
        )
        cls.member_2 = cls.env["project.show.member"].create(
            {
                "role_id": cls.role_2.id,
                "partner_id": cls.partner_2.id,
                "project_id": cls.show.id,
            }
        )


class TestConstraints(ProjectShowFeeCase):
    def test_max_sale_amount__lower_than__min_sale_amount(self):
        with pytest.raises(ValidationError):
            self.fee.write({"max_sale_amount": 1, "min_sale_amount": 2})


@ddt
class TestComputeShowFees(ProjectShowFeeCase):
    def test_fields_mapping(self):
        fees = self._compute_show_fees()
        assert len(fees) == 1
        assert fees.amount == self.amount
        assert fees.partner_id == self.partner_1
        assert fees.role_id == self.role_1
        assert fees.project_type_id == self.project_type_1

    @data(149.99, 150)
    def test_min_sale__matched(self, min_sale_amount):
        self.fee.min_sale_amount = min_sale_amount
        fees = self._compute_show_fees()
        assert len(fees) == 1
        assert fees.amount == self.amount
        assert fees.min_sale_amount == min_sale_amount

    def test_min_sale__not_matched(self):
        self.fee.min_sale_amount = 150.01
        fees = self._compute_show_fees()
        assert not fees

    @data(150, 150.01)
    def test_max_sale__matched(self, max_sale_amount):
        self.fee.max_sale_amount = max_sale_amount
        fees = self._compute_show_fees()
        assert len(fees) == 1
        assert fees.amount == self.amount
        assert fees.max_sale_amount == max_sale_amount

    def test_max_sale__not_matched(self):
        self.fee.max_sale_amount = 149.99
        fees = self._compute_show_fees()
        assert not fees

    @data(-1000, 1, 1000)
    def test_fixed_rate__matched(self, sale_amount):
        self.fee.type_ = "fixed"
        self.fee.min_sale_amount = 0
        self.fee.max_sale_amount = 0
        self.show.show_sale_amount = sale_amount
        fees = self._compute_show_fees()
        assert len(fees) == 1
        assert fees.type_ == "fixed"
        assert fees.amount == self.amount
        assert fees.min_sale_amount == 0
        assert fees.max_sale_amount == 0

    def test_compute_fees__matching_two_partners(self):
        self.member_2.role_id = self.role_1
        fees = self._compute_show_fees()
        assert len(fees) == 2
        assert fees[0].partner_id == self.partner_1
        assert fees[1].partner_id == self.partner_2

    def test_compute_fees__no_specific_project_type(self):
        self.fee.project_type_id = None
        fees = self._compute_show_fees()
        assert len(fees) == 1

    def test_compute_fees__unmatched_project_type(self):
        self.fee.project_type_id = self.project_type_2
        fees = self._compute_show_fees()
        assert len(fees) == 0

    def test_compute_fees_twice(self):
        self._compute_show_fees()
        fees = self._compute_show_fees()
        assert len(fees) == 1

    def test_project_type_not_set(self):
        self.show.project_type_id = False
        with pytest.raises(ValidationError):
            self._compute_show_fees()

    def test_members_not_set(self):
        self.member_1.unlink()
        self.member_2.unlink()
        with pytest.raises(ValidationError):
            self._compute_show_fees()

    def test_no_fees_defined_on_tour(self):
        self.fee.unlink()
        with pytest.raises(ValidationError):
            self._compute_show_fees()

    def _compute_show_fees(self):
        self.show.compute_show_fees()
        return self.show.show_fee_ids


@ddt
class TestIncompatibleFees(ProjectShowFeeCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fee_2 = cls.fee.copy({"project_type_id": cls.project_type_2.id})

    def test_same_project_type(self):
        with pytest.raises(ValidationError):
            self.fee_2.project_type_id = self.project_type_1

    def test_one_fee_with_no_project_type(self):
        with pytest.raises(ValidationError):
            self.fee_2.project_type_id = None

    def test_fees_with_different_ranges(self):
        self.fee_2.write(
            {
                "min_sale_amount": self.fee.max_sale_amount + 0.01,
                "max_sale_amount": 999999,
                "project_type_id": self.project_type_1.id,
            }
        )

    @data((0, 1, 1, 3), (0, 1, 0, 3), (0, 0.99, 0.991, 2))
    @unpack
    def test_overlapped_sale_range(self, min_1, max_1, min_2, max_2):
        self.fee.min_sale_amount = min_1
        self.fee.max_sale_amount = max_1
        self.fee_2.min_sale_amount = min_2
        self.fee_2.max_sale_amount = max_2
        assert self.fee._overlaps_sale_range(self.fee_2)
        assert self.fee_2._overlaps_sale_range(self.fee)

    @data((0, 1, 2, 3), (0, 0.99, 1, 2))
    @unpack
    def test_not_overlapped_sale_range(self, min_1, max_1, min_2, max_2):
        self.fee.min_sale_amount = min_1
        self.fee.max_sale_amount = max_1
        self.fee_2.min_sale_amount = min_2
        self.fee_2.max_sale_amount = max_2
        assert not self.fee._overlaps_sale_range(self.fee_2)
        assert not self.fee_2._overlaps_sale_range(self.fee)

    @unpack
    def test_fixed__overlapped_sale_range(self):
        self.fee_2.type_ = "fixed"
        assert self.fee._overlaps_sale_range(self.fee_2)
        assert self.fee_2._overlaps_sale_range(self.fee)
