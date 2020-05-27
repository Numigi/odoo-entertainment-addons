# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class RecordingExternalRevenueRaw(models.Model):
    _name = "recording.external.revenue.raw"
    _description = "Recording External Revenue Raw"
    _order = 'operation_date'

    operation_date = fields.Date(index=True)
    period_start_date = fields.Date()
    period_end_date = fields.Date()

    partner = fields.Char(index=True)
    country = fields.Char(index=True)
    state = fields.Char()
    fiscal_position = fields.Selection(
        [("partner", "Partner"), ("revenue", "Revenue")],
        string="Fiscal Position",
    )
    revenue_type = fields.Char(index=True)
    platform = fields.Char(index=True)
    subplatform = fields.Char()
    is_converted = fields.Boolean("Converted", default=False, readonly=True, index=True)
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.user.company_id,
    )

    isrc = fields.Char("ISRC", index=True)
    upc = fields.Char("UPC", index=True)
    recording_external_catalog = fields.Char(index=True)
    recording_external_catalog_reference = fields.Char(index=True)
    title = fields.Char()
    artist = fields.Char()

    product_reference = fields.Char(index=True)
    product_external_catalog = fields.Char(index=True)
    product_external_catalog_reference = fields.Char(index=True)

    quantity = fields.Float()
    gross_amount_per_unit = fields.Float()
    gross_amount = fields.Float()
    revenue_id = fields.Many2one(
        "recording.external.revenue",
        readonly=True,
    )
    currency = fields.Char(index=True)
    tax = fields.Char()
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
