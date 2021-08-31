# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    is_show = fields.Boolean("Is Show", related="type_id.is_show", store=True)

    artist_id = fields.Many2one("artist", ondelete="restrict")
    show_project_id = fields.Many2one(
        "project.project", "Show", ondelete="restrict",
    )

    other_artists = fields.Text()
    has_first_part = fields.Boolean()
    first_part = fields.Char()

    artist_favour_tickets = fields.Integer("Artist's Favour Tickets")
    announcement_date = fields.Date()
    selling_date = fields.Date()
    ticket_price_ids = fields.One2many(
        "sale.order.ticket.price",
        "order_id",
        "Ticket Prices",
    )
    service_fee_ids = fields.One2many(
        "sale.order.service.fee",
        "order_id",
        "Service Fees",
    )
    show_date = fields.Date()
    show_hour = fields.Float()
    show_duration = fields.Float()
    door_hour = fields.Float()
    artist_start_hour = fields.Float()
    show_notes = fields.Text()

    show_place_id = fields.Many2one(
        related="show_project_id.show_place_id", string="Show Location", store=True,
    )
    show_place_maximum_capacity = fields.Integer(
        "Show Location Capacity",
        related="show_project_id.show_place_maximum_capacity", store=True,
    )

    has_intermission = fields.Boolean("Intermission")

    has_accomodation = fields.Boolean()
    accomodation = fields.Char()

    has_meal = fields.Boolean()
    meal = fields.Char()

    has_benefits_sharing = fields.Boolean("Benefits Sharing")
    benefits_sharing_rate = fields.Float()
    benefits_sharing_type = fields.Selection(
        [
            ("after_fixed_amount", "After Fixed Expense Amount"),
            ("after_real_costs", "After Real Costs"),
        ],
    )
    benefits_sharing_amount_before = fields.Monetary(
        "Expense Amount Before Sharing",
    )
    benefits_sharing_forcasted_expense = fields.Monetary(
        "Forecasted Expenses Amount",
    )

    @api.onchange("show_place_id")
    def onchange_show_place(self):
        self.show_place_maximum_capacity = self.show_place_id.show_place_maximum_capacity

    @api.onchange("show_project_id")
    def onchange_show_project(self):
        self.analytic_account_id = self.show_project_id.analytic_account_id
