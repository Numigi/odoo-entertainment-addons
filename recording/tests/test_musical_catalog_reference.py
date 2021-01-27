from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestRecordingUniqueConstrains(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rec_1 = cls.env["recording"].create({"name": "Rec 1", "ttype": "sound"})
        cls.rec_2 = cls.env["recording"].create({"name": "Rec 2", "ttype": "sound"})
        cls.catalog_A = cls.env["musical.catalog"].create(
            {"name": "A", "reference_unique": True, "active": True}
        )
        cls.catalog_B = cls.env["musical.catalog"].create(
            {"name": "B", "reference_unique": False, "active": True}
        )

    def test_not_reference_unique_pass(self):
        self._add_musical_catalog_reference(self.rec_1, self.catalog_B, "AAA")
        self._add_musical_catalog_reference(self.rec_1, self.catalog_B, "AAA")
        self._add_musical_catalog_reference(self.rec_2, self.catalog_B, "AAA")

    def test_reference_unique_pass(self):
        self._add_musical_catalog_reference(self.rec_1, self.catalog_A, "AAA")
        self._add_musical_catalog_reference(self.rec_1, self.catalog_A, "BBB")
        self._add_musical_catalog_reference(self.rec_2, self.catalog_A, "CCC")

    def test_reference_unique_fail(self):
        self._add_musical_catalog_reference(self.rec_1, self.catalog_A, "AAA")
        with self.assertRaises(ValidationError):
            self._add_musical_catalog_reference(self.rec_1, self.catalog_A, "AAA")
        with self.assertRaises(ValidationError):
            self._add_musical_catalog_reference(self.rec_2, self.catalog_A, "AAA")

    def _add_musical_catalog_reference(self, recording, catalog, code):
        self.env["musical.catalog.reference"].create(
            {"recording_id": recording.id, "catalog_id": catalog.id, "code": code}
        )
