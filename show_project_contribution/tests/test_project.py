# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestContributionBase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.register = cls.env["hr.contribution.register"].search([], limit=1)
        cls.type_ = cls.env["hr.contribution.type"].create(
            {
                "register_id": cls.register.id,
                "name": "My Contribution Type",
                "code": "XYZ",
            }
        )
        cls.base = cls.env["hr.contribution.base"].create(
            {
                "type_id": cls.type_.id,
                "amount": 100,
            }
        )

        cls.role = cls.env["project.show.role"].create(
            {
                "name": "Main Artist",
            }
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Joe Pass",
            }
        )

        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Joe Pass",
                "address_id": cls.partner.id,
                "contribution_type_ids": [(4, cls.type_.id)],
            }
        )

        cls.tour = cls.env["project.project"].create(
            {
                "name": "My Tour",
                "show_type": "tour",
            }
        )

        cls.show = cls.env["project.project"].create(
            {
                "name": "My Show",
                "show_type": "show",
                "parent_id": cls.tour.id,
                "contribution_base_ids": [(4, cls.base.id)],
            }
        )

        cls.member = cls.env["project.show.member"].create(
            {
                "project_id": cls.show.id,
                "role_id": cls.role.id,
                "partner_id": cls.partner.id,
            }
        )

    def test_compute(self):
        self.show.compute_show_contributions()
        assert len(self.show.show_contribution_ids) == 1

    def test_compute_twice(self):
        self.show.compute_show_contributions()
        self.show.compute_show_contributions()
        assert len(self.show.show_contribution_ids) == 1

    def test_employee_not_eligible(self):
        self.employee.contribution_type_ids = None
        self.show.compute_show_contributions()
        assert not self.show.show_contribution_ids

    def test_partner_not_linked_to_employee(self):
        self.employee.address_id = None
        with pytest.raises(ValidationError):
            self.show.compute_show_contributions()

    def test_two_bases_with_same_type(self):
        base_2 = self.base.copy({"amount": 200})
        with pytest.raises(ValidationError):
            self.show.contribution_base_ids |= base_2

    def test_two_bases_with_different_type(self):
        type_2 = self.type_.copy({"code": "ZZZ"})
        base_2 = self.base.copy({"amount": 200, "type_id": type_2.id})
        self.show.contribution_base_ids |= base_2
