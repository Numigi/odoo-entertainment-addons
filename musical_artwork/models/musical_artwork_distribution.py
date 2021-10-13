# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare

decimal_precision = (12, 3)


class MusicalArtworkDistributionLine(models.Model):
    _name = "musical.artwork.distribution.line"
    _description = "Musical Artwork Distribution Line"
    _order = "sequence"

    sequence = fields.Integer()
    partner_id = fields.Many2one(
        "res.partner",
        ondelete="restrict",
        required=True,
    )
    role_id = fields.Many2one(
        "musical.artwork.role",
        ondelete="restrict",
        required=True,
    )
    percentage = fields.Float(
        "%",
        digits=decimal_precision,
        required=True,
    )
    is_managed = fields.Boolean("Managed", default=True)
    distribution_id = fields.Many2one(
        "musical.artwork.distribution", required=True, ondelete="cascade", index=True
    )
    artwork_id = fields.Many2one(
        related="distribution_id.musical_artwork_id",
        store=True,
        string="Artwork",
    )


class MusicalArtworkDistribution(models.Model):
    _name = "musical.artwork.distribution"
    _description = "Musical Artwork Distribution"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    active = fields.Boolean(
        default=True,
        track_visibility="onchange",
    )

    name = fields.Char(
        readonly=True,
        string="Reference",
        track_visibility="onchange",
    )

    musical_artwork_id = fields.Many2one(
        "musical.artwork",
        required=True,
        ondelete="restrict",
        index=True,
        track_visibility="onchange",
    )
    country_group_id = fields.Many2one(
        "res.country.group",
        ondelete="restrict",
        track_visibility="onchange",
    )
    line_ids = fields.One2many(
        "musical.artwork.distribution.line",
        "distribution_id",
        copy=True,
    )

    total_distribution_key = fields.Float(
        "Distribution Key Total",
        digits=decimal_precision,
        readonly=True,
        store=True,
        compute="_compute_total_distribution_key",
    )

    @api.depends("line_ids.percentage")
    def _compute_total_distribution_key(self):
        for record in self:
            record.total_distribution_key = sum(record.line_ids.mapped("percentage"))

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.name = self.env["ir.sequence"].next_by_code(self._name)
        return record

    @api.constrains("total_distribution_key")
    def _check_total_distribution_key(self):
        for record in self:
            if float_compare(record.total_distribution_key, 100, 3):
                raise ValidationError(
                    _(
                        "The sum of the distribution key lines is not equal to 100. "
                        "The distribution key must have a total of 100%."
                    )
                )


class MusicalArtworkDistributionTrackedLines(models.Model):

    _inherit = "musical.artwork.distribution"

    distribution_table_html = fields.Html(
        compute="_compute_distribution_table_html",
    )

    def _compute_distribution_table_html(self):
        table_html_template = self.env.ref(
            "musical_artwork.distribution_table_html_template"
        )
        for distribution in self:
            distribution.distribution_table_html = table_html_template.render(
                {
                    "distribution": distribution,
                }
            )

    @api.model
    def create(self, vals):
        distribution = super().create(vals)
        distribution._log_initial_distribution()
        return distribution

    @api.multi
    def write(self, vals):
        super().write(vals)
        if "line_ids" in vals:
            for line in self:
                line._log_new_distribution()
        return True

    def _log_initial_distribution(self):
        message_template = self.env.ref(
            "musical_artwork.initial_distribution_message_template"
        )
        self._log_distribution_table_html(message_template)

    def _log_new_distribution(self):
        message_template = self.env.ref(
            "musical_artwork.new_distribution_message_template"
        )
        self._log_distribution_table_html(message_template)

    def _log_distribution_table_html(self, message_template):
        message_body = message_template.render(
            {
                "distribution": self,
            }
        )
        self.message_post(body=message_body)
