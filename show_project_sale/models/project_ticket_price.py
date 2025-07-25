# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectTicketPrice(models.Model):

    _name = "project.ticket.price"
    _inherit = "project.price.mixin"
    _description = "Project Ticket Price"
