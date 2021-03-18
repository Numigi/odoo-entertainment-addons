# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestShowProject(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.artwork_1 = cls.env["musical.artwork"].create({"title": "Artwork 1"})
        cls.artwork_2 = cls.env["musical.artwork"].create({"title": "Artwork 2"})
        cls.tour = cls.env["project.project"].create(
            {"name": "Tour Project 1", "show_type": "tour"}
        )
        cls.tour.artwork_ids = cls.artwork_1 | cls.artwork_2
        cls.show = cls.env["project.project"].create(
            {"name": "Show Project 1", "show_type": "show", "parent_id": cls.tour.id}
        )

    def test_artwork_propagation(self):
        self.show._onchange_parent_propagate_artworks()
        assert self.show.artwork_ids == self.artwork_1 | self.artwork_2
