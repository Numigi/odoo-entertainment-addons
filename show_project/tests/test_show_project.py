# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import SavepointCase


class TestShowProject(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.standard_project_1 = cls.env["project.project"].create(
            {
                "name": "Standard Project 1",
                "project_type": "standard"}
        )
        cls.show_project_1 = cls.env["project.project"].create(
            {
                "name": "Show Project 1",
                "project_type": "show"}
        )
        cls.tour_project_1 = cls.env["project.project"].create(
            {
                "name": "Tour Project 1",
                "project_type": "tour"}
        )

    def _create_project(self, name, project_type=None, parent_id=None):
        vals = {
            "name": name,
            "project_type": project_type,
            "parent_id": parent_id,
        }
        return self.env["project.project"].create(vals)

    def test_onchange_project_type_standard(self):
        result_onchange = self.standard_project_1._onchange_project_type()
        self.assertEqual(result_onchange['domain']['parent_id'], [("project_type", "=", "standard")])

    def test_onchange_project_type_show(self):
        result_onchange = self.show_project_1._onchange_project_type()
        self.assertEqual(result_onchange['domain']['parent_id'], [("project_type", "=", "tour")])

    def test_onchange_project_type_tour(self):
        self.tour_project_1._onchange_project_type()
        self.assertEqual(self.tour_project_1.parent_id, self.env["project.project"])

    def test_tour_project_dont_have_parent(self):
        self.tour_project_2 = self._create_project("Tour Project 2", project_type="tour", parent_id=self.standard_project_1.id)
        self.assertNotEqual(self.tour_project_2.parent_id, self.standard_project_1)
