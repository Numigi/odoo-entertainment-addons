# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase
from odoo.tests.common import tagged


@tagged("post_install")
class TestArtworkCredentialFormat(SavepointCase):
    def test__check_iswc_pass_1(self):
        self._create_musical_artwork("T123456789")

    def test__check_iswc_pass_2(self):
        self._create_musical_artwork("T997755331")

    def test__check_iswc_pass_3(self):
        self._create_musical_artwork("T000000000")

    def test__check_iswc_pass_4(self):
        self._write_musical_artwork("T999999999")

    def test__check_iswc_block_1(self):
        with self.assertRaises(ValidationError):
            self._create_musical_artwork("t123456789")

    def test__check_iswc_block_2(self):
        with self.assertRaises(ValidationError):
            self._create_musical_artwork("TT97755331")

    def test__check_iswc_block_3(self):
        with self.assertRaises(ValidationError):
            self._create_musical_artwork("0000000000")

    def test__check_iswc_block_4(self):
        with self.assertRaises(ValidationError):
            self._write_musical_artwork("999999999")

    def _create_musical_artwork(self, iswc):
        self.env["musical.artwork"].create({"title": "Test", "iswc": iswc})

    def _write_musical_artwork(self, iswc):
        self.env["musical.artwork"].create({"title": "Test"}).iswc = iswc
