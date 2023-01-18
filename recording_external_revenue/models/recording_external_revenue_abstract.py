# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp

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
        "res.company", default=lambda self: self.env.user.company_id, required=True
    )

    operation_date = fields.Date(required=True)
    period_start_date = fields.Date(required=True)
    period_end_date = fields.Date(required=True)

    quantity = fields.Float()
    gross_amount_per_unit = fields.Float(
        digits=dp.get_precision('External Revenues')
    )
    gross_amount = fields.Float(
        digits=dp.get_precision('External Revenues')
    )
    tax_base = fields.Selection(
        [
            ("net_amount", "Net Amount Before Tax"),
            ("gross_amount", "Gross Amount Before Tax"),
        ],
        required=True,
    )

    commission_amount = fields.Float(
        "Total Commissions Amount",
        digits=dp.get_precision('External Revenues')
    )
    net_amount = fields.Float(
        "Total Net Amount (Untaxed)",
        digits=dp.get_precision('External Revenues')
    )

    @api.multi
    def name_get(self):
        return [(r.id, "#{}".format(r.id)) for r in self]

    @api.model
    def create(self, vals):
        revenue = super().create(vals)
        revenue.id_string = str(revenue.id)
        return revenue

    @api.constrains("period_start_date", "period_end_date")
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
