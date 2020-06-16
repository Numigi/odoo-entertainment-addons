# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields


class RecordingExternalRevenue(models.Model):
    _name = "recording.external.revenue"
    _description = "Recording External Revenue"
    _inherit = "recording.external.revenue.abstract"

    product_id = fields.Many2one("product.product", ondelete="restrict")
    partner_id = fields.Many2one("res.partner", ondelete="restrict")
    platform_id = fields.Many2one("recording.platform", ondelete="restrict")
    subplatform_id = fields.Many2one(
        "recording.subplatform",
        ondelete="restrict",
        domain="[('platform_id', '=', platform_id)]",
    )
    country_id = fields.Many2one("res.country", ondelete="restrict")
    state_id = fields.Many2one(
        "res.country.state",
        ondelete="restrict",
        domain="[('country_id', '=', country_id)]",
    )
    currency_id = fields.Many2one("res.currency", ondelete="restrict")
    recording_id = fields.Many2one("recording", ondelete="restrict")
    artist_id = fields.Many2one("artist", ondelete="restrict")
    analytic_account_id = fields.Many2one(
        "account.analytic.account", ondelete="restrict"
    )
    tax_id = fields.Many2one("account.tax", ondelete="restrict")

    raw_revenue_ids = fields.One2many(
        "recording.external.revenue.raw", "revenue_id", "Raw Data Lines"
    )
    raw_revenue_count = fields.Integer(compute="_compute_raw_revenue_count")

    def _compute_raw_revenue_count(self):
        for line in self:
            line.raw_revenue_count = len(line.raw_revenue_ids)

    @api.onchange("product_id")
    def _onchange_product_propagate_recording(self):
        self.recording_id = self.product_id.recording_id

    @api.onchange("recording_id")
    def _onchange_recording_propagate_artist(self):
        self.artist_id = self.recording_id.artist_id

    @api.onchange("platform_id")
    def _onchange_platform_empty_subplatform(self):
        if self.subplatform_id.platform_id != self.platform_id:
            self.subplatform_id = False

    @api.onchange("country_id")
    def _onchange_country_empty_state(self):
        if self.state_id.country_id != self.country_id:
            self.state_id = False
