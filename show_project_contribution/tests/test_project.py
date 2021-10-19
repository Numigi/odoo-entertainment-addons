# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestShowContributions(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.gmmq = cls.env.ref("show_project_contribution.gmmq_register")
        cls.uda = cls.env.ref("show_project_contribution.uda_register")

        cls.uda_type_1 = cls.env.ref("show_project_contribution.uda_type_1")
        cls.gmmq_type_1 = cls.env.ref("show_project_contribution.gmmq_type_1")

        cls.gmmq.type_ids.write({"active": False})
        cls.uda.type_ids.write({"active": False})
        cls.uda_type_1.active = True
        cls.gmmq_type_1.active = True

        cls.uda_base = cls.env.ref("show_project_contribution.uda_base_1")
        cls.gmmq_base_1 = cls.env.ref("show_project_contribution.gmmq_base_1")
        cls.gmmq_base_2 = cls.env.ref("show_project_contribution.gmmq_base_2")

        cls.role_main = cls.env.ref("show_project_role.role_main_artist")
        cls.role_musician = cls.env.ref("show_project_role.role_musician")

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Oscar Peterson",
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
                "gmmq_main_artist_base_id": cls.gmmq_base_1.id,
                "gmmq_other_artist_base_id": cls.gmmq_base_2.id,
                "uda_base_id": cls.uda_base.id,
            }
        )

        cls.member_1 = cls.env["project.show.member"].create(
            {
                "project_id": cls.show.id,
                "role_id": cls.role_main.id,
                "partner_id": cls.partner.id,
            }
        )

    def test_compute_no_register_enabled(self):
        self.show.compute_show_contributions()
        assert len(self.show.show_contribution_ids) == 0

    def test_compute_gmmq__main_artist(self):
        self.member_1.gmmq = True
        self.member_1.main_artist = True
        self.show.compute_show_contributions()
        line = self.show.show_contribution_ids
        assert len(line) == 1
        assert line.code == self.gmmq_type_1.code
        assert line.base_amount == self.gmmq_base_1.amount

    def test_compute_gmmq__other_artist(self):
        self.member_1.gmmq = True
        self.show.compute_show_contributions()
        line = self.show.show_contribution_ids
        assert len(line) == 1
        assert line.code == self.gmmq_type_1.code
        assert line.base_amount == self.gmmq_base_2.amount

    def test_compute_uda(self):
        self.member_1.uda = True
        self.show.compute_show_contributions()
        line = self.show.show_contribution_ids
        assert len(line) == 1
        assert line.code == self.uda_type_1.code
        assert line.base_amount == self.uda_base.amount

    def test_coefficient(self):
        self.member_1.gmmq = True
        self.member_1.coefficient = 0.5
        self.gmmq_type_1.rate = 0.08
        self.gmmq_base_2.amount = 100
        self.show.compute_show_contributions()
        line = self.show.show_contribution_ids
        assert line.base_amount == 100
        assert line.coefficient == 0.5
        assert line.rate == 0.08
        assert line.amount == 4  # 100 * 0.5 * 0.08

    def test_onchange_role_id__gmmq(self):
        self.role_main.gmmq = True
        self.member_1.onchange_role_id()
        assert self.member_1.gmmq

    def test_onchange_role_id__uda(self):
        self.role_main.uda = True
        self.member_1.onchange_role_id()
        assert self.member_1.uda

    def test_onchange_role_id__main_artist(self):
        self.member_1.onchange_role_id()
        assert self.member_1.main_artist

    def test_onchange_role_id__coefficient(self):
        self.role_main.coefficient = 0.5
        self.member_1.onchange_role_id()
        assert self.member_1.coefficient == 0.5

