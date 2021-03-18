# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class RecordingOtherIsrc(models.Model):

    _inherit = ["recording.other.isrc", "recording.isrc.format"]
    _name = "recording.other.isrc"
