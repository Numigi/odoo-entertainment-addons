# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestLyricsPropagation(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sound_1 = cls.env['recording'].create({
            'name': 'Sound 1',
            'ttype': 'sound',
        })

        cls.video_1 = cls.env['recording'].create({
            'name': 'Video 1',
            'ttype': 'video',
            'sound_recording_id': cls.sound_1.id,
        })

        cls.lyrics = "Jingle bells, jingle bells..."

    def test_when_setting_lytic_on_sound_recording__lyric_propagated_video(self):
        self.sound_1.lyrics = self.lyrics
        assert self.video_1.lyrics == self.lyrics

    def test_when_selecting_sound__lyric_propagated_video(self):
        self.video_1.sound_recording_id = False
        self.sound_1.lyrics = self.lyrics
        self.video_1.sound_recording_id = self.sound_1
        assert self.video_1.lyrics == self.lyrics

    def test_when_creating_video__lyric_propagated_from_sound(self):
        self.sound_1.lyrics = self.lyrics
        video = self.env['recording'].create({
            'name': 'Video 2',
            'ttype': 'video',
            'sound_recording_id': self.sound_1.id,
        })
        assert video.lyrics == self.lyrics
