# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class Recording(models.Model):

    _inherit = "musical.artwork"

    state = fields.Selection(
        [("to_validate", "To Validate"), ("validated", "Validated")],
        default="to_validate",
        track_visibility="onchange",
    )

    @api.multi
    def write(self, vals):
        if not self.env.user.has_group("recording.group_manager"):
            vals.update({"state": "to_validate"})
        return super().write(vals)

    @api.multi
    def action_validate(self):
        for record in self:
            record.state = "validated"
