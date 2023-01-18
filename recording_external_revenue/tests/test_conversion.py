# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
import decimal

from ddt import ddt, data
from odoo.exceptions import ValidationError
from .common import ExternalRevenueCase


@ddt
class TestConversion(ExternalRevenueCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.r1 = cls._create_raw_revenue()
        cls.r2 = cls._create_raw_revenue(company_id=cls.company.id)
        cls.r3 = cls._create_raw_revenue(company_id=cls.company.id)
        cls.raw_revenues = cls.r1 | cls.r2 | cls.r3

    @classmethod
    def _find_jobs(cls, revenues):
        return (
            cls.env["queue.job"]
            .search(
                [
                    ("model_name", "=", "recording.external.revenue.raw"),
                    ("method_name", "=", "convert"),
                ]
            )
            .filtered(lambda j: set(j.record_ids) == set(revenues.ids))
        )

    @data(
        "partner", "country", "state",
    )
    def test_revenues_group_by(self, field):
        self.r1[field] = "value 1"
        self.r2[field] = "value 2"
        self.r3[field] = "value 1"
        groups = self.raw_revenues.group_by_common_parameters()
        groups = sorted(groups, key=lambda g: len(g))
        assert len(groups) == 2
        assert groups[0] == self.r2
        assert groups[1] == self.r1 | self.r3

    def test_schedule_conversion(self):
        self.r1.partner = "P1"
        self.r2.partner = "P2"
        self.r3.partner = "P1"
        self.env["recording.external.revenue.raw"].schedule_conversion(self.company)
        assert len(self._find_jobs(self.r1 | self.r3)) == 1
        assert len(self._find_jobs(self.r2)) == 1

    def test_records_filtered_per_company(self):
        other_company = self.env["res.company"].create({"name": "Other Company"})
        self.r1.company_id = other_company
        self.r2.company_id = other_company
        self.env["recording.external.revenue.raw"].schedule_conversion(other_company)
        assert len(self._find_jobs(self.r1 | self.r2)) == 1
        assert not self._find_jobs(self.r3)

    @data(
        "commission_amount", "gross_amount", "net_amount", "quantity",
    )
    def test_aggregated_amounts(self, field):
        self.r1[field] = 100
        self.r2[field] = 200
        self.r3[field] = 300
        revenue = self.raw_revenues.convert()
        assert revenue[field] == 600

    def test_gross_amount_per_unit__grouped_by(self):
        self.r1.gross_amount_per_unit = 100
        self.r2.gross_amount_per_unit = 100
        self.r3.gross_amount_per_unit = 200
        self.env["recording.external.revenue.raw"].schedule_conversion(self.company)
        assert len(self._find_jobs(self.r1 | self.r2)) == 1
        assert len(self._find_jobs(self.r3)) == 1

    def test_gross_amount_per_unit__not_summed(self):
        self.raw_revenues.write({"gross_amount_per_unit": 100})
        revenue = self.raw_revenues.convert()
        assert revenue.gross_amount_per_unit == 100

    def test_mapped_field(self):
        partner_label = self.env.ref(
            "recording_external_revenue.demo_mapping_blv"
        ).label
        expected_partner = self.env.ref(
            "recording_external_revenue.demo_partner_believe"
        )
        self.r1.partner = partner_label
        self.r2.partner = partner_label
        self.r3.partner = partner_label
        revenue = self.raw_revenues.convert()
        assert revenue.partner_id == expected_partner

    def test_raw_revenues_linked_to_revenue(self):
        revenue = self.raw_revenues.convert()
        assert revenue.raw_revenue_ids == self.raw_revenues

    def test_raw_revenues__is_converted_flag_checked(self):
        assert all(not r.is_converted for r in self.raw_revenues)
        self.raw_revenues.convert()
        assert all(r.is_converted for r in self.raw_revenues)

    def test_raw_revenue_can_not_be_converted_twice(self):
        self.raw_revenues.convert()
        with pytest.raises(ValidationError):
            self.raw_revenues.convert()

    def test_raw_revenue_can_not_be_modified_after_conversion(self):
        self.raw_revenues.convert()
        with pytest.raises(ValidationError):
            self.raw_revenues.write({"partner": "P1"})

    def test_raw_revenue_can_not_be_deleted_after_conversion(self):
        self.raw_revenues.convert()
        with pytest.raises(ValidationError):
            self.raw_revenues.unlink()

    def test_external_revenue_decimal_precision(self):
        self.raw_revenues.write({"commission_amount": 10.19934})
        revenue = self.raw_revenues.convert()
        d = decimal.Decimal(str(revenue.commission_amount))
        assert abs(d.as_tuple().exponent) <= 2

