# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartnerDiffuser(models.Model):

    _name = "res.partner.diffuser"
    _inherit = ["diffuser.mixin"]
    _description = "Contact Diffuser"

    inverse_partner_id = fields.Many2one("res.partner")
