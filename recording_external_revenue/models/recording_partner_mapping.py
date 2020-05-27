# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class RecordingPartnerMapping(models.Model):
    _name = "recording.partner.mapping"
    _description = "Recording Partner Mapping"
    _order = "label"
    _rec_name = "label"

    label = fields.Char(required=True, unique=True, string="Label")
    partner_id = fields.Many2one("res.partner", ondelete="restrict", required=True)

    _sql_constraints = [
        ("unique_label", "unique (label)", "Only one partner can be mapped per label.")
    ]
