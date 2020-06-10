# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class RecordingJournalMapping(models.Model):
    _name = "recording.journal.mapping"
    _description = "Recording Journal Mapping"
    _order = "currency_id"

    currency_id = fields.Many2one("res.currency", required=True, unique=True)
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.user.company_id
    )
    journal_id = fields.Many2one(
        "account.journal", ondelete="restrict", required=True,
        domain="""
            [
                '&',
                ('company_id', '=', company_id),
                '|',
                ('currency_id', '=', False),
                ('currency_id', '=', currency_id),
            ]
        """,
    )

    _sql_constraints = [
        (
            "unique_currency_company",
            "unique (currency_id, company_id)",
            "Only one journal can be mapped per currency and company.",
        )
    ]

    @api.model
    def map(self, company, currency):
        mapping = self.search(
            [("company_id", "=", company.id), ("currency_id", "=", currency.id)]
        )
        if not mapping:
            raise ValidationError(
                _("No journal found for the currency {}").format(currency.display_name)
            )
        return mapping.journal_id
