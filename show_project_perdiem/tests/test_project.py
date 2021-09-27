# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestPerDiem(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.breakfast = cls.env.ref("show_project_perdiem.perdiem_type_breakfast")
        cls.lunch = cls.env.ref("show_project_perdiem.perdiem_type_lunch")
        cls.supper = cls.env.ref("show_project_perdiem.perdiem_type_supper")

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

        cls.tour = cls.env["project.project"].create(
            {
                "name": "My Tour",
                "show_type": "tour",
            }
        )

        cls.tour_perdiem = cls.env["project.tour.perdiem.config"].create(
            {
                "project_id": cls.tour.id,
                "type_id": cls.breakfast.id,
                "unit_amount": 30,
            }
        )

        cls.show = cls.env["project.project"].create(
            {
                "name": "My Show",
                "show_type": "show",
                "parent_id": cls.tour.id,
            }
        )

        cls.show_perdiem_config = cls.env["project.show.perdiem.config"].create(
            {
                "project_id": cls.show.id,
                "type_id": cls.breakfast.id,
                "quantity": 2,
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
        self.show.compute_show_perdiems()
        perdiem = self.show.show_perdiem_ids
        assert len(perdiem) == 1
        assert perdiem.unit_amount == 30
        assert perdiem.quantity == 2
        assert perdiem.total == 60
        assert perdiem.type_id == self.breakfast

    def test_compute_twice(self):
        self.show.compute_show_perdiems()
        self.show.compute_show_perdiems()
        perdiem = self.show.show_perdiem_ids
        assert len(perdiem) == 1

    def test_missing_perdiem_type_on_tour(self):
        self.tour_perdiem.unlink()
        with pytest.raises(ValidationError):
            self.show.compute_show_perdiems()

    def test_tour_with_twice_same_type(self):
        vals = {
            "tour_perdiem_config_ids": [
                (
                    0,
                    0,
                    {
                        "type_id": self.breakfast.id,
                    },
                )
            ]
        }
        with pytest.raises(ValidationError):
            self.tour.write(vals)

    def test_show_with_twice_same_type(self):
        vals = {
            "show_perdiem_config_ids": [
                (
                    0,
                    0,
                    {
                        "type_id": self.breakfast.id,
                    },
                )
            ]
        }
        with pytest.raises(ValidationError):
            self.show.write(vals)
