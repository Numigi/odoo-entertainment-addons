# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartnerShowConfiguration(models.Model):

    _name = "res.partner.show.configuration"
    _description = "Partner Show Place Configuration"

    sequence = fields.Integer()
    partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade")
    name = fields.Char(string="Name", required=True, translate=True)
    configuration_id = fields.Many2one("show.place.configuration", required=True)
    maximum_capacity = fields.Integer(
        string="Maximum capacity",
    )
    minor_restriction = fields.Boolean(
        string="Minor Restriction",
        help="Check this box if this place has a restriction for minors.",
    )

    @api.multi
    def name_get(self):
        return [(r.id, f"{r.name} - {r.maximum_capacity}") for r in self]
