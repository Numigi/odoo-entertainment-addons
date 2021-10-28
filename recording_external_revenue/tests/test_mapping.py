# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime, timedelta
from ddt import ddt, data
from odoo.exceptions import ValidationError
from .common import ExternalRevenueCase


@ddt
class TestRawRevenueMapping(ExternalRevenueCase):
    def _new_raw_revenue(self, **kwargs):
        return self.env["recording.external.revenue.raw"].new(kwargs)

    def test_map_partner(self):
        raw_revenue = self._new_raw_revenue(partner=self.believe_mapping.label)
        assert raw_revenue.make_new_revenue().partner_id == self.believe

    def test_partner_not_found(self):
        raw_revenue = self._new_raw_revenue(partner="Wrong Label")
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_map_country(self):
        raw_revenue = self._new_raw_revenue(country=self.canada_mapping.label)
        assert raw_revenue.make_new_revenue().country_id == self.canada

    def test_country_not_found(self):
        raw_revenue = self._new_raw_revenue(country="Wrong Label")
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_map_country_state(self):
        raw_revenue = self._new_raw_revenue(
            country=self.canada_mapping.label, state=self.quebec_mapping.label
        )
        assert raw_revenue.make_new_revenue().state_id == self.quebec

    def test_country_state_not_found(self):
        raw_revenue = self._new_raw_revenue(
            country=self.canada_mapping.label, state="Wrong Label"
        )
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_map_platform(self):
        raw_revenue = self._new_raw_revenue(platform=self.spotify_mapping.label)
        assert raw_revenue.make_new_revenue().platform_id == self.spotify

    def test_platform_not_found(self):
        raw_revenue = self._new_raw_revenue(platform="Wrong Label")
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_map_subplatform(self):
        raw_revenue = self._new_raw_revenue(
            platform=self.spotify_mapping.label,
            subplatform=self.spotify_premium_mapping.label,
        )
        assert raw_revenue.make_new_revenue().subplatform_id == self.spotify_premium

    def test_subplatform_not_found(self):
        raw_revenue = self._new_raw_revenue(
            platform=self.spotify_mapping.label, subplatform="Wrong Label"
        )
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_map_tax_mapping(self):
        raw_revenue = self._new_raw_revenue(
            company_id=self.tax_mapping.company_id.id, tax=self.tax_mapping.label
        )
        assert raw_revenue.make_new_revenue().tax_id == self.tax

    def test_tax_not_found(self):
        raw_revenue = self._new_raw_revenue(
            company_id=self.tax_mapping.company_id.id, tax="Wrong Label"
        )
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_map_currency(self):
        raw_revenue = self._new_raw_revenue(currency=self.cad_mapping.label)
        assert raw_revenue.make_new_revenue().currency_id == self.cad

    def test_currency_not_found(self):
        raw_revenue = self._new_raw_revenue(currency="Wrong Label")
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    @data(
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
    )
    def test_direct_mapping(self, field):
        today = datetime.now().date()
        raw_revenue = self._new_raw_revenue(
            operation_date=today + timedelta(10),
            period_start_date=today + timedelta(5),
            period_end_date=today + timedelta(15),
            tax_base="net_amount",
            quantity=10,
            gross_amount_per_unit=20,
            gross_amount=300,
            commission_amount=200,
            net_amount=100,
            fiscal_position="partner",
        )
        revenue = raw_revenue.make_new_revenue()
        assert revenue[field] == raw_revenue[field]

    def test_map_revenue_type(self):
        self.stream.product_tmpl_id.recording_id = False
        raw_revenue = self._new_raw_revenue(revenue_type=self.stream_mapping.label)
        assert raw_revenue.make_new_revenue().product_id == self.stream

    def test_no_product_found_for_revenue_type(self):
        raw_revenue = self._new_raw_revenue(revenue_type="unexisting reference")
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_product_reference_has_priority_over_revenue_type(self):
        stream_mapping = self.env.ref(
            "recording_external_revenue.demo_mapping_streaming"
        )
        raw_revenue = self._new_raw_revenue(
            product_reference=self.video.default_code, revenue_type=stream_mapping.label
        )
        assert raw_revenue.make_new_revenue().product_id == self.video

    def test_no_product_found_with_reference(self):
        raw_revenue = self._new_raw_revenue(product_reference="unexisting reference")
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_2_products_with_same_reference(self):
        self.video.copy({"default_code": self.video.default_code})
        raw_revenue = self._new_raw_revenue(product_reference=self.video.default_code)
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_map_product_using_catalog_reference(self):
        raw_revenue = self._new_raw_revenue(
            product_external_catalog=self.catalog_mapping.label,
            product_external_catalog_reference=self.video_catalog_reference.code,
        )
        revenue = raw_revenue.make_new_revenue()
        assert revenue.product_id == self.video
        assert revenue.recording_id == self.recording

    def test_no_product_found_with_catalog_reference(self):
        raw_revenue = self._new_raw_revenue(
            product_external_catalog=self.catalog_mapping.label,
            product_external_catalog_reference="unexisting reference",
        )
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_2_products_with_same_catalog_reference(self):
        self.video.copy({"product_tmpl_id": self.video.product_tmpl_id.id})
        raw_revenue = self._new_raw_revenue(
            product_external_catalog=self.catalog_mapping.label,
            product_external_catalog_reference=self.video_catalog_reference.code,
        )
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_product_with_no_related_recording(self):
        raw_revenue = self._new_raw_revenue(
            product_external_catalog=self.catalog_mapping.label,
            product_external_catalog_reference=self.video_catalog_reference.code,
        )
        self.video.product_tmpl_id.recording_id = False
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_catalog_not_found(self):
        raw_revenue = self._new_raw_revenue(
            product_external_catalog="unexisting reference",
            product_external_catalog_reference=self.video_catalog_reference.code,
        )
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_map_recording_from_upc(self):
        raw_revenue = self._new_raw_revenue(upc=self.upc)
        assert raw_revenue.make_new_revenue().recording_id == self.recording

    def test_map_recording_from_upc_packshot(self):
        raw_revenue = self._new_raw_revenue(upc=self.upc_packshot)
        assert raw_revenue.make_new_revenue().recording_id == self.recording

    def test_recording_not_found_with_upc(self):
        raw_revenue = self._new_raw_revenue(upc="wrong-upc-code")
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_map_recording_from_isrc(self):
        raw_revenue = self._new_raw_revenue(isrc=self.isrc)
        assert raw_revenue.make_new_revenue().recording_id == self.recording

    def test_map_recording_from_other_isrc(self):
        raw_revenue = self._new_raw_revenue(isrc=self.other_isrc)
        assert raw_revenue.make_new_revenue().recording_id == self.recording

    def test_recording_not_found_with_isrc(self):
        raw_revenue = self._new_raw_revenue(isrc="wrong-isrc-code")
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_map_recording_using_catalog_reference(self):
        raw_revenue = self._new_raw_revenue(
            recording_external_catalog=self.catalog_mapping.label,
            recording_external_catalog_reference=self.recording_catalog_reference.code,
        )
        assert raw_revenue.make_new_revenue().recording_id == self.recording

    def test_no_recording_found_with_catalog_reference(self):
        raw_revenue = self._new_raw_revenue(
            recording_external_catalog=self.catalog_mapping.label,
            recording_external_catalog_reference="unexisting reference",
        )
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_2_recordings_with_same_catalog_reference(self):
        new_recording = self.recording.copy()
        self.recording_catalog_reference.copy({"recording_id": new_recording.id})
        raw_revenue = self._new_raw_revenue(
            recording_external_catalog=self.catalog_mapping.label,
            recording_external_catalog_reference=self.recording_catalog_reference.code,
        )
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_analytic_account_taken_from_recording(self):
        raw_revenue = self._new_raw_revenue(isrc=self.isrc)
        revenue = raw_revenue.make_new_revenue()
        assert revenue.analytic_account_id == self.analytic_account

    def test_if_no_analytic_account__raise_error(self):
        self.recording.analytic_account_id = False
        raw_revenue = self._new_raw_revenue(isrc=self.isrc)
        with pytest.raises(ValidationError):
            raw_revenue.make_new_revenue()

    def test_artist_taken_from_recording(self):
        self.recording.artist_id = self.artist
        raw_revenue = self._new_raw_revenue(isrc=self.isrc)
        revenue = raw_revenue.make_new_revenue()
        assert revenue.artist_id == self.artist
