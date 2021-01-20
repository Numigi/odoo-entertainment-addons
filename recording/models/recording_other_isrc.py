# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models

from odoo.exceptions import ValidationError

from ..isrc import check_isrc_code


class RecordingOtherISRC(models.Model):

    _name = 'recording.other.isrc'
    _description = 'Recording Other ISRC'
    _order = 'sequence'

    recording_id = fields.Many2one(
        'recording',
        ondelete='cascade',
        required=True,
    )
    sequence = fields.Integer()
    isrc = fields.Char('ISRC', size=12, required=True)
    partner_id = fields.Many2one(
        'res.partner', 'Issuer',
    )
    notes = fields.Text()

    @api.constrains('isrc')
    def _check_isrc(self):
        for line in self:
            check_isrc_code(line.isrc, line._context)

    @api.constrains("isrc")
    def _unique_isrc(self):
        recording_env = self.env["recording"]
        for record in self:
            same_isrc_records = self.search(
                [("isrc", "=", record.isrc), ("id", "!=", record.id)]
            )
            same_isrc_recordings = same_isrc_records.mapped("recording_id")
            same_isrc_recordings |= recording_env.search([("isrc", "=", record.isrc)])
            if same_isrc_recordings:
                raise ValidationError(
                    _(
                        "This ISRC code is already used on another recording %s.\n"
                        "ISRC code must be unique."
                    ) % same_isrc_recordings[:1].display_name
                )
