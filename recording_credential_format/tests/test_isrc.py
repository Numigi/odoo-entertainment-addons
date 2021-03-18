# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestIsrc(SavepointCase):
    def test__check_isrc_recording_pass_1(self):
        self._create_recording("ABC123456789")

    def test__check_isrc_recording_pass_2(self):
        self._create_recording("ZZ1234567890")

    def test__check_isrc_recording_pass_3(self):
        self._create_recording("XYABC0000000")

    def test__check_isrc_recording_pass_5(self):
        self._write_recording("XYABC9999999")

    def test__check_isrc_recording_block_1(self):
        with self.assertRaises(ValidationError):
            self._create_recording("ABC123456")

    def test__check_isrc_recording_block_2(self):
        with self.assertRaises(ValidationError):
            self._create_recording("111234567890")

    def test__check_isrc_recording_block_3(self):
        with self.assertRaises(ValidationError):
            self._create_recording("XYABCKKKKKKK")

    def test__check_isrc_recording_block_4(self):
        with self.assertRaises(ValidationError):
            self._write_recording("XYABC999999K")

    def test__create_recording_with_lower_case_isrc(self):
        recording = self._create_recording("abc123456789")
        assert recording.isrc == "ABC123456789"

    def test__edit_recording_with_lower_case_isrc(self):
        recording = self._create_recording(None)
        recording.isrc = "abc123456789"
        recording.refresh()
        assert recording.isrc == "ABC123456789"

    def _create_recording(self, isrc):
        return self.env["recording"].create({"name": "Test", "isrc": isrc})

    def _write_recording(self, isrc):
        self.env["recording"].create({"name": "Test"}).isrc = isrc
