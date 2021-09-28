# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Lead(models.Model):
    _inherit = "crm.lead"

    artist = fields.Many2one("artist")
    artworks = fields.Many2many("musical.artwork", "artwork_lead_rel", "crm_lead_id", "musical_artwork_id")
    has_rights = fields.Many2many("musical.artwork.distribution.line", compute="_compute_has_rights")


    def _compute_has_rights(self):
        pass