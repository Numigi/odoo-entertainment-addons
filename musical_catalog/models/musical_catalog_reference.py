# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models

from odoo.exceptions import ValidationError


class MusicalCatalogReference(models.Model):

    _name = 'musical.catalog.reference'
    _description = 'External Catalog References'
    _order = 'sequence'

    sequence = fields.Integer()
    catalog_id = fields.Many2one('musical.catalog', required=True)
    code = fields.Char(required=True)

    @api.constrains("code")
    def _unique_code(self):
        for record in self.filtered(lambda r: r.catalog_id.reference_unique and r.code):
            same_catalog_code_records = self.search(
                [("catalog_id", "=", record.catalog_id.id), ("code", "=", record.code)]
            )
            if len(same_catalog_code_records) > 1:
                raise ValidationError(
                    _(
                        "The catalogue reference %s is already used for another "
                        "Recording, Work or Product.\n"
                        "The reference must be unique for this catalog."
                    ) % same_catalog_code_records[:1].code
                )
