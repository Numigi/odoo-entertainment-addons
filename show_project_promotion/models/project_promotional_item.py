# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectPromotionalItem(models.Model):

    _name = "project.promotional.item"
    _description = "Project Promotional Item"

    sequence = fields.Integer()
    project_id = fields.Many2one("project.project", required=True, index=True)
    product_id = fields.Many2one("product.product", required=True)
    description = fields.Text(required=True)
    notes = fields.Text()

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.get_product_multiline_description_sale()
