# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from .common import ExternalRevenueCase


class TestRawRevenueConstraints(ExternalRevenueCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.date_1 = datetime.now().date()
        cls.date_2 = cls.date_1 + timedelta(1)
        cls.date_3 = cls.date_1 + timedelta(2)
        cls.date_4 = cls.date_1 + timedelta(3)

    def test_period_start_date_must_be_before_period_end_date(self):
        with pytest.raises(ValidationError):
            self._create_raw_revenue(
                period_start_date=self.date_4,
                operation_date=self.date_2,
                period_end_date=self.date_3,
            )
