# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    ticket_ids = fields.One2many(
        comodel_name="show.ticket.sold", inverse_name="show_id"
    )

    @api.multi
    def _update_new_sold_tickets(self):
        for project in self:
            total_sold_tickets_previous = 0
            for ticket in project.ticket_ids:
                ticket.with_context(
                    skip_update_new_sold_tickets=True
                ).new_sold_tickets = (
                    ticket.total_sold_tickets - total_sold_tickets_previous
                )
                total_sold_tickets_previous = ticket.total_sold_tickets
