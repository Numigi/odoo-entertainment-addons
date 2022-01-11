# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import Form
from odoo.tests.common import SavepointCase


class TestShowPlace(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_create_diffuser_role(self):
        return self.env["diffuser.role"].create(
            {"name": "Test DR", "description": "Test description"}
        )

    def test_create_partner_diffuser(self):
        individual = self.env["res.partner"].create(
            {"name": "Individual", "email": "test@gmail.com", "mobile": "0123456789"}
        )
        role = self.test_create_diffuser_role()
        with Form(self.env["res.partner"]) as partner_form:
            partner_form.name = "Test"
            with partner_form.diffuser_ids.new() as line:
                line.partner_id = individual
                line.diffuser_role_id = role
                self.assertEqual(line.email, individual.email)
                self.assertEqual(line.mobile, individual.mobile)
