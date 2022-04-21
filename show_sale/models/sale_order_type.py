# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrderType(models.Model):

    _inherit = "sale.order.type"

    is_show = fields.Boolean(
        "Show", help="Adds a tab Show on the sale order that allows to manage show settings."
    )
