# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContributionRegister(models.Model):

    _inherit = "hr.contribution.register"

    is_gmmq = fields.Boolean(readonly=True)
    is_uda = fields.Boolean(readonly=True)

    type_ids = fields.One2many(
        "hr.contribution.type",
        "register_id",
    )
