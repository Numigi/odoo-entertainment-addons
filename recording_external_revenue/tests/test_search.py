# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import ExternalRevenueCase


class TestRawRevenueSearch(ExternalRevenueCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.raw_revenue_1 = cls._create_raw_revenue()
        cls.raw_revenue_2 = cls._create_raw_revenue()

    def _search_raw_revenue_by_name(self, name):
        return self._search_by_name('recording.external.revenue.raw', name)

    def _search_by_name(self, model, name):
        ids = [t[0] for t in self.env[model].name_search(name)]
        return self.env[model].browse(ids)

    def test_search_raw_revenue_by_id(self):
        result = self._search_raw_revenue_by_name(str(self.raw_revenue_1.id))
        assert self.raw_revenue_1 in result
        assert self.raw_revenue_2 not in result
