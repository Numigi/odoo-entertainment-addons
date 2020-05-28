# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class RecordingExternalCatalogMapping(models.Model):
    _name = "recording.external.catalog.mapping"
    _description = "Recording External Catalog Mapping"
    _order = "label"
    _rec_name = "label"

    label = fields.Char(required=True, unique=True, string="Label")
    catalog_id = fields.Many2one("musical.catalog", ondelete="restrict", required=True)

    _sql_constraints = [
        (
            "unique_label",
            "unique (label)",
            "Only one external catalog can be mapped per label.",
        )
    ]

    @api.model
    def map(self, label):
        catalog = self.search([("label", "=", label)]).catalog_id
        if not catalog:
            raise ValidationError(
                _("No external catalog found for the label {}").format(label)
            )
        return catalog
