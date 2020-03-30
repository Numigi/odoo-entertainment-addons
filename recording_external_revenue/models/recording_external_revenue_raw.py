# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class RecordingExternalRevenueRaw(models.Model):
    _name = "recording.external.revenue.raw"
    _description = "Recording External Revenue Raw"

    date = fields.Date(required=True)
    partner = fields.Char(required=True)
    country = fields.Char(required=True)
    state = fields.Char()
    fiscal_position = fields.Selection(
        [("partner", "Partner"), ("revenue", "Revenue")],
        string="Fiscal Position",
        required=True,
    )
    revenue_type = fields.Char(required=True)
    platform = fields.Char()
    sub_platform = fields.Char()
    is_converted = fields.Boolean("Converted", default=False, readonly=True)
    company_id = fields.Many2one(
        "res.partner",
        required=True,
        domain=[("is_company", "=", True)],
    )


class RecordingExternalRevenueRawRecordingIdentifiers(models.Model):
    """ fields of the tab "Recording Identifiers" """
    _inherit = "recording.external.revenue.raw"

    isrc = fields.Char("ISRC")
    upc = fields.Char("UPC")
    recording_external_catalog = fields.Char()
    recording_external_catalog_reference = fields.Char()
    title = fields.Char()
    artist = fields.Char()


class RecordingExternalRevenueRawProductIdentifiers(models.Model):
    """ fields of the tab "Product Identifiers" """
    _inherit = "recording.external.revenue.raw"

    product_reference = fields.Char()
    product_external_catalog = fields.Char()
    product_external_catalog_reference = fields.Char()


class RecordingExternalRevenueRawRevenue(models.Model):
    """ fields of the tab "Revenue" """
    _inherit = "recording.external.revenue.raw"

    # required for for Monetary fields.
    currency_id = fields.Many2one(
        'res.company',
        string="Currency",
        readonly=True
    )

    # Montant brut unitaire (HT)
    gross_amount_per_unit = fields.Monetary("Gross Amount Per Unit")
    quantity = fields.Integer()
    gross_amount = fields.Monetary()
    # waiting for TA#20794
    # revenue = fields.Many2one(
    #     "recording.external.revenue",
    #     readonly=True,
    # )
    currency = fields.Char(required=True)
    tax = fields.Char()
    tax_base = fields.Selection(
        [
            ("net_amount", "Net Amount Before Tax"),
            ("gross_amount", "Gross Amount Before Tax")
        ],
        required=True
    )
    commission_total = fields.Monetary("Total Commissions Amount")
    net_amount_total = fields.Monetary("Total Net Amount")
