# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase

from odoo.tests.common import tagged


@tagged("post_install")
class TestRecordingCredentialFormatRecordingOtherIsrc(SavepointCase):
    def test__check_isrc_recording_pass_1(self):
        self._create_recording_other_isrc("ABC123456789")

    def test__check_isrc_recording_pass_2(self):
        self._create_recording_other_isrc("ZZ1234567890")

    def test__check_isrc_recording_pass_3(self):
        self._create_recording_other_isrc("XYABC0000000")

    def test__check_isrc_recording_pass_4(self):
        self._write_recording_other_isrc("XYABC9999999")

    def test__check_isrc_recording_block_1(self):
        with self.assertRaises(ValidationError):
            self._create_recording_other_isrc("ABC123456")

    def test__check_isrc_recording_block_2(self):
        with self.assertRaises(ValidationError):
            self._create_recording_other_isrc("111234567890")

    def test__check_isrc_recording_block_3(self):
        with self.assertRaises(ValidationError):
            self._create_recording_other_isrc("XYABCKKKKKKK")

    def test__check_isrc_recording_block_4(self):
        with self.assertRaises(ValidationError):
            self._write_recording_other_isrc("XYABC999999K")

    def _create_recording_other_isrc(self, isrc):
        recording = self.env["recording"].create({"name": "Test"})
        self.env["recording.other.isrc"].create(
            {"isrc": isrc, "recording_id": recording.id}
        )

    def _write_recording_other_isrc(self, isrc):
        recording = self.env["recording"].create({"name": "Test"})
        self.env["recording.other.isrc"].create(
            {"recording_id": recording.id, "isrc": "ABC123456789"}
        ).isrc = isrc
