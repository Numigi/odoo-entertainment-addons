# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data, unpack
from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


@ddt
class TestRecording(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.sound_1 = cls.env["recording"].create({"name": "Sound 1", "ttype": "sound"})
        cls.sound_2 = cls.env["recording"].create({"name": "Sound 2", "ttype": "sound"})
        cls.video_1 = cls.env["recording"].create({"name": "Video 1", "ttype": "video"})
        cls.video_2 = cls.env["recording"].create({"name": "Video 1", "ttype": "video"})
        cls.group_1 = cls.env["recording"].create(
            {
                "name": "Group 1",
                "ttype": "group",
                "track_ids": [
                    (0, 0, {"sequence": 1, "recording_id": cls.sound_1.id}),
                    (0, 0, {"sequence": 2, "recording_id": cls.sound_2.id}),
                ],
            }
        )

    def test_number_of_related_video(self):
        self.video_1.sound_recording_id = self.sound_1
        assert self.sound_1.related_video_count == 1

    def test_number_of_related_group(self):
        self.video_1.sound_recording_id = self.sound_1
        assert self.sound_1.related_group_count == 1

    def test_number_of_tracks(self):
        assert self.group_1.number_of_tracks == 2

    def test_group_duration(self):
        self.sound_1.duration = 8
        self.sound_2.duration = 2
        assert self.group_1.group_duration == 10

    @data("0", "1", "1A")
    def test_next_volume(self, volume):
        self.group_1.track_ids[1].volume = volume
        assert self.group_1.next_volume_number == volume

    @data(("0", "1"), ("2", "3"), (" 2 ", "3"))
    @unpack
    def test_next_track(self, last_track, expected_next_track):
        self.group_1.track_ids[1].track = last_track
        assert self.group_1.next_track_number == expected_next_track

    def test_if_no_track_next_volume_is_1(self):
        self.group_1.track_ids.unlink()
        assert self.group_1.next_volume_number == "1"

    def test_if_no_track_next_track_is_1(self):
        self.group_1.track_ids.unlink()
        assert self.group_1.next_track_number == "1"


class TestRecordingGroup(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.sound_1 = cls.env["recording"].create({"name": "Sound 1", "ttype": "sound"})
        cls.sound_2 = cls.env["recording"].create({"name": "Sound 2", "ttype": "sound"})
        cls.group_1 = cls.env["recording"].create({"name": "Group 1", "ttype": "group"})

        cls.track_pool = cls.env["recording.track"]

    def test_whenSameSoundAddedTwice_thenRaiseError(self):
        track_1 = self.track_pool.create(
            {
                "recording_group_id": self.group_1.id,
                "volume": 1,
                "track": 1,
                "recording_id": self.sound_1.id,
            }
        )
        track_2 = self.track_pool.create(
            {
                "recording_group_id": self.group_1.id,
                "volume": 1,
                "track": 2,
                "recording_id": self.sound_1.id,
            }
        )

        with pytest.raises(ValidationError):
            self.group_1.write({"track_ids": [(6, 0, [track_1.id, track_2.id])]})

    def test_whenTrackWithDifferentRecordings_thenTheyAreAddedToTheGRoup(self):
        track_1 = self.track_pool.create(
            {
                "recording_group_id": self.group_1.id,
                "volume": 1,
                "track": 1,
                "recording_id": self.sound_1.id,
            }
        )
        track_2 = self.track_pool.create(
            {
                "recording_group_id": self.group_1.id,
                "volume": 1,
                "track": 2,
                "recording_id": self.sound_2.id,
            }
        )

        self.group_1.write({"track_ids": [(6, 0, [track_1.id, track_2.id])]})
        assert 2 == len(self.group_1.track_ids)


class TestRecordingUniqueConstrains(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rec_1 = cls.env["recording"].create({"name": "Rec 1", "ttype": "sound"})
        cls.rec_2 = cls.env["recording"].create({"name": "Rec 2", "ttype": "sound"})

    def test_unique_upc_pass(self):
        self.rec_1.upc = "AAA"
        self.rec_2.upc = "BBB"

    def test_unique_upc_fail(self):
        self.rec_1.upc = "AAA"
        with self.assertRaises(ValidationError):
            self.rec_2.upc = "AAA"

    def test_unique_upc_packshot_pass(self):
        self.rec_1.upc_packshot = "AAA"
        self.rec_2.upc_packshot = "BBB"

    def test_unique_upc_packshot_fail(self):
        self.rec_1.upc_packshot = "AAA"
        with self.assertRaises(ValidationError):
            self.rec_2.upc_packshot = "AAA"

    def test_unique_isrc_pass(self):
        self.rec_1.isrc = "AAAAAAAAAAAA"
        self.rec_2.isrc = "BBBBBBBBBBBB"
        self._add_other_isrc(self.rec_1, "CCCCCCCCCCCC")
        self._add_other_isrc(self.rec_2, "DDDDDDDDDDDD")

    def test_unique_isrc_fail(self):
        self.rec_1.isrc = "AAAAAAAAAAAA"
        with self.assertRaises(ValidationError):
            self.rec_2.isrc = "AAAAAAAAAAAA"
        with self.assertRaises(ValidationError):
            self._add_other_isrc(self.rec_1, "AAAAAAAAAAAA")
        with self.assertRaises(ValidationError):
            self._add_other_isrc(self.rec_2, "AAAAAAAAAAAA")

    def _add_other_isrc(self, recording, code):
        self.env['recording.other.isrc'].create({
            'recording_id': recording.id,
            'isrc': code,
            'partner_id': self.env['res.partner'].search([], limit=1).id,
        })
