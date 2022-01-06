# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from ..isrc import check_isrc_code


class RecordingOtherISRC(models.Model):

    _name = "recording.other.isrc"
    _description = "Recording Other ISRC"
    _order = "sequence"

    recording_id = fields.Many2one("recording", ondelete="cascade", required=True)
    sequence = fields.Integer()
    isrc = fields.Char("ISRC", required=True)
    partner_id = fields.Many2one("res.partner", "Issuer")
    notes = fields.Text()
