# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data, unpack
from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


@ddt
class TestMusicalArtworkDistribution(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.artwork = cls.env['musical.artwork'].create({
            'title': 'ttitle',
            'iswc': 'tiswc',
            'catalogue_reference': 'tcatalogue_reference'
        })

        cls.role = cls.env.ref('musical_artwork.musical_artwork_role_author')
        cls.partner = cls.env.ref('base.res_partner_1')

        cls.distribution = cls.env['musical.artwork.distribution'].create({
            'musical_artwork_id': cls.artwork.id,
            'country_group_id': cls.env.ref('base.europe').id,
            'line_ids': [(0, 0, {
                'partner_id': cls.partner.id,
                'role_id': cls.role.id,
                'percentage': 100,
            })]
        })

    def _new_line(self, percentage):
        return self.env['musical.artwork.distribution.line'].new({
            'partner_id': self.partner.id,
            'role_id': self.role.id,
            'percentage': percentage,
        })

    @data(
        ([10.0], 10.0),
        ([10.0, 10.0], 20.0),
        ([30.0, 10.0, 15.0], 55.0),
    )
    @unpack
    def test_total_distribution_key(self, values, expected):
        with self.env.do_in_onchange():
            self.distribution.update({'line_ids': [(5, 0)]})

            for value in values:
                self.distribution.line_ids |= self._new_line(value)

            assert expected == self.distribution.total_distribution_key

    def test_on_create_sequence_number_assigned(self):
        assert self.distribution.name

    def test_if_distribution_not_100__raise_error(self):
        with pytest.raises(ValidationError):
            self.distribution.line_ids |= self._new_line(0.001)

    def test_musical_artwork_count(self):
        self.distribution.copy({})
        assert self.artwork.distribution_key_count == 2

    def test_distribution_table_html__partner(self):
        assert self.partner.display_name in self.distribution.distribution_table_html

    def test_distribution_table_html__role(self):
        assert self.role.display_name in self.distribution.distribution_table_html

    def test_distribution_table_html__percentage(self):
        assert "100.00" in self.distribution.distribution_table_html

    def test_distribution_table_html__is_managed(self):
        self.distribution.line_ids.is_managed = True
        assert "Yes" in self.distribution.distribution_table_html
        assert "No" not in self.distribution.distribution_table_html

    def test_distribution_table_html__is_not_managed(self):
        self.distribution.line_ids.is_managed = False
        assert "Yes" not in self.distribution.distribution_table_html
        assert "No" in self.distribution.distribution_table_html
