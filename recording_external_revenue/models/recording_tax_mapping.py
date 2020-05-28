# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class RecordingTaxMapping(models.Model):
    _name = "recording.tax.mapping"
    _description = "Recording Tax Mapping"
    _order = "label"
    _rec_name = "label"

    label = fields.Char(required=True, unique=True, string="Label")
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.user.company_id
    )
    tax_id = fields.Many2one(
        "account.tax",
        ondelete="restrict",
        required=True,
        domain="[('company_id', '=', company_id)]",
    )

    @api.onchange("company_id")
    def _empty_tax_if_not_match_company(self):
        if self.company_id != self.tax_id.company_id:
            self.tax_id = None

    _sql_constraints = [
        (
            "unique_label_and_company",
            "unique (label, company_id)",
            "Only one tax can be mapped per label and company.",
        )
    ]

    @api.model
    def map(self, company, label):
        tax = self.search(
            [("company_id", "=", company.id), ("label", "=", label)]
        ).tax_id
        if not tax:
            raise ValidationError(_(
                "No tax found for the label {}"
            ).format(label))
        return tax
