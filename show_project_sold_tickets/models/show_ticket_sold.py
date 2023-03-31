# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


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
    record_date = fields.Date(required=True)
    total_sold_tickets = fields.Integer()
    new_sold_tickets = fields.Integer(readonly=True)
    artist_id = fields.Many2one(
        related="show_id.artist_id", readonly=True, store=True, string="Artist"
    )
    show_parent_id = fields.Many2one(
        related="show_id.parent_id", readonly=True, store=True, string="Tour"
    )
    show_place_id = fields.Many2one(
        related="show_id.show_place_id", readonly=True, store=True, string="Show place"
    )
    city = fields.Char(related="show_id.city", readonly=True, store=True, string="City")
    show_date = fields.Date(
        related="show_id.show_date", readonly=True, store=True, string="Show date"
    )
    show_place_maximum_capacity = fields.Integer(
        related="show_id.show_place_maximum_capacity",
        readonly=True,
        store=True,
        group_operator="avg",
        string="Show place capacity",
    )
    favour_tickets = fields.Integer(
        compute="_compute_favour_tickets",
        store=True,
        group_operator="avg",
        string="Favour Tickets"
    )
    sold_tickets = fields.Float(
        compute="_compute_sold_tickets",
        store=True,
        string="% Sold Tickets",
        group_operator="avg",
        digits=(12, 2),
    )
    last_entry = fields.Boolean(
        string='Last Entry',
        compute='_compute_last_entry',
        store=True
    )

    _sql_constraints = [
        (
            "unique_show_id_date",
            "UNIQUE(show_id, record_date)",
            "A record already exists on this date for this show!",
        )
    ]

    @api.multi
    @api.depends("record_date", "show_id.ticket_ids", "show_id.ticket_ids.record_date")
    def _compute_last_entry(self):
        for t in self:
            ticket_ids = t.show_id.ticket_ids.filtered(lambda st: st.record_date)
            sold_ticket_ids = ticket_ids.sorted('record_date', reverse=True)
            if sold_ticket_ids:
                last_entry = (t.record_date and t.record_date >= sold_ticket_ids[0].record_date) \
                             or False
            else:
                last_entry = True
            t.last_entry = last_entry

    @api.multi
    @api.depends("show_id.artist_favour_tickets", "show_id.diffisor_favour_tickets")
    def _compute_favour_tickets(self):
        for t in self:
            show_id = t.show_id
            t.favour_tickets = (
                    show_id.artist_favour_tickets + show_id.diffisor_favour_tickets
            )

    @api.multi
    @api.depends("show_place_maximum_capacity", "favour_tickets", "total_sold_tickets")
    def _compute_sold_tickets(self):
        for t in self:
            sold_tickets = 0
            salable_tickets = t.show_place_maximum_capacity - t.favour_tickets
            if salable_tickets != 0:
                sold_tickets = t.total_sold_tickets / salable_tickets
            t.sold_tickets = sold_tickets

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.show_id._update_new_sold_tickets()
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if not self._context.get("skip_update_new_sold_tickets"):
            self.mapped("show_id")._update_new_sold_tickets()
        return res

    @api.multi
    def unlink(self):
        projects = self.mapped("show_id")
        res = super().unlink()
        projects._update_new_sold_tickets()
        return res
