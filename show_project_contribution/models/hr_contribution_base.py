# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContributionBase(models.Model):

    _name = "hr.contribution.base"
    _description = "Contribution Base"
    _order = "type_id, amount"

    amount = fields.Monetary("Contribution Base", required=True)
    register_id = fields.Many2one(
        "hr.contribution.register", "Contribution Register", required=True
    )
    active = fields.Boolean(default=True)
    description = fields.Text()

    currency_id = fields.Many2one("res.currency", compute="_compute_currency_id")

    is_gmmq = fields.Boolean(related="register_id.is_gmmq", store=True)
    is_uda = fields.Boolean(related="register_id.is_uda", store=True)

    @api.model
    def name_get(self):
        return [(r.id, r._get_display_name()) for r in self]

    def _get_display_name(self):
        return f"{self.register_id.display_name} - {self.amount:.2f}"

    def _compute_currency_id(self):
        currency = self.env.user.company_id.currency_id

        for rec in self:
            rec.currency_id = currency
