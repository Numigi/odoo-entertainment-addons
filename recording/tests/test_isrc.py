# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase
from ..isrc import check_isrc_code


@pytest.mark.parametrize('code', [
    '@',
    '*',
    '_',
    '-',
    ' ',
])
def test_no_special_caracters(code):
    with pytest.raises(ValidationError):
        check_isrc_code(code, {})


@pytest.mark.parametrize('code', [
    'USRC17607839',
])
def test_valid_code_does_not_raise_error(code):
    check_isrc_code(code, {})



@pytest.mark.parametrize('code', [
    'ABCD1234567',
    'ABCD123456789',
])
def test_code_must_have_12_chars(code):
    with pytest.raises(ValidationError):
        check_isrc_code(code, {})


class TestRecording(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.record = cls.env['recording'].create({
            'name': 'Sound 1',
            'type': 'sound',
        })

    def test_on_write__if_wrong_isrc__error_raised(self):
        with pytest.raises(ValidationError):
            self.record.isrc = '@wrong'
