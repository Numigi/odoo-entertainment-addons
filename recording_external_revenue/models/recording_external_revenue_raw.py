# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class RecordingExternalRevenueRaw(models.Model):
    _name = "recording.external.revenue.raw"
    _description = "Recording External Revenue Raw"
    _order = 'date'

    date = fields.Date(required=True, index=True)
    partner = fields.Char(required=True, index=True)
    country = fields.Char(required=True, index=True)
    state = fields.Char()
    fiscal_position = fields.Selection(
        [("partner", "Partner"), ("revenue", "Revenue")],
        string="Fiscal Position",
        required=True,
    )
    revenue_type = fields.Char(required=True, index=True)
    platform = fields.Char(index=True)
    sub_platform = fields.Char()
    is_converted = fields.Boolean("Converted", default=False, readonly=True, index=True)
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.user.company_id,
    )


class RecordingExternalRevenueRawRecordingIdentifiers(models.Model):
    """ fields of the tab "Recording Identifiers" """
    _inherit = "recording.external.revenue.raw"

    isrc = fields.Char("ISRC", index=True)
    upc = fields.Char("UPC", index=True)
    recording_external_catalog = fields.Char(index=True)
    recording_external_catalog_reference = fields.Char(index=True)
    title = fields.Char()
    artist = fields.Char()


class RecordingExternalRevenueRawProductIdentifiers(models.Model):
    """ fields of the tab "Product Identifiers" """
    _inherit = "recording.external.revenue.raw"

    product_reference = fields.Char(index=True)
    product_external_catalog = fields.Char(index=True)
    product_external_catalog_reference = fields.Char(index=True)


class RecordingExternalRevenueRawRevenue(models.Model):
    """ fields of the tab "Revenue" """
    _inherit = "recording.external.revenue.raw"

    gross_amount_per_unit = fields.Float("Gross Amount Per Unit")
    quantity = fields.Integer(index=True)
    gross_amount = fields.Float()
    # waiting for TA#20794
    # revenue = fields.Many2one(
    #     "recording.external.revenue",
    #     readonly=True,
    # )
    currency = fields.Char(required=True, index=True)
    tax = fields.Char()
    tax_base = fields.Selection(
        [
            ("net_amount", "Net Amount Before Tax"),
            ("gross_amount", "Gross Amount Before Tax")
        ],
        required=True
    )
    commission_total = fields.Float("Total Commissions Amount")
    net_amount_total = fields.Float("Total Net Amount")
