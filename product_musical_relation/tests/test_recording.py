# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestRecordings(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.record = cls.env['recording'].create({
            'name': 'A',
            'ttype': 'sound',
        })

        cls.product_1 = cls.env['product.template'].create({
            'name': 'A1',
            'musical_relation': 'sound',
            'recording_id': cls.record.id,
        })
        cls.product_2 = cls.env['product.template'].create({
            'name': 'A2',
            'musical_relation': 'sound',
            'recording_id': cls.record.id,
        })

    def test_related_products_count(self):
        assert self.record.related_product_count == 2
