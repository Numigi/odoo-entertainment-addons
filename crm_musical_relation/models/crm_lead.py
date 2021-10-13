# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Lead(models.Model):
    _inherit = "crm.lead"

    artist_id = fields.Many2one("artist", ondelete="restrict")
    artwork_ids = fields.Many2many(
        "musical.artwork",
        "musical_artwork_lead_rel",
        "crm_lead_id",
        "musical_artwork_id",
        string="Artworks",
    )
    artwork_distribution_line_ids = fields.Many2many(
        "musical.artwork.distribution.line",
        "crm_lead_musical_artwork_distribution_line_rel",
        "lead_id",
        "line_id",
        string="Beneficiary",
        compute="_compute_artwork_distribution_line_ids",
    )
    recording_ids = fields.Many2many(
        "recording",
        "recording_lead_rel",
        "crm_lead_id",
        "recording_id",
        string="Recordings",
    )

    @api.depends("artwork_ids")
    def _compute_artwork_distribution_line_ids(self):
        for rec in self:
            rec.artwork_distribution_line_ids = rec.env[
                "musical.artwork.distribution.line"
            ].search(
                [
                    ("distribution_id.musical_artwork_id", "in", rec.artwork_ids.ids),
                ]
            )
