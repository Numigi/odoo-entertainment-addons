# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class RecordingExternalRevenueRaw(models.Model):
    _name = "recording.external.revenue.raw"
    _description = "Recording External Revenue Raw"
    _order = "operation_date"

    operation_date = fields.Date(index=True)
    period_start_date = fields.Date()
    period_end_date = fields.Date()

    partner = fields.Char(index=True)
    country = fields.Char(index=True)
    state = fields.Char()
    fiscal_position = fields.Selection(
        [("partner", "Partner"), ("revenue", "Revenue")], string="Fiscal Position",
    )
    revenue_type = fields.Char(index=True)
    platform = fields.Char(index=True)
    subplatform = fields.Char()
    is_converted = fields.Boolean("Converted", default=False, readonly=True, index=True)
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.user.company_id,
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

    revenue_id = fields.Many2one("recording.external.revenue", readonly=True,)
    currency = fields.Char(index=True)
    tax = fields.Char()
    tax_base = fields.Selection(
        [
            ("net_amount", "Net Amount Before Tax"),
            ("gross_amount", "Gross Amount Before Tax"),
        ],
    )

    quantity = fields.Float()
    gross_amount_per_unit = fields.Float()
    gross_amount = fields.Float()
    commission_amount = fields.Float("Total Commissions Amount")
    net_amount = fields.Float("Total Net Amount (Untaxed)")

    def make_revenue(self):
        revenue = self.env["recording.external.revenue"].new()

        for field in self.get_direct_mapping_fields():
            revenue[field] = self[field]

        revenue.partner_id = self._map_partner()
        revenue.country_id = self._map_country()
        revenue.state_id = self._map_country_state()
        revenue.platform_id = self._map_platform()
        revenue.subplatform_id = self._map_subplatform()
        revenue.product_id = self._map_product()
        revenue.recording_id = self._map_recording()
        revenue.tax_id = self._map_tax()
        revenue.currency_id = self._map_currency()
        return revenue

    def get_direct_mapping_fields(self):
        return [
            "commission_amount",
            "fiscal_position",
            "gross_amount",
            "gross_amount_per_unit",
            "net_amount",
            "operation_date",
            "period_end_date",
            "period_start_date",
            "quantity",
            "tax_base",
        ]

    def _map_partner(self):
        if self.partner:
            return self.env["recording.partner.mapping"].map(self.partner)

    def _map_currency(self):
        if self.currency:
            return self.env["recording.currency.mapping"].map(self.currency)

    def _map_country(self):
        if self.country:
            return self.env["recording.country.mapping"].map(self.country)

    def _map_country_state(self):
        if self.country and self.state:
            country = self._map_country()
            return self.env["recording.country.state.mapping"].map(country, self.state)

    def _map_platform(self):
        if self.platform:
            return self.env["recording.platform.mapping"].map(self.platform)

    def _map_subplatform(self):
        if self.platform and self.subplatform:
            platform = self._map_platform()
            return self.env["recording.subplatform.mapping"].map(platform, self.subplatform)

    def _map_product(self):
        if self.product_reference:
            return self._map_product_from_reference()

        if self.product_external_catalog and self.product_external_catalog_reference:
            return self._map_product_from_catalog_reference()

        if self.revenue_type:
            return self._map_product_from_revenue_type()

    def _map_product_from_reference(self):
        product = self.env["product.product"].search(
            [("default_code", "=", self.product_reference)]
        )

        if not product:
            raise self._no_product_found_from_reference_error()

        if len(product) > 1:
            raise self._multiple_products_found_from_reference_error(product)

        return product

    def _no_product_found_from_reference_error(self):
        raise ValidationError(
            _("No product found with the reference {}").format(self.product_reference)
        )

    def _multiple_products_found_from_reference_error(self, products):
        raise ValidationError(
            _(
                "Found more than one product with the reference {reference}:\n\n"
                " * {products}"
            ).format(
                reference=self.product_reference,
                products="\n * ".join(p.display_name for p in products),
            )
        )

    def _map_product_from_catalog_reference(self):
        catalog = self._map_catalog(self.product_external_catalog)

        references = self.env["musical.catalog.reference"].search(
            [
                ("code", "=", self.product_external_catalog_reference),
                ("catalog_id", "=", catalog.id),
            ]
        )

        product = references.mapped("product_template_id.product_variant_ids")

        if not product:
            raise self._no_product_found_from_catalog_error(catalog)

        if len(product) > 1:
            raise self._multiple_products_found_from_catalog_error(catalog, product)

        return product

    def _no_product_found_from_catalog_error(self, catalog):
        raise ValidationError(
            _(
                "No product found with the catalog reference {reference} (Catalog: {catalog})"
            ).format(
                reference=self.product_external_catalog_reference,
                catalog=catalog.display_name,
            )
        )

    def _multiple_products_found_from_catalog_error(self, catalog, products):
        raise ValidationError(
            _(
                "Found more than one product with the catalog reference {reference}"
                "(Catalog: {catalog}):\n\n"
                " * {products}"
            ).format(
                reference=self.product_external_catalog_reference,
                products="\n * ".join(p.display_name for p in products),
                catalog=catalog.display_name,
            )
        )

    def _map_recording(self):
        product = self._map_product()
        if product and product.recording_id:
            return product.recording_id

        if self.isrc:
            return self._map_recording_from_isrc()

        if self.upc:
            return self._map_recording_from_upc()

        if self.recording_external_catalog and self.recording_external_catalog_reference:
            return self._map_recording_from_catalog_reference()

    def _map_recording_from_isrc(self):
        recording = self.env["recording"].search(
            ["|", ("isrc", "=", self.isrc), ("other_isrc_ids.isrc", "=", self.isrc),]
        )

        if not recording:
            raise self._no_isrc_found_error()

        if len(recording) > 1:
            raise self._multiple_isrc_found_error(recording)

        return recording

    def _no_isrc_found_error(self):
        raise ValidationError(
            _("No recording found with the ISRC code {}").format(self.isrc)
        )

    def _multiple_isrc_found_error(self, recordings):
        raise ValidationError(
            _(
                "Found more than one recording with the ISRC code {isrc}:\n\n"
                " * {recordings}"
            ).format(
                isrc=self.isrc,
                recordings="\n * ".join(r.display_name for r in recordings),
            )
        )

    def _map_recording_from_upc(self):
        recording = self.env["recording"].search(
            ["|", ("upc", "=", self.upc), ("upc_packshot", "=", self.upc),]
        )

        if not recording:
            raise self._no_upc_found_error()

        if len(recording) > 1:
            raise self._multiple_upc_found_error(recording)

        return recording

    def _no_upc_found_error(self):
        raise ValidationError(
            _("No recording found with the UPC code {}").format(self.upc)
        )

    def _multiple_upc_found_error(self, recordings):
        raise ValidationError(
            _(
                "Found more than one recording with the UPC code {upc}:\n\n"
                " * {recordings}"
            ).format(
                upc=self.upc,
                recordings="\n * ".join(r.display_name for r in recordings),
            )
        )

    def _map_recording_from_catalog_reference(self):
        catalog = self._map_catalog(self.recording_external_catalog)

        references = self.env["musical.catalog.reference"].search(
            [
                ("code", "=", self.recording_external_catalog_reference),
                ("catalog_id", "=", catalog.id),
            ]
        )
        recording = references.mapped("recording_id")

        if not recording:
            raise self._no_recording_found_from_catalog_error(catalog)

        if len(recording) > 1:
            raise self._multiple_recordings_found_from_catalog_error(catalog, recording)

        return recording

    def _no_recording_found_from_catalog_error(self, catalog):
        raise ValidationError(
            _(
                "No recording found with the catalog reference {reference} (Catalog: {catalog})"
            ).format(
                reference=self.recording_external_catalog_reference,
                catalog=catalog.display_name,
            )
        )

    def _multiple_recordings_found_from_catalog_error(self, catalog, recordings):
        raise ValidationError(
            _(
                "Found more than one recording with the catalog reference {reference}"
                "(Catalog: {catalog}):\n\n"
                " * {recordings}"
            ).format(
                reference=self.recording_external_catalog_reference,
                recordings="\n * ".join(p.display_name for p in recordings),
                catalog=catalog.display_name,
            )
        )

    def _map_catalog(self, reference):
        return self.env["recording.external.catalog.mapping"].map(reference)

    def _map_product_from_revenue_type(self):
        if self.revenue_type:
            return self.env["recording.revenue.type.mapping"].map(self.revenue_type)

    def _map_tax(self):
        if self.tax:
            return self.env["recording.tax.mapping"].map(self.company_id, self.tax)
