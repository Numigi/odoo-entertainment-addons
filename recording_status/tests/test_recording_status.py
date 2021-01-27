# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import pytest

from odoo.exceptions import AccessError
from odoo.tests.common import SavepointCase


class TestRecordingStatus(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_user = cls.env.ref("recording.group_user")
        cls.group_manager = cls.env.ref("recording.group_manager")
        cls.user_user = cls.env["res.users"].create(
            {
                "name": "User",
                "login": "User",
                "email": "u@u.u",
                "groups_id": [(4, cls.group_user.id)],
            }
        )
        cls.user_manager = cls.env["res.users"].create(
            {
                "name": "Manger",
                "login": "Manger",
                "email": "m@m.m",
                "groups_id": [(4, cls.group_manager.id)],
            }
        )

    def _create_artwork(self, user=None, custom_vals=None):
        if not user:
            user = self.env["res.users"].browse(1)
        vals = {"title": "MA1"}
        if custom_vals:
            vals.update(custom_vals)
        return self.env["musical.artwork"].sudo(user=user).create(vals)

    def _create_recording(self, user=None, custom_vals=None):
        if not user:
            user = self.env["res.users"].browse(1)
        vals = {"name": "R1", "duration": 0}
        if custom_vals:
            vals.update(custom_vals)
        return self.env["recording"].sudo(user=user).create(vals)

    @staticmethod
    def _validate_artwork(user, artwork):
        artwork.sudo(user=user).action_validate()
        return artwork

    @staticmethod
    def _validate_recording(user, recording):
        recording.sudo(user=user).action_validate()
        return recording

    @staticmethod
    def _modify_artwork(user, artwork):
        artwork.sudo(user=user).lyrics = "ABCDEFG..."
        return artwork

    @staticmethod
    def _modify_recording(user, recording):
        recording.sudo(user=user).ttype = "video"
        return recording

    def test_user_can_not_validate_artwork(self):
        artwork = self._create_artwork(user=self.user_user)
        with pytest.raises(Exception):
            self._validate_artwork(user=self.user_user, artwork=artwork)

    def test_user_can_not_validate_recording(self):
        recording = self._create_recording(user=self.user_user)
        with pytest.raises(Exception):
            self._validate_recording(user=self.user_user, recording=recording)

    def test_manager_can_validate_artwork(self):
        artwork = self._create_artwork(user=self.user_manager)
        self._validate_artwork(user=self.user_manager, artwork=artwork)

    def test_manager_can_validate_recording(self):
        recording = self._create_recording(user=self.user_manager)
        self._validate_recording(user=self.user_manager, recording=recording)

    def test_artwork_modified_by_music_user__then_to_validate(self):
        artwork = self._create_artwork(custom_vals={"state": "validated"})
        assert artwork.state == "validated"
        artwork = self._modify_artwork(user=self.user_user, artwork=artwork)
        assert artwork.state == "to_validate"

    def test_artwork_modified_by_music_manager__then_not_to_validate(self):
        artwork = self._create_artwork(custom_vals={"state": "validated"})
        assert artwork.state == "validated"
        artwork = self._modify_artwork(user=self.user_manager, artwork=artwork)
        assert artwork.state == "validated"

    def test_recording_modified_by_user__then_to_validate(self):
        recording = self._create_recording(custom_vals={"state": "validated"})
        assert recording.state == "validated"
        artwork = self._modify_recording(user=self.user_user, recording=recording)
        assert artwork.state == "to_validate"

    def test_recording_modified_by_manager__then_not_to_validate(self):
        recording = self._create_recording(custom_vals={"state": "validated"})
        assert recording.state == "validated"
        artwork = self._modify_recording(user=self.user_user, recording=recording)
        assert artwork.state == "to_validate"

    def test_artwork_created_by_music_user__then_to_validate(self):
        artwork = self._create_artwork(user=self.user_user)
        assert artwork.state == "to_validate"

    def test_artwork_create_by_music_manager__then_to_validate(self):
        artwork = self._create_artwork(user=self.user_manager)
        assert artwork.state == "to_validate"

    def test_recording_created_by_user__then_to_validate(self):
        recording = self._create_recording(user=self.user_user)
        assert recording.state == "to_validate"

    def test_recording_created_by_manager__then_to_validate(self):
        recording = self._create_recording(user=self.user_manager)
        assert recording.state == "to_validate"

    def test_artwork_validated_by_manager__then_status_validated(self):
        artwork = self._create_artwork(user=self.user_manager)
        artwork = self._validate_artwork(user=self.user_manager, artwork=artwork)
        assert artwork.state == "validated"

    def test_recording_validated_by_manager__then_status_validated(self):
        recording = self._create_recording(user=self.user_manager)
        recording = self._validate_recording(
            user=self.user_manager, recording=recording
        )
        assert recording.state == "validated"

    def test_artwork_validated_by_user__raise_access_error(self):
        artwork = self._create_artwork(user=self.user_user)
        with pytest.raises(AccessError):
            self._validate_artwork(user=self.user_user, artwork=artwork)

    def test_recording_validated_by_user__raise_access_error(self):
        recording = self._create_recording(user=self.user_user)
        with pytest.raises(AccessError):
            self._validate_recording(user=self.user_user, recording=recording)
