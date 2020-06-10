# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields


class RecordingExternalRevenue(models.Model):
    _name = "recording.external.revenue"
    _description = "Recording External Revenue"
    _inherit = 'recording.external.revenue.abstract'

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
    tax_id = fields.Many2one('account.tax', ondelete='restrict')

    raw_revenue_ids = fields.One2many(
        "recording.external.revenue.raw",
        "revenue_id",
        "Raw Data Lines",
    )
    raw_revenue_count = fields.Integer(compute="_compute_raw_revenue_count")

    def _compute_raw_revenue_count(self):
        for line in self:
            line.raw_revenue_count = len(line.raw_revenue_ids)
