# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests.common import SavepointCase


class TestShowProject(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.empty_project = cls.env["project.project"]
        cls.standard_project_1 = cls.env["project.project"].create(
            {"name": "Standard Project 1", "show_type": "standard"}
        )
        cls.tour_project_1 = cls.env["project.project"].create(
            {"name": "Tour Project 1", "show_type": "tour"}
        )
        cls.show_project_1 = cls.env["project.project"].create(
            {"name": "Show Project 1", "show_type": "show"}
        )

    def _create_project(self, name, show_type=None, parent_id=None):
        vals = {"name": name, "show_type": show_type, "parent_id": parent_id}
        return self.env["project.project"].create(vals)

    def _update_show_date(self, project, show_date):
        project.write({"show_date": show_date})

    def test_tour_project_dont_have_parent(self):
        self.tour_project_2 = self._create_project(
            "Tour Project 2", show_type="tour", parent_id=self.standard_project_1.id
        )
        self.assertNotEqual(self.tour_project_2.parent_id, self.standard_project_1)

    def test_compute_previous_and_next_show_not_show_project(self):
        self.assertEqual(self.tour_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.standard_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.tour_project_1.next_show_id, self.empty_project)
        self.assertEqual(self.standard_project_1.next_show_id, self.empty_project)

    def test_compute_previous_and_next_show_show_project_without_show_date(self):
        self.assertEqual(self.show_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)

    def test_compute_previous_and_next_show_show_project_with_show_date(self):
        self._update_show_date(self.show_project_1, fields.Date.today())
        self.assertEqual(self.show_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)
        self.show_project_1.parent_id = self.tour_project_1
        self.assertEqual(self.show_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)
        self.show_project_2 = self._create_project(
            "Show Project 2", "show", self.tour_project_1.id
        )
        self.assertEqual(self.show_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)
        self._update_show_date(
            self.show_project_2, fields.Date.today() - relativedelta(days=1)
        )
        self.assertEqual(self.show_project_1.previous_show_id, self.show_project_2)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)
        self.show_project_3 = self._create_project(
            "Show Project 3", "show", self.tour_project_1.id
        )
        self.assertEqual(self.show_project_1.previous_show_id, self.show_project_2)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)
        self._update_show_date(
            self.show_project_3, fields.Date.today() + relativedelta(days=1)
        )
        self.assertEqual(self.show_project_1.previous_show_id, self.show_project_2)
        self.assertEqual(self.show_project_1.next_show_id, self.show_project_3)
