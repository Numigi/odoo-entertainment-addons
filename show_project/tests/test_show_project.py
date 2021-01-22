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
                "show_type": "standard"}
        )

    def _create_project(self, name, show_type=None, parent_id=None):
        vals = {
            "name": name,
            "show_type": show_type,
            "parent_id": parent_id,
        }
        return self.env["project.project"].create(vals)

    def test_tour_project_dont_have_parent(self):
        self.tour_project_2 = self._create_project("Tour Project 2", show_type="tour", parent_id=self.standard_project_1.id)
        self.assertNotEqual(self.tour_project_2.parent_id, self.standard_project_1)
