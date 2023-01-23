# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import TestRecordings
from odoo.exceptions import ValidationError


class TestSaleOrder(TestRecordings):
    def check_create_so(self):
        return self.env["sale.order"].create(
            {
                "partner_id": self.env.user.partner_id.id,
                "show_project_id": self.show.id,
            }
        )

    def test_onchange_show_project(self):
        self.order.onchange_show_project()
        assert self.order.analytic_account_id == self.show.analytic_account_id

    def test_show_sale_order_count(self):
        assert self.show.show_sale_order_count == 1

    def test_01_check_unique_so(self):
        """
        I try to create a sale order with
        show_project_id that already linked to another sale order
        I check that it failed
        """
        with self.assertRaises(ValidationError):
            self.check_create_so()

    def test_02_check_unique_so(self):
        """
        I try to create a sale order with show_project_id that
        already linked to another sale order but it was cancelled
        I check that the creation will not fail
        """
        self.order.action_cancel()
        assert isinstance(self.check_create_so().id, int)
