# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestRecordings(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.show = cls.env["project.project"].create({
            "name": "My Show",
            "show_type": "show",
        })

        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.env.user.partner_id.id,
                "show_project_id": cls.show.id,
            }
        )

    def test_onchange_show_project(self):
        self.order.onchange_show_project()
        assert self.order.analytic_account_id == self.show.analytic_account_id

    def test_show_sale_order_count(self):
        assert self.show.show_sale_order_count == 1
