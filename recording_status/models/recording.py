# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class Recording(models.Model):

    _inherit = "recording"

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
        if not self.env.user.has_group("recording.group_manager"):
            raise AccessError(_("You don't have access to validate."))
        for record in self:
            record.state = "validated"
