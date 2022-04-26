# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProject(models.Model):

    _inherit = "project.project"

    show_sale_date = fields.Date("Sale Date", prefetch=False)
    distributor_platform_url = fields.Char("Distributor Platform", prefetch=False)
    show_event_url = fields.Char("Show Event", prefetch=False)
    photo_gallery_url = fields.Char("Photo Gallery", prefetch=False)
    tour_poster_url = fields.Char("Tour Poster", prefetch=False)
    show_description_url = fields.Char("Show Description", prefetch=False)
    biography_url = fields.Char("Biography", prefetch=False)
    announcement_date = fields.Date("Announcement Date", prefetch=False)
    note = fields.Text("Notes", prefetch=False)

    promotional_item_ids = fields.One2many(
        "project.promotional.item", "project_id", "Promotional Items"
    )

    @api.onchange("parent_id")
    def _onchange_parent_propagate_promotion_fields(self):
        if self.parent_id and self.show_type == "show":
            self.tour_poster_url = self.parent_id.tour_poster_url
            self.show_description_url = self.parent_id.show_description_url
            self.promotional_item_ids = self.parent_id._copy_promotional_items()
            self.photo_gallery_url = self.parent_id.photo_gallery_url
            self.show_description_url = self.parent_id.show_description_url
            self.biography_url = self.parent_id.biography_url

    def _copy_promotional_items(self):
        res = self.env["project.promotional.item"]

        for item in self.promotional_item_ids:
            res |= self.env["project.promotional.item"].new(
                {
                    "sequence": item.sequence,
                    "product_id": item.product_id.id,
                    "description": item.description,
                    "notes": item.notes,
                }
            )

        return res
