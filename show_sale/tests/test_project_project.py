# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import TestRecordings


class TestProject(TestRecordings):
    def test_01_check_so_exist(self):
        self.assertTrue(self.show.check_so_exist)

    def test_02_check_so_exist(self):
        self.order.action_cancel()
        self.assertFalse(self.show.check_so_exist)
