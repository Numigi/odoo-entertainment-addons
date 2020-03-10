# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Artist(models.Model):
    _inherit = "artist"

    record_count = fields.Integer(compute="_compute_record_count")

    def _compute_record_count(self):
        for rec in self:
            rec.record_count = self.env["recording"].search([
                "|", ("artist_id", "=", rec.id), ("secondary_artist_id", "=", rec.id)
            ], count=True)
