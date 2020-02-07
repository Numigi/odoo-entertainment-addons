# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestRecordings(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.artist_1 = cls.env['artist'].create({
            'name': 'Artist 1',
        })
        cls.artist_2 = cls.env['artist'].create({
            'name': 'Artist 2',
        })

        cls.record_1 = cls.env['recording'].create({
            'name': 'A',
            'ttype': 'sound',
            'artist_id': cls.artist_1.id,
        })
        cls.record_2 = cls.env['recording'].create({
            'name': 'B',
            'ttype': 'sound',
            'artist_id': cls.artist_2.id,
        })

        cls.product_1 = cls.env['product.template'].create({
            'name': 'A1',
            'musical_relation': 'sound',
            'recording_id': cls.record_1.id,
        })
        cls.product_2 = cls.env['product.template'].create({
            'name': 'A2',
            'musical_relation': 'sound',
            'recording_id': cls.record_1.id,
        })

    def test_related_products_count(self):
        assert self.record_1.related_product_count == 2

    def test_artist_propagated_to_products(self):
        assert self.product_1.artist_id == self.artist_1
        self.record_1.artist_id = self.artist_2
        assert self.product_1.artist_id == self.artist_2

    def test_when_setting_record_on_product__artist_propagated(self):
        assert self.product_1.artist_id == self.artist_1
        self.product_1.recording_id = self.record_2
        assert self.product_1.artist_id == self.artist_2
