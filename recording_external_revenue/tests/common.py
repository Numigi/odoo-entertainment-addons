# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo.tests.common import SavepointCase


class ExternalRevenueCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cad = cls.env.ref("base.CAD")
        cls.cad_mapping = cls.env.ref("recording_external_revenue.demo_mapping_cad")
        cls.eur = cls.env.ref("base.EUR")

        cls.company = cls.env["res.company"].create({"name": "New Company"})
        cls.company.currency_id = cls.cad

        cls.believe = cls.env.ref("recording_external_revenue.demo_partner_believe")
        cls.believe_mapping = cls.env.ref("recording_external_revenue.demo_mapping_blv")
        cls.canada = cls.env.ref("base.ca")
        cls.canada_mapping = cls.env.ref("recording_external_revenue.demo_mapping_ca")
        cls.quebec = cls.env.ref("base.state_ca_qc")
        cls.quebec_mapping = cls.env.ref("recording_external_revenue.demo_mapping_qc")
        cls.spotify = cls.env.ref("recording_platform.spotify")
        cls.spotify_mapping = cls.env.ref(
            "recording_external_revenue.demo_mapping_spotify"
        )
        cls.spotify_premium = cls.env.ref("recording_platform.spotify_premium")
        cls.spotify_premium_mapping = cls.env.ref(
            "recording_external_revenue.demo_mapping_spotify_premium"
        )

        cls.tax = cls._create_tax(
            name="My Awesome Tax",
            amount=100,
            amount_type="percent",
            company_id=cls.company.id,
        )
        cls.tax_mapping = cls.env["recording.tax.mapping"].create(
            {"label": "AwesomeTax", "tax_id": cls.tax.id}
        )

        cls.stream = cls.env.ref("recording_external_revenue.demo_product_stream")
        cls.stream_mapping = cls.env.ref(
            "recording_external_revenue.demo_mapping_streaming"
        )
        cls.video = cls.env.ref("recording_external_revenue.demo_product_video")
        cls.video_reference = "123VIDEO"
        cls.video.default_code = cls.video_reference

        cls.catalog = cls.env.ref("musical_catalog.apple_music")
        cls.catalog_mapping = cls.env.ref(
            "recording_external_revenue.demo_mapping_apple_music"
        )
        cls.video_catalog_reference = cls.env["musical.catalog.reference"].create(
            {
                "catalog_id": cls.catalog.id,
                "code": "456VIDEO",
                "product_template_id": cls.video.product_tmpl_id.id,
            }
        )

        cls.upc = "639382000393"
        cls.upc_packshot = "811868865980"
        cls.isrc = "USS1Z9900001"
        cls.other_isrc = "USS2A8800002"
        cls.artist = cls.env["artist"].create({"name": "Some Artist"})
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {"name": "My Analytic Account", "company_id": cls.company.id}
        )
        cls.recording = cls.env["recording"].create(
            {
                "name": "Awesome Video",
                "ttype": "video",
                "artist_id": cls.artist.id,
                "upc": cls.upc,
                "upc_packshot": cls.upc_packshot,
                "isrc": cls.isrc,
                "other_isrc_ids": [(0, 0, {"isrc": cls.other_isrc})],
                "analytic_account_id": cls.analytic_account.id,
            }
        )
        cls.video.product_tmpl_id.recording_id = cls.recording
        cls.stream.product_tmpl_id.recording_id = cls.recording
        cls.recording_catalog_reference = cls.env["musical.catalog.reference"].create(
            {
                "catalog_id": cls.catalog.id,
                "code": "789RECORDING",
                "recording_id": cls.recording.id,
            }
        )

    @classmethod
    def _create_tax(cls, **kwargs):
        return cls.env["account.tax"].create(kwargs)

    @classmethod
    def _create_raw_revenue(cls, **kwargs):
        vals = {
            "company_id": cls.company.id,
            "partner": cls.believe_mapping.label,
            "operation_date": datetime.now().date(),
            "period_start_date": datetime.now().date(),
            "period_end_date": datetime.now().date(),
            "country": cls.canada_mapping.label,
            "fiscal_position": "partner",
            "revenue_type": cls.stream_mapping.label,
            "platform": cls.spotify_mapping.label,
            "currency": cls.cad_mapping.label,
            "tax_base": "net_amount",
        }
        vals.update(kwargs)
        return cls.env["recording.external.revenue.raw"].create(vals)
