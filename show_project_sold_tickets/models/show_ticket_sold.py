# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ShowTicketSold(models.Model):
    _name = "show.ticket.sold"
    _rec_name = "record_date"
    _order = "record_date"
    _description = "Show Ticket Sold"

    show_id = fields.Many2one(
        comodel_name="project.project",
    )
    record_date = fields.Date(
        required=True,
    )
    total_sold_tickets = fields.Integer()
    new_sold_tickets = fields.Integer(
        readonly=True,
    )

    _sql_constraints = [
        ("record_date_uniq",
         "UNIQUE(show_id, record_date)",
         "A record already exists on this date for this show!"),
    ]

    @api.multi
    def _update_new_sold_tickets(self):
        for ticket in self:
            previous_ticket_sold = \
                self.search([
                    ('record_date', '<', ticket.record_date),
                    ('show_id', '=', ticket.show_id.id)
                ], order = "record_date desc", limit=1)
            new_sold_tickets = ticket.total_sold_tickets - previous_ticket_sold.total_sold_tickets
            ticket.with_context(skip_update_new_sold_tickets=False).write({"new_sold_tickets": new_sold_tickets})

    @api.model
    def create(self, vals):
        res = super(ShowTicketSold, self).create(vals)
        res._update_new_sold_tickets()
        return res

    @api.multi
    def write(self, vals):
        res = super(ShowTicketSold, self).write(vals)
        if self._context.get("skip_update_new_sold_tickets", True):
            # Update record of next day of current modified record.
            show_tickets = self
            for ticket in self:
                next_date_ticket_sold = \
                    self.search([
                        ('show_id', '=', ticket.show_id.id),
                        ('record_date', '>', ticket.record_date),
                    ], order = "record_date", limit=1)
                show_tickets |= next_date_ticket_sold
            show_tickets._update_new_sold_tickets()
        return res
