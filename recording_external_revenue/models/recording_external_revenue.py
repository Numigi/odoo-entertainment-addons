# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class RecordingExternalRevenue(models.Model):
    _name = "recording.external.revenue"
    _description = "Recording External Revenue"
    _order = 'operation_date'

    product_id = fields.Many2one('product.product', ondelete='restrict')
    partner_id = fields.Many2one('res.partner', ondelete='restrict')
    platform_id = fields.Many2one('recording.platform', ondelete='restrict')
    subplatform_id = fields.Many2one('recording.subplatform', ondelete='restrict')
    country_id = fields.Many2one('res.country', ondelete='restrict')
    state_id = fields.Many2one('res.country.state', ondelete='restrict')
    currency_id = fields.Many2one('res.currency', ondelete='restrict')
    recording_id = fields.Many2one('recording', ondelete='restrict')
    artist_id = fields.Many2one('artist', ondelete='restrict')
    analytic_account_id = fields.Many2one('account.analytic.account', ondelete='restrict')

    fiscal_position = fields.Selection(
        [("partner", "Partner"), ("revenue", "Revenue")],
        string="Fiscal Position",
    )
    revenue_type = fields.Char(index=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.user.company_id,
    )

    operation_date = fields.Date()
    period_start_date = fields.Date()
    period_end_date = fields.Date()

    quantity = fields.Float()
    gross_amount_per_unit = fields.Float()
    gross_amount = fields.Float()
    tax_id = fields.Many2one('account.tax', ondelete='restrict')
    tax_base = fields.Selection(
        [
            ("net_amount", "Net Amount Before Tax"),
            ("gross_amount", "Gross Amount Before Tax")
        ],
    )

    raw_unit_amount = fields.Float("Raw Unit Amount (Untaxed)")
    raw_amount = fields.Float("Total Raw Amount (Untaxed)")
    commission_amount = fields.Float("Total Commissions Amount")
    net_amount = fields.Float("Total Net Amount (Untaxed)")

    raw_revenue_ids = fields.One2many(
        "recording.external.revenue.raw",
        "revenue_id",
        "Raw Data Lines",
    )
    raw_revenue_count = fields.Integer(compute="_compute_raw_revenue_count")

    def _compute_raw_revenue_count(self):
        for line in self:
            line.raw_revenue_count = len(line.raw_revenue_ids)
