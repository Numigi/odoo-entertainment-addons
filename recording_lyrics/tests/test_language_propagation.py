# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestLanguagePropagation(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.en = cls.env.ref('recording_lang.recording_language_en')
        cls.fr = cls.env.ref('recording_lang.recording_language_fr')

        cls.initial_percentages = [(cls.en, 50), (cls.fr, 50)]
        cls.new_percentages = [(cls.en, 40), (cls.fr, 60)]

        cls.sound_1 = cls.env['recording'].create({
            'name': 'Sound 1',
            'ttype': 'sound',
        })
        cls._set_percentages(cls.sound_1, cls.initial_percentages)

        cls.video_1 = cls.env['recording'].create({
            'name': 'Video 1',
            'ttype': 'video',
            'sound_recording_id': cls.sound_1.id,
        })

    @staticmethod
    def _set_percentages(record, percentages):
        language_vals = [(5, 0)] + [
            (0, 0, {
                'sequence': i,
                'language_id': item[0].id,
                'percentage': item[1],
            }) for i, item in enumerate(percentages)
        ]
        record.write({'language_ids': language_vals})

    def _assert_has_percentages(self, record, expected_percentages):
        actual_percentages = [(item.language_id, item.percentage) for item in record.language_ids]
        assert actual_percentages == expected_percentages

    def test_when_setting_langs_on_sound__langs_propagated_to_video(self):
        self._set_percentages(self.sound_1, self.new_percentages)
        self._assert_has_percentages(self.video_1, self.new_percentages)

    def test_when_selecting_sound__langs_propagated_to_video(self):
        self.video_1.sound_recording_id = False
        self._set_percentages(self.sound_1, self.new_percentages)
        self.video_1.sound_recording_id = self.sound_1
        self._assert_has_percentages(self.video_1, self.new_percentages)

    def test_when_creating_video__langs_propagated_from_sound(self):
        self._assert_has_percentages(self.video_1, self.initial_percentages)
