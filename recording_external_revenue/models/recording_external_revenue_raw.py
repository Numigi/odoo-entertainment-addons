# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from odoo.tools import float_round


class RecordingExternalRevenueRaw(models.Model):
    _name = "recording.external.revenue.raw"
    _description = "Recording External Revenue Raw"
    _inherit = "recording.external.revenue.abstract"

    partner = fields.Char(index=True, required=True)
    country = fields.Char(index=True, required=True)
    state = fields.Char()
    platform = fields.Char(index=True, required=True)
    subplatform = fields.Char()
    is_converted = fields.Boolean(
        "Converted", default=False, readonly=True, index=True, copy=False
    )
    revenue_type = fields.Char(index=True, required=True)

    isrc = fields.Char("ISRC", index=True)
    upc = fields.Char("UPC", index=True)
    recording_external_catalog = fields.Char(index=True)
    recording_external_catalog_reference = fields.Char(index=True)
    title = fields.Char()
    artist = fields.Char()

    product_reference = fields.Char(index=True)
    product_external_catalog = fields.Char(index=True)
    product_external_catalog_reference = fields.Char(index=True)

    revenue_id = fields.Many2one(
        "recording.external.revenue", readonly=True, copy=False
    )
    currency = fields.Char(index=True, required=True)
    tax = fields.Char()

    @api.multi
    def write(self, vals):
        self._check_can_edit_fields(vals)
        return super().write(vals)

    @api.multi
    def unlink(self):
        self._check_can_unlink()
        return super().unlink()

    def _check_can_edit_fields(self, vals):
        fields_to_check = self._get_fields_protected_after_conversion()
        converted_revenues = self.filtered("is_converted")
        if converted_revenues and fields_to_check.intersection(vals):
            raise ValidationError(
                _(
                    "The following raw revenue lines can not be edited because "
                    "these are already converted into revenues:\n"
                    "{}"
                ).format(", ".join(converted_revenues.mapped("display_name")))
            )

    def _get_fields_protected_after_conversion(self):
        result = set(self.get_direct_mapping_fields())
        result.update(self.get_aggregated_fields())
        result.update(self.get_common_parameter_fields())
        return result

    def _check_can_unlink(self):
        converted_revenues = self.filtered("is_converted")
        if converted_revenues:
            raise ValidationError(
                _(
                    "The following raw revenue lines can not be deleted because "
                    "these are already converted into revenues:\n"
                    "{}"
                ).format(", ".join(converted_revenues.mapped("display_name")))
            )

    def schedule_conversion(self, company):
        revenues_to_convert = self.search([("is_converted", "=", False)]).filtered(
            lambda r: r.company_id == company
        )
        for revenues in revenues_to_convert.group_by_common_parameters():
            revenues.with_delay().convert()

    def group_by_common_parameters(self):
        fields = self.get_common_parameter_fields()

        def groupby_func(record):
            return tuple(record[f] for f in fields)

        result = {}

        for record in self:
            key = groupby_func(record)
            if key in result:
                result[key] |= record
            else:
                result[key] = record

        return result.values()

    def get_common_parameter_fields(self):
        return [
            "country",
            "currency",
            "fiscal_position",
            "isrc",
            "operation_date",
            "partner",
            "platform",
            "product_external_catalog",
            "product_external_catalog_reference",
            "product_reference",
            "recording_external_catalog",
            "recording_external_catalog_reference",
            "revenue_type",
            "state",
            "subplatform",
            "tax",
            "tax_base",
            "upc",
            "gross_amount_per_unit",
        ]

    def convert(self):
        self._check_not_already_converted()
        new_revenue = self.make_new_revenue()
        revenue = self.env["recording.external.revenue"].create(
            dict(new_revenue._cache)
        )
        self.write({"revenue_id": revenue.id, "is_converted": True})
        return revenue

    def _check_not_already_converted(self):
        for raw_revenue in self:
            if raw_revenue.is_converted:
                raise ValidationError(
                    _(
                        "The raw revenue {} is already converted. "
                        "It can not be converted twice."
                    ).format(raw_revenue.display_name)
                )

    def make_new_revenue(self):
        revenue = self.env["recording.external.revenue"].new()
        self[0]._execute_direct_mapping(revenue)
        self[0]._execute_advanced_mapping(revenue)
        self._execute_aggregated_fields_mapping(revenue)
        return revenue

    def _execute_direct_mapping(self, revenue):
        for field in self.get_direct_mapping_fields():
            revenue[field] = self[field]

    def get_direct_mapping_fields(self):
        return [
            "company_id",
            "fiscal_position",
            "gross_amount_per_unit",
            "operation_date",
            "period_end_date",
            "period_start_date",
            "quantity",
            "tax_base",
        ]

    def _execute_aggregated_fields_mapping(self, revenue):
        aggregated_fields = self.get_aggregated_fields()
        for field in aggregated_fields:
            revenue[field] = float_round(sum(r[field] or 0 for r in self),
                                         precision_digits=2)

    def get_aggregated_fields(self):
        return ["commission_amount", "gross_amount", "net_amount", "quantity"]

    def _execute_advanced_mapping(self, revenue):
        revenue.partner_id = self._map_partner()
        revenue.country_id = self._map_country()
        revenue.state_id = self._map_country_state()
        revenue.platform_id = self._map_platform()
        revenue.subplatform_id = self._map_subplatform()
        revenue.product_id = self._map_product()
        revenue.recording_id = self._map_recording(revenue.product_id)
        revenue.tax_id = self._map_tax()
        revenue.currency_id = self._map_currency()
        revenue.analytic_account_id = self._map_analytic_account(revenue.recording_id)
        revenue.artist_id = revenue.recording_id.artist_id

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
            return self.env["recording.subplatform.mapping"].map(
                platform, self.subplatform
            )

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

        if not product.recording_id:
            raise self._no_recording_related_to_product(product)

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

        if not product.recording_id:
            raise self._no_recording_related_to_product(product)

        return product

    def _no_recording_related_to_product(self, product):
        return ValidationError(
            _("The product {} is not related to a recording.").format(
                product.display_name
            )
        )

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

    def _map_recording(self, product):
        if product.recording_id:
            return product.recording_id

        if self.isrc:
            return self._map_recording_from_isrc()

        if self.upc:
            return self._map_recording_from_upc()

        if (
            self.recording_external_catalog
            and self.recording_external_catalog_reference
        ):
            return self._map_recording_from_catalog_reference()

    def _map_recording_from_isrc(self):
        recording = self.env["recording"].search(
            ["|", ("isrc", "=", self.isrc), ("other_isrc_ids.isrc", "=", self.isrc)]
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
            ["|", ("upc", "=", self.upc), ("upc_packshot", "=", self.upc)]
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

    def _map_analytic_account(self, recording):
        if recording and not recording.analytic_account_id:
            raise ValidationError(
                _("The recording {} has no analytic account.").format(
                    recording.display_name
                )
            )
        return recording.analytic_account_id
