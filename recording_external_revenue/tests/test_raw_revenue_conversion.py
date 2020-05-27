# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


class TestMusicalArtworkDistribution(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.raw_revenue_1 = cls._make_raw_revenue()

    def _make_raw_revenue(self, **kwargs):
        return cls.env["recording.external.revenue.raw"].create(kwargs)
