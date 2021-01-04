# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


class TestMusicalArtworkReferenceSequence(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = cls.env.user
        cls.main_company = cls.env.ref("base.main_company")
        cls.env.ref("base.group_multi_company").write({"users": [(4, user.id)]})
        cls.company_A = cls.env["res.company"].create({"name": "A"})

    def test_create_musical_artwork_main_company_pass(self):
        self._switch_company(self.main_company)
        record = self._create_musical_artwork()
        self._check_musical_artwork_reference(record.reference)

    def test_create_musical_artwork_new_company_fail(self):
        self._switch_company(self.company_A)
        with self.assertRaises(ValidationError):
            self._create_musical_artwork()

    def test_create_musical_artwork_new_company_pass(self):
        self._switch_company(self.company_A)
        self.env["ir.sequence"].create(
            {
                "name": "Musical Artwork",
                "code": "musical.artwork",
                "prefix": "EDTC",
                "padding": "8",
                "company_id": self.company_A.id,
            }
        )
        record = self._create_musical_artwork()
        self._check_musical_artwork_reference(record.reference)

    @staticmethod
    def _check_musical_artwork_reference(reference):
        assert reference == "EDTC00000001"

    def _switch_company(self, company):
        self.env.user.company_id = company.id

    def _create_musical_artwork(self):
        return self.env["musical.artwork"].create({"title": "Test"})
