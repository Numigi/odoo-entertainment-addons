# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    show_hour = fields.Float(string="Show Time")
    show_duration = fields.Char()
    door_hour = fields.Float(string="Door Time")
    artist_start_hour = fields.Float(string="Artist Start Time")
    other_artists = fields.Char()
    has_intermission = fields.Boolean("Intermission")
    has_accomodation = fields.Boolean("Accomodation")
    accomodation = fields.Char()
    has_meal = fields.Boolean("Meals")
    meals = fields.Char()
    artist_favour_tickets = fields.Integer("Artist's Favour Tickets")
    diffisor_favour_tickets = fields.Integer("Diffusor's Favor Tickets")
    selling_date = fields.Date()
    ticket_price_ids = fields.One2many(
        "project.ticket.price",
        "project_id",
        "Ticket Prices",
    )
    service_fee_ids = fields.One2many(
        "project.service.fee",
        "project_id",
        "Service Fees",
    )
    has_benefits_sharing = fields.Boolean("Benefits Sharing")
    benefits_sharing_rate = fields.Float("Applicable Rate (%)", digits=(3, 2))
    benefits_sharing_type = fields.Selection(
        [
            ("after_fixed_amount", "After Fixed Expense Amount"),
            ("after_real_costs", "After Real Costs"),
        ],
        "Type of Sharing",
    )
    benefits_sharing_amount_before = fields.Monetary(
        "Expenses Amount Before Sharing",
        currency_field="sale_currency_id",
    )
    benefits_sharing_forcasted_expense = fields.Monetary(
        "Forecasted Expenses Amount",
        currency_field="sale_currency_id",
    )
    sale_currency_id = fields.Many2one(
        related="show_sale_order_ids.pricelist_id.currency_id",
    )
    sales_note = fields.Text(string="Notes")
    other_contract_terms = fields.Text(string="Other terms of the contract")

