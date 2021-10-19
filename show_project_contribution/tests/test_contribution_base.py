# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
                "register_id": cls.register.id,
                "amount": 100,
            }
        )

    def test_contribution_type_display_name(self):
        assert self.type_.display_name == f"{self.type_.name} - {self.type_.code}"

    def test_contribution_base_display_name(self):
        assert self.base.display_name == f"{self.register.display_name} - 100.00"
