# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, _
from odoo.addons.queue_job.job import job
from odoo.exceptions import ValidationError


class RecordingExternalRevenue(models.Model):

    _inherit = "recording.external.revenue"

    is_posted = fields.Boolean(readonly=True)

    def schedule_generate_journal_entries(self, company):
        revenues_to_post = self.search([("is_posted", "=", False)]).filtered(
            lambda r: r.company_id == company
        )
        for revenues in revenues_to_post:
            revenues.with_delay().generate_journal_entry()

    @job
    def generate_journal_entry(self):
        self = self.with_context(force_company=self.company_id.id)

        with self.env.do_in_onchange():
            move = self._make_new_journal_entry()

        move_vals = dict(move._cache)
        move_vals["line_ids"] = [(0, 0, line._cache) for line in move.line_ids]
        move = self.env["account.move"].create(move_vals)
        move.post()
        return move

    def _make_new_journal_entry(self):
        move = self.env["account.move"].new(
            {
                "company_id": self.company_id.id,
                "journal_id": self._map_journal().id,
                "date": self.operation_date,
            }
        )

        revenue_line = self._make_new_revenue_move_line()
        move.line_ids = revenue_line

        self._set_tax_base_amount(revenue_line)
        self._add_tax_move_lines(move)
        self._set_revenue_amount(revenue_line)
        self._add_receivable_move_line(move)

        self._check_no_deprecated_journal_account(move)

        return move

    def _add_tax_move_lines(self, move):
        move._onchange_line_ids()

    def _add_receivable_move_line(self, move):
        receivable_amount = sum(-l.balance for l in move.line_ids)
        move.line_ids |= self._make_receivable_lines(receivable_amount)

    def _map_journal(self):
        return self.env["recording.journal.mapping"].map(
            self.company_id, self.currency_id
        )

    def _make_new_revenue_move_line(self):
        line = self.env["account.move.line"].new()
        line.name = "/"
        line.account_id = self._get_map_revenue_account()
        line.product_id = self.product_id
        line.product_uom_id = self.product_id.uom_id
        line.quantity = self.quantity
        line.recompute_tax_line = True
        line.tax_ids = self._get_revenue_line_taxes()
        line.analytic_account_id = self.analytic_account_id
        if not self._is_revenue_in_company_currency:
            line.currency_id = self.currency_id
        return line

    def _get_revenue_line_taxes(self):
        if self.tax_id:
            return self.tax_id

        taxes = self._get_taxes_from_product() or self._get_taxes_from_revenue_account()
        taxes = taxes.filtered(lambda t: t.company_id == self.company_id)
        fiscal_position = self._map_fiscal_position()
        if fiscal_position:
            taxes = fiscal_position.map_tax(taxes)
        return taxes

    def _map_fiscal_position(self):
        if self.fiscal_position == "revenue":
            return self._get_fiscal_position_from_revenue()
        elif self.fiscal_position == "partner":
            return self._get_fiscal_position_from_partner()

    def _get_fiscal_position_from_revenue(self):
        position_pool = self._get_fiscal_position_pool()
        position = position_pool._get_fpos_by_region(
            self.country_id.id, self.state_id.id
        )
        if not position:
            raise ValidationError(
                _(
                    "No fiscal position defined for the country {}, nor for a group of countries "
                    "containing this country."
                ).format(self.country_id.display_name)
            )
        return position

    def _get_fiscal_position_from_partner(self):
        position_pool = self._get_fiscal_position_pool()
        position_id = position_pool.get_fiscal_position(self.partner_id.id)
        position = position_pool.browse(position_id)
        if not position:
            raise ValidationError(
                _(
                    "The revenue indicates that the fiscal position from "
                    "the partner is applicable. "
                    "No fiscal position is defined for the partner {}."
                ).format(self.partner_id.display_name)
            )
        return position

    def _get_fiscal_position_pool(self):
        return self.env["account.fiscal.position"]

    def _get_taxes_from_product(self):
        return self.product_id.taxes_id

    def _get_taxes_from_revenue_account(self):
        revenue_account = self._get_map_revenue_account()
        return revenue_account.tax_ids

    def _set_tax_base_amount(self, revenue_line):
        amount = self[self.tax_base]
        self._set_move_line_credit(revenue_line, amount)

    def _set_revenue_amount(self, revenue_line):
        amount = self.net_amount
        self._set_move_line_credit(revenue_line, amount)

    def _set_move_line_credit(self, move_line, amount):
        if self._is_revenue_in_company_currency:
            move_line.debit = -amount if amount < 0 else 0
            move_line.credit = amount if amount > 0 else 0
            move_line.amount_currency = 0
        else:
            amount_company_currency = self._convert_amount_in_company_currency(amount)
            move_line.debit = -amount_company_currency if amount < 0 else 0
            move_line.credit = amount_company_currency if amount > 0 else 0
            move_line.amount_currency = -amount

    def _convert_amount_in_company_currency(self, amount):
        return self.currency_id._convert(
            amount, self._company_currency, self.company_id, self.operation_date,
        )

    @property
    def _is_revenue_in_company_currency(self):
        return self.currency_id == self._company_currency

    @property
    def _company_currency(self):
        return self.company_id.currency_id

    def _get_map_revenue_account(self):
        product_template = self.product_id.product_tmpl_id
        account = product_template.get_product_accounts().get("income")
        if not account:
            raise ValidationError(
                _("There is no revenue account defined for the product {}.").format(
                    self.product_id.display_name
                )
            )

        fiscal_position = self._map_fiscal_position()
        if fiscal_position:
            account = fiscal_position.map_account(account)

        return account

    def _make_receivable_lines(self, amount):
        payment_term = self._map_payment_term()

        if payment_term:
            return self._make_receivable_lines_from_payment_term(amount, payment_term)
        else:
            return self._make_single_receivable_move_line(amount, self.period_end_date)

    def _make_receivable_lines_from_payment_term(self, total_amount, payment_term):
        payment_term = payment_term.with_context(currency_id=self.currency_id.id)
        invoice_date = self.period_end_date
        result = self.env["account.move.line"]

        due_amount_list = payment_term.compute(total_amount, invoice_date)[0]

        for due_date, amount in due_amount_list:
            result |= self._make_single_receivable_move_line(amount, due_date)
        return result

    def _make_single_receivable_move_line(self, amount, due_date):
        line = self.env["account.move.line"].new()
        line.name = "/"
        line.account_id = self._map_receivable_account()
        line.debit = amount if amount > 0 else 0
        line.credit = -amount if amount < 0 else 0
        line.currency_id = line.account_id.currency_id
        line.date_maturity = due_date
        return line

    def _map_receivable_account(self):
        return self.partner_id.property_account_receivable_id

    def _map_payment_term(self):
        return self.partner_id.property_payment_term_id

    def _check_no_deprecated_journal_account(self, move):
        accounts = (l.account_id for l in move.line_ids)
        deprecated_account = next((a for a in accounts if a.deprecated), None)
        if deprecated_account:
            raise ValidationError(
                _("The journal account {} is deprecated.").format(
                    deprecated_account.display_name
                )
            )
