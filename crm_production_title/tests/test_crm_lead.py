# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestCrmLead(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.production_type = cls.env["production.type"].create(
            {
                "name": "type",
                "description": "type",
                "active": True,
            }
        )

        cls.production_title = cls.env["production.title"].create(
            {
                "name": "title",
                "description": "title",
                "active": True,
                "type_id": cls.production_type.id,
            }
        )

        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "lead",
            }
        )

    def test_compute_production_type_id(self):
        self.lead.production_title_id = self.production_title
        self.lead._compute_production_type_id()
        assert self.lead.production_type_id == self.production_type
