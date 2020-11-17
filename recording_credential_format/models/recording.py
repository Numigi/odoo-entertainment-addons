# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import _, api, models
from odoo.exceptions import ValidationError


class Recording(models.Model):
    _inherit = "recording"

    @api.constrains("isrc", "ttype")
    def _check_isrc(self):
        pattern = re.compile(r"^[A-Z]{2}[A-Z0-9]{3}[0-9]{7}$")
        for record in self.filtered(lambda r: r.isrc and r.ttype != "group"):
            if not re.fullmatch(pattern, record.isrc):
                raise ValidationError(
                    _(
                        "The field ISRC must respect the following format: ABC123456789, where:\n"
                        "- The first two characters must be uppercase letters (example: CA, AU, FR)\n"
                        "- The 3 following characters must be alphanumeric and letters must be using uppercase "
                        "(examples: D12, A43, EN9), accents are not allowed\n"
                        "- The 7 following characters must be numeric characters"
                    )
                )
