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

    def test_compute(self):
        self.show.compute_show_contributions()
        lines = self.show.show_contribution_ids
        assert len(lines) == 2
