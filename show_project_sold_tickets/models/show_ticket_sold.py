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
        required=True,
        domain="[('show_type', '=', 'show')]",
    )
    record_date = fields.Date(
        required=True,
    )
    total_sold_tickets = fields.Integer()
    new_sold_tickets = fields.Integer(
        readonly=True,
    )

    _sql_constraints = [
        ("unique_show_id_date",
         "UNIQUE(show_id, record_date)",
         "A record already exists on this date for this show!"),
    ]

    @api.model
    def create(self, vals):
        res = super(ShowTicketSold, self).create(vals)
        res.show_id._update_new_sold_tickets()
        return res

    @api.multi
    def write(self, vals):
        res = super(ShowTicketSold, self).write(vals)
        if not self._context.get("skip_update_new_sold_tickets"):
            self.mapped("show_id")._update_new_sold_tickets()
        return res

    @api.multi
    def unlink(self):
        projects = self.mapped("show_id")
        res = super(ShowTicketSold, self).unlink()
        projects._update_new_sold_tickets()
        return res
