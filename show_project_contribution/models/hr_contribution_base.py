# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContributionBase(models.Model):

    _name = "hr.contribution.base"
    _description = "Contribution Base"
    _order = "type_id, amount"

    amount = fields.Float("Contribution Base", required=True)
    type_id = fields.Many2one(
        "hr.contribution.type", "Contribution Type", required=True
    )
    active = fields.Boolean(default=True)
    description = fields.Text()

    @api.model
    def name_get(self):
        return [(r.id, r._get_display_name()) for r in self]

    def _get_display_name(self):
        return f"{self.type_id.display_name} - {self.amount:.2f}"
