# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestRecordings(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.capacity = 500
        cls.place = cls.env["res.partner"].create({
            "name": "Theater",
            "show_place_maximum_capacity": cls.capacity,
        })

        cls.show = cls.env["project.project"].create({
            "name": "My Show",
            "show_type": "show",
        })

    def setUp(self):
        super().setUp()
        self.order = self.env["sale.order"].new({})

    def test_onchange_show_place(self):
        self.order.show_place_id = self.place
        self.order.onchange_show_place()
        assert self.order.show_place_maximum_capacity == self.capacity

    def test_onchange_show_project(self):
        self.order.show_project_id = self.show
        self.order.onchange_show_project()
        assert self.order.analytic_account_id == self.show.analytic_account_id
