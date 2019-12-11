# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[('show_site', 'Show site')])
    show_place_type_id = fields.Many2one('show.place.type', string="Place type")
    show_place_configuration_id = fields.Many2one('show.place.configuration', string="Configuration")
    maximum_capacity = fields.Integer(string="Maximum capacity")
    notes = fields.Text(string="Notes")
    linked_product_id = fields.Many2one('product.product', 'Linked Product', domain=[('type', '=', 'service')])
    minor_restriction = fields.Boolean(string="Minor restriction")
