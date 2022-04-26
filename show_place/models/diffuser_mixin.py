# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class DiffuserMixin(models.AbstractModel):

    _name = "diffuser.mixin"
    _description = "Diffuser Mixin"

    partner_id = fields.Many2one(
        "res.partner",
        string="Contact",
        domain="[('is_company', '=', False)]",
        required=True,
    )
    diffuser_role_id = fields.Many2one("diffuser.role", string="Role", required=True)
    email = fields.Char()
    mobile = fields.Char()
    phone = fields.Char()

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        self.email = self.partner_id.email
        self.mobile = self.partner_id.mobile
        self.phone = self.partner_id.phone
