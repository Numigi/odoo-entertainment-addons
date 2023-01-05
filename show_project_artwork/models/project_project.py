# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProject(models.Model):

    _inherit = "project.project"

    artwork_ids = fields.Many2many(
        "musical.artwork",
        "project_musical_artwork_rel",
        "project_id",
        "artwork_id",
        "Artworks",
    )
    artwork_note = fields.Text(string="Notes")

    @api.onchange("parent_id")
    def _onchange_parent_propagate_artworks(self):
        if self.parent_id and self.show_type == "show":
            self.artwork_ids = self.parent_id.artwork_ids
