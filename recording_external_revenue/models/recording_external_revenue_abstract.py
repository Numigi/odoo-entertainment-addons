# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

date_to_string = fields.Date.to_string


class RecordingExternalRevenueAbstract(models.AbstractModel):
    """Common base between raw and converted revenues."""

    _name = "recording.external.revenue.abstract"
    _description = "Recording External Revenue Abstract"
    _order = "operation_date"
    _rec_name = "id_string"

    id_string = fields.Char("ID (String)", index=True, readonly=True)
    fiscal_position = fields.Selection(
        [("partner", "Partner"), ("revenue", "Revenue")],
        string="Fiscal Position",
        required=True,
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.user.company_id, required=True,
    )

    operation_date = fields.Date(required=True)
    period_start_date = fields.Date(required=True)
    period_end_date = fields.Date(required=True)

    quantity = fields.Float()
    gross_amount_per_unit = fields.Float()
    gross_amount = fields.Float()
    tax_base = fields.Selection(
        [
            ("net_amount", "Net Amount Before Tax"),
            ("gross_amount", "Gross Amount Before Tax"),
        ],
        required=True,
    )

    commission_amount = fields.Float("Total Commissions Amount")
    net_amount = fields.Float("Total Net Amount (Untaxed)")

    @api.multi
    def name_get(self):
        return [(r.id, "#{}".format(r.id)) for r in self]

    @api.model
    def create(self, vals):
        revenue = super().create(vals)
        revenue.id_string = str(revenue.id)
        return revenue

    @api.constrains("operation_date", "period_start_date", "period_end_date")
    def _check_dates(self):
        for revenue in self:
            revenue._check_period_start_before_period_end()
            revenue._check_operation_date_in_period()

    def _check_period_start_before_period_end(self):
        if self.period_start_date > self.period_end_date:
            raise ValidationError(
                _(
                    "The period start date ({start}) must be before "
                    "the period end date ({end})."
                ).format(
                    start=date_to_string(self.period_start_date),
                    end=date_to_string(self.period_end_date),
                )
            )

    def _check_operation_date_in_period(self):
        if not (self.period_start_date <= self.operation_date <= self.period_end_date):
            raise ValidationError(
                _(
                    "The operation date ({operation_date}) must be between "
                    "the period start date ({start}) and "
                    "the period end date ({end})."
                ).format(
                    operation_date=date_to_string(self.operation_date),
                    start=date_to_string(self.period_start_date),
                    end=date_to_string(self.period_end_date),
                )
            )
