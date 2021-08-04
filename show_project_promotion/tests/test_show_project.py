# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestShowProject(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tour_poster_url = "tour.poster.url"
        cls.show_description_url = "show.description.url"
        cls.tour_biography_url = "tour.biography"
        cls.tour_photo_gallery_url = "tour.photo.gallery"
        cls.tour = cls.env["project.project"].create(
            {
                "name": "Tour Project 1",
                "show_type": "tour",
                "tour_poster_url": cls.tour_poster_url,
                "show_description_url": cls.show_description_url,
                "biography_url": cls.tour_biography_url,
                "photo_gallery_url": cls.tour_photo_gallery_url,
            }
        )
        cls.product = cls.env["product.product"].search([], limit=1)
        cls.item_description = "Some description"
        cls.item_notes = "Some notes"
        cls.item = cls.env["project.promotional.item"].create(
            {
                "project_id": cls.tour.id,
                "product_id": cls.product.id,
                "description": cls.item_description,
                "notes": cls.item_notes,
            }
        )
        cls.show = cls.env["project.project"].create(
            {"name": "Show Project 1", "show_type": "show", "parent_id": cls.tour.id}
        )

    def test_text_field_propagation(self):
        self.show._onchange_parent_propagate_promotion_fields()
        assert self.show.tour_poster_url == self.tour_poster_url
        assert self.show.show_description_url == self.show_description_url
        assert self.show.biography_url == self.tour_biography_url
        assert self.show.photo_gallery_url == self.tour_photo_gallery_url

    def test_promotional_item_propagation(self):
        self.show._onchange_parent_propagate_promotion_fields()
        item = self.show.promotional_item_ids
        assert len(item) == 1
        assert item != self.item
        assert item.product_id == self.product
        assert item.description == self.item_description
        assert item.notes == self.item_notes

    def test_onchange_product(self):
        self.item._onchange_product_id()
        assert (
            self.item.description
            == self.product.get_product_multiline_description_sale()
        )
