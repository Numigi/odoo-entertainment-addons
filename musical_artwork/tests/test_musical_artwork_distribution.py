# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data, unpack
from odoo.tests.common import SavepointCase


@ddt
class TestMusicalArtworkDistribution(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        artwork = cls.env['musical.artwork'].create({
            'title': 'ttitle',
            'iswc': 'tiswc',
            'catalogue_reference': 'tcatalogue_reference'
        })

        cls.distribution = cls.env['musical.artwork.distribution'].create({
            'musical_artwork_id': artwork.id,
            'country_group_id': cls.env.ref('base.europe').id,
        })

    def create_line(self, distribution, percentage):
        partner_id = self.env.ref('base.res_partner_1').id
        role_id = self.env.ref('musical_artwork.musical_artwork_role_author').id

        return self.env['musical.artwork.distribution.line'].create({
            'partner_id': partner_id,
            'role_id': role_id,
            'percentage': percentage,
            'distribution_id': distribution.id,
        })

    @data(
        ([10.0], 10.0),
        ([10.0, 10.0], 20.0),
        ([30.0, 10.0, 15.0], 55.0),
    )
    @unpack
    def test_total_distribution_key(self, values, expected):
        for value in values:
            self.create_line(self.distribution, value)

        assert expected == self.distribution.total_distribution_key
