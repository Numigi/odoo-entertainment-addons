# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContributionType(models.Model):

    _name = "hr.contribution.type"
    _description = "Contribution Type"
    _order = "code"

    name = fields.Char(translate=True, required=True)
    code = fields.Char(required=True)
    register_id = fields.Many2one(
        "hr.contribution.register", "Contribution Register", required=True
    )
    active = fields.Boolean(default=True)
    description = fields.Text()

    @api.model
    def name_get(self):
        return [(r.id, r._get_display_name()) for r in self]

    def _get_display_name(self):
        return f"{self.name} - {self.code}"
