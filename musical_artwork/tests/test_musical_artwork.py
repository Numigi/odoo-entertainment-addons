# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestMusicalArtworkCatalogueReferenceSequence(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = cls.env.user
        cls.sequence = cls.env.ref("musical_artwork.musical_artwork_sequence")
        cls.main_company = cls.env.ref("base.main_company")
        cls.env.ref("base.group_multi_company").write({"users": [(4, user.id)]})
        cls.company_A = cls.env["res.company"].create({"name": "A"})

    def test_create_musical_artwork_main_company_pass(self):
        self._switch_company(self.main_company)
        record = self._create_musical_artwork()
        assert record.catalogue_reference.startswith(self.sequence.prefix)

    def test_create_musical_artwork_new_company_fail(self):
        self._switch_company(self.company_A)
        with self.assertRaises(ValidationError):
            self._create_musical_artwork()

    def test_create_musical_artwork_new_company_pass(self):
        specific_code = "EDTC_2"
        self._switch_company(self.company_A)
        self.env["ir.sequence"].create(
            {
                "name": "Musical Artwork",
                "code": "musical.artwork",
                "prefix": specific_code,
                "padding": "8",
                "company_id": self.company_A.id,
            }
        )
        record = self._create_musical_artwork()
        assert record.catalogue_reference.startswith(specific_code)

    def _switch_company(self, company):
        self.env.user.company_id = company.id

    def _create_musical_artwork(self):
        return self.env["musical.artwork"].create({"title": "Test"})
