# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class RecordingExternalCatalogMapping(models.Model):
    _name = "recording.external.catalog.mapping"
    _description = "Recording External Catalog Mapping"
    _order = "label"
    _rec_name = "label"

    label = fields.Char(required=True, unique=True, string="Label")
    catalog_id = fields.Many2one("musical.catalog", ondelete="restrict", required=True)

    _sql_constraints = [
        ("unique_label", "unique (label)", "Only one external catalog can be mapped per label.")
    ]
