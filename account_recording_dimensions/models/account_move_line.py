# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class AccountMoveLineRecordingArtist(models.Model):
    _inherit = "account.move.line"
    recording_id = fields.Many2one("recording")
    artist_id = fields.Many2one("artist")
