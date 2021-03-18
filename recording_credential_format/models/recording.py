# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class Recording(models.Model):

    _inherit = ["recording", "recording.isrc.format"]
    _name = "recording"
