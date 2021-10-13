# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestCrmLead(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.artist = cls.env["artist"].create(
            {
                "name": "artist",
            }
        )

        cls.artwork = cls.env["musical.artwork"].create(
            {
                "name": "artwork",
                "title": "title",
            }
        )

        cls.role = cls.env["musical.artwork.role"].create(
            {
                "name": "role",
                "code": "r0l3",
            }
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "partner",
            }
        )

        cls.distribution = cls.env["musical.artwork.distribution"].create(
            {
                "musical_artwork_id": cls.artwork.id,
                "country_group_id": cls.env.ref("base.europe").id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": cls.partner.id,
                            "role_id": cls.role.id,
                            "percentage": 100,
                        },
                    )
                ],
            }
        )

        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "lead",
                "artist_id": cls.artist.id,
                "artwork_ids": [(4, cls.artwork.id)],
            }
        )

    def test_compute_has_rights(self):
        self.lead.artwork_id = self.artwork
        distribution_line = self.lead.artwork_distribution_line_ids
        assert len(distribution_line) == 1
        assert distribution_line.distribution_id == self.distribution
