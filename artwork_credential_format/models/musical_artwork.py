# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import _, api, models
from odoo.exceptions import ValidationError


class MusicalArtwork(models.Model):
    _inherit = "musical.artwork"

    @api.constrains("iswc")
    def _check_iswc(self):
        pattern = re.compile(r"^T[0-9]{9}$")
        for record in self.filtered(lambda r: r.iswc):
            if not re.fullmatch(pattern, record.iswc):
                raise ValidationError(
                    _(
                        "The field ISWC must respect the following format: T123456789, where:\n"
                        "- T must be the first character and must be uppercase\n"
                        "- 123456789 must be 9 numerical characters\n"
                        "- The length of the string value must be exactly 10 characters"
                    )
                )
