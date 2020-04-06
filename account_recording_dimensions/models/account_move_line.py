# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class AccountMoveLineRecordingArtist(models.Model):
    _inherit = "account.move.line"
    # Index as we are grouping by these dimensions
    recording_id = fields.Many2one("recording", ondelete="restrict", index=True)
    artist_id = fields.Many2one("artist", ondelete="restrict", index=True)
