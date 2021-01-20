# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta
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

    @api.multi
    def _update_new_sold_tickets(self):
        for ticket in self:
            previous_tickets_sold = \
                self.search([
                    ('record_date', '=', fields.Date.to_string(ticket.record_date + relativedelta(days=-1))),
                    ('show_id', '=', ticket.show_id.id)
                ])
            new_sold_tickets = ticket.total_sold_tickets - sum(previous_tickets_sold.mapped("total_sold_tickets"))
            ticket.with_context(update_new_sold_tickets=True).write({"new_sold_tickets": new_sold_tickets})

    @api.model
    def create(self, vals):
        res = super(ShowTicketSold, self).create(vals)
        res._update_new_sold_tickets()
        return res

    @api.multi
    def write(self, vals):
        res = super(ShowTicketSold, self).write(vals)
        if not self._context.get("update_new_sold_tickets", False):
            # Update record of next day of current modified record.
            show_tickets = self
            for ticket in self:
                next_date_tickets_sold = \
                    self.search([
                        ('show_id', '=', ticket.show_id.id),
                        ('record_date', '=', fields.Date.to_string(
                            ticket.record_date + relativedelta(days=1))),
                    ])
                show_tickets |= next_date_tickets_sold
            show_tickets._update_new_sold_tickets()
        return res
