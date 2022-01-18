# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import Form
from odoo.tests.common import SavepointCase


class TestShowConfiguration(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.distance_from_productor = 100
        cls.show_place_stage = "outdoor"
        cls.place = cls.env["res.partner"].create(
            {
                "name": "My Place",
                "type": "show_site",
                "show_place_distance_from_productor": cls.distance_from_productor,
                "show_place_stage": cls.show_place_stage,
            }
        )

        cls.config = cls.env["show.place.configuration"].create(
            {
                "name": "Outdoor Scene",
            }
        )

        cls.maximum_capacity = 300
        cls.config_line = cls.env["res.partner.show.configuration"].create(
            {
                "partner_id": cls.place.id,
                "name": "My Scene Configuration",
                "configuration_id": cls.config.id,
                "maximum_capacity": cls.maximum_capacity,
                "minor_restriction": True,
            }
        )

    def test_place_propagation_to_project(self):
        project = self._new_project()
        project.show_place_id = self.place
        project._onchange_show_place_id()
        assert project.show_place_distance_from_productor == self.distance_from_productor
        assert project.show_place_stage == self.show_place_stage

    def test_configuration_not_matching_place(self):
        place_2 = self.place.copy()
        project = self._new_project()
        project.show_place_id = place_2
        project.show_place_configuration_id = self.config_line
        project._onchange_show_place_id()
        assert not project.show_place_configuration_id

    def test_configuration_propagation_to_project(self):
        project = self._new_project()
        project.show_place_id = self.place
        project.show_place_configuration_id = self.config_line
        project._onchange_show_place_configuration_id()
        assert project.show_place_maximum_capacity == self.maximum_capacity
        assert project.show_place_minor_restriction is True
        assert project.show_place_configuration == self.config_line.name

    def _new_project(self):
        return self.env["project.project"].new({})
