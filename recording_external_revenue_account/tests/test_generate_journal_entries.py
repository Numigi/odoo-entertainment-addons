# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime, timedelta
from ddt import ddt, data, unpack
from odoo.exceptions import ValidationError
from odoo.addons.recording_external_revenue.tests.common import \
    ExternalRevenueCase


@ddt
class TestConversion(ExternalRevenueCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.recording.state = "validated"
        cls.partner = cls.believe.with_context(force_company=cls.company.id)
        cls.product = cls.stream.with_context(force_company=cls.company.id)
        cls.operation_date = datetime.now().date() + timedelta(10)
        cls.period_start_date = datetime.now().date() + timedelta(5)
        cls.period_end_date = datetime.now().date() + timedelta(15)
        cls.quantity = 5
        cls.gross_amount_per_unit = 10
        cls.gross_amount = 50
        cls.commission_amount = 20
        cls.net_amount = 30
        cls.revenue = cls._create_revenue(
            analytic_account_id=cls.analytic_account.id,
            artist_id=cls.artist.id,
            commission_amount=cls.commission_amount,
            country_id=cls.canada.id,
            currency_id=cls.cad.id,
            fiscal_position="revenue",
            gross_amount=cls.gross_amount,
            gross_amount_per_unit=cls.gross_amount_per_unit,
            net_amount=cls.net_amount,
            operation_date=cls.operation_date,
            partner_id=cls.partner.id,
            period_end_date=cls.period_end_date,
            period_start_date=cls.period_start_date,
            platform_id=cls.spotify.id,
            quantity=cls.quantity,
            recording_id=cls.recording.id,
            state_id=cls.quebec.id,
            subplatform_id=cls.spotify_premium.id,
            tax_base="net_amount",
            tax_id=cls.tax.id,
            product_id=cls.product.id,
            company_id=cls.company.id,
        )

        cls.journal = cls.env["account.journal"].create(
            {
                "name": "External Revenues (CAD)",
                "code": "EXTCAD",
                "type": "general",
                "company_id": cls.company.id,
            }
        )

        cls.eur_journal = cls.env["account.journal"].create(
            {
                "name": "External Revenues (EUR)",
                "code": "EXTEUR",
                "type": "general",
                "company_id": cls.company.id,
                "currency_id": cls.eur.id,
            }
        )

        cls.journal_mapping = cls.env["recording.journal.mapping"].create(
            {
                "journal_id": cls.journal.id,
                "currency_id": cls.cad.id,
                "company_id": cls.company.id,
            }
        )

        cls.eur_journal_mapping = cls.env["recording.journal.mapping"].create(
            {
                "journal_id": cls.eur_journal.id,
                "currency_id": cls.eur.id,
                "company_id": cls.company.id,
            }
        )

        cls.receivable_account = cls._create_account(
            name="Receivable",
            code="111111",
            company_id=cls.company.id,
            user_type_id=cls.env.ref("account.data_account_type_receivable").id,
            reconcile=True,
        )

        cls.tax_account = cls._create_account(
            name="Taxes",
            code="222222",
            company_id=cls.company.id,
            user_type_id=cls.env.ref(
                "account.data_account_type_current_liabilities"
            ).id,
        )

        cls.revenue_account = cls._create_account(
            name="Revenue",
            code="444444",
            company_id=cls.company.id,
            user_type_id=cls.env.ref("account.data_account_type_revenue").id,
        )

        cls.other_revenue_account = cls._create_account(
            name="Other Revenue",
            code="444445",
            company_id=cls.company.id,
            user_type_id=cls.env.ref("account.data_account_type_revenue").id,
        )

        cls.product.property_account_income_id = cls.revenue_account

        cls.tax.account_id = cls.tax_account.id
        cls.partner.property_account_receivable_id = cls.receivable_account

        cls.tps = cls._create_tax(
            name="TPS",
            amount=5,
            amount_type="percent",
            company_id=cls.company.id,
            account_id=cls.tax_account.id,
        )
        cls.tps_account = cls._create_account(
            name="Quebec Tax (TPS)",
            code="222223",
            company_id=cls.company.id,
            user_type_id=cls.env.ref(
                "account.data_account_type_current_liabilities"
            ).id,
        )

        cls.fixed_amount_tax = cls._create_fixed_amount_tax(1000)

        cls.fiscal_position_quebec = cls._create_fiscal_position(
            name="Quebec",
            company_id=cls.company.id,
            state_ids=[(4, cls.quebec.id)],
            country_id=cls.canada.id,
            auto_apply=True,
        )
        cls._create_fiscal_position_tax_rule(
            cls.fiscal_position_quebec, cls.tax, cls.tps
        )

    @classmethod
    def _create_fiscal_position(cls, **kwargs):
        return cls.env["account.fiscal.position"].create(kwargs)

    @classmethod
    def _create_fiscal_position_tax_rule(cls, position, src_tax, dest_tax):
        return cls.env["account.fiscal.position.tax"].create(
            {
                "position_id": position.id,
                "tax_src_id": src_tax.id,
                "tax_dest_id": dest_tax.id,
            }
        )

    @classmethod
    def _create_fiscal_position_account_rule(cls, position, src_account,
                                             dest_account):
        return cls.env["account.fiscal.position.account"].create(
            {
                "position_id": position.id,
                "account_src_id": src_account.id,
                "account_dest_id": dest_account.id,
            }
        )

    @classmethod
    def _create_account(cls, **kwargs):
        return cls.env["account.account"].create(kwargs)

    @classmethod
    def _create_revenue(cls, **kwargs):
        return cls.env["recording.external.revenue"].create(kwargs)

    @classmethod
    def _create_fixed_amount_tax(cls, amount):
        return cls._create_tax(
            name="Tax defined on product",
            amount=amount,
            amount_type="fixed",
            company_id=cls.company.id,
            account_id=cls.tax_account.id,
        )

    @classmethod
    def _find_jobs(cls, revenue):
        return (
            cls.env["queue.job"]
            .search(
                [
                    ("model_name", "=", "recording.external.revenue"),
                    ("method_name", "=", "generate_journal_entry"),
                ]
            )
            .filtered(lambda j: j.record_ids == [revenue.id])
        )

    def test_schedule_generate_journal_entries(self):
        self.env[
            "recording.external.revenue"].schedule_generate_journal_entries(
            self.company
        )
        assert len(self._find_jobs(self.revenue)) == 1

    def test_journal_entry_posted(self):
        entry = self.revenue.generate_journal_entry()
        assert entry.state == "posted"

    def test_journal_mapping(self):
        entry = self.revenue.generate_journal_entry()
        assert entry.journal_id == self.journal

    def test_no_journal_found(self):
        self.journal_mapping.unlink()
        with pytest.raises(ValidationError):
            self.revenue.generate_journal_entry()

    def test_deprecated_account(self):
        self.revenue_account.deprecated = True
        with pytest.raises(ValidationError):
            self.revenue.generate_journal_entry()

    def test_operation_date(self):
        entry = self.revenue.generate_journal_entry()
        assert entry.date == self.period_end_date

    def test_journal_accounts(self):
        entry = self.revenue.generate_journal_entry()
        assert len(entry.line_ids) == 3
        assert len(self._get_revenue_line(entry)) == 1
        assert len(self._get_tax_line(entry)) == 1
        assert len(self._get_receivable_line(entry)) == 1

    @data(
        ("net_amount", 10, 3),
        ("net_amount", 20, 6),
        ("gross_amount", 10, 5),
        ("gross_amount", 20, 10),
    )
    @unpack
    def test_tax_amount(self, tax_base, percent, expected_amount):
        self.revenue.tax_base = tax_base
        self.tax.amount_type = "percent"
        self.tax.amount = percent
        entry = self.revenue.generate_journal_entry()
        assert self._get_tax_line(entry).credit == expected_amount

    def test_tax_defined_on_product(self):
        self.revenue.tax_id = False
        self.stream.taxes_id = self.fixed_amount_tax
        entry = self.revenue.generate_journal_entry()
        assert self._get_tax_line(entry).credit == self.fixed_amount_tax.amount

    def test_tax_defined_on_revenue_account(self):
        self.revenue.tax_id = False
        self.revenue_account.tax_ids = self.fixed_amount_tax
        entry = self.revenue.generate_journal_entry()
        assert self._get_tax_line(entry).credit == self.fixed_amount_tax.amount

    def test_fiscal_position_used_on_product_taxes(self):
        self.revenue.tax_id = False
        self.stream.taxes_id = self.fixed_amount_tax
        self._create_fiscal_position_tax_rule(
            self.fiscal_position_quebec, self.fixed_amount_tax, self.tps
        )
        entry = self.revenue.generate_journal_entry()
        assert self._get_tax_line(entry).credit == 1.5  # 0.05 * self.net_amount

    def test_fiscal_position_used_on_account_taxes(self):
        self.revenue.tax_id = False
        self.revenue_account.tax_ids = self.fixed_amount_tax
        self._create_fiscal_position_tax_rule(
            self.fiscal_position_quebec, self.fixed_amount_tax, self.tps
        )
        entry = self.revenue.generate_journal_entry()
        assert self._get_tax_line(entry).credit == 1.5  # 0.05 * self.net_amount

    def test_revenue_account(self):
        entry = self.revenue.generate_journal_entry()
        assert self._get_revenue_line(entry).account_id == self.revenue_account

    def test_revenue_account_mapped_with_fiscal_position(self):
        self._create_fiscal_position_account_rule(
            self.fiscal_position_quebec,
            self.revenue_account,
            self.other_revenue_account,
        )
        entry = self.revenue.generate_journal_entry()
        assert self._get_revenue_line(
            entry).account_id == self.other_revenue_account

    def test_no_available_fiscal_position(self):
        self.revenue.state_id = False
        self.revenue.country_id = self.env.ref("base.fr")
        with pytest.raises(ValidationError):
            self.revenue.generate_journal_entry()

    def test_fiscal_position_defined_on_partner(self):
        self.revenue.write(
            {"fiscal_position": "partner", "country_id": False,
             "state_id": False}
        )
        self.revenue.partner_id.write(
            {"country_id": self.canada.id, "state_id": self.quebec.id}
        )
        self._create_fiscal_position_account_rule(
            self.fiscal_position_quebec,
            self.revenue_account,
            self.other_revenue_account,
        )
        entry = self.revenue.generate_journal_entry()
        assert self._get_revenue_line(
            entry).account_id == self.other_revenue_account

    def test_no_fiscal_position_found_for_the_partner(self):
        self.revenue.write(
            {"fiscal_position": "partner", "country_id": False,
             "state_id": False}
        )
        self.partner.state_id = False
        self.partner.country_id = self.env.ref("base.fr")
        with pytest.raises(ValidationError):
            self.revenue.generate_journal_entry()

    def test_amount_in_foreign_currency(self):
        self._set_currency_rate(self.eur, 0.8)
        self.revenue.currency_id = self.eur
        self.receivable_account.currency_id = self.eur
        self.revenue_account.currency_id = self.eur
        self.tax.amount = 10

        entry = self.revenue.generate_journal_entry()

        revenue_line = self._get_revenue_line(entry)
        assert revenue_line.credit == 37.5  # net_amount / 0.8
        assert revenue_line.amount_currency == -30  # net_amount
        assert revenue_line.currency_id == self.eur

        tax_line = self._get_tax_line(entry)
        assert tax_line.credit == 3.75  # net_amount * 10% / 0.8
        assert tax_line.amount_currency == -3
        assert tax_line.currency_id == self.eur

        receivable_line = self._get_receivable_line(entry)
        assert receivable_line.debit == 41.25
        assert receivable_line.amount_currency == 33  # net_amount * (1 + 10%) / 0.8
        assert receivable_line.currency_id == self.eur

    def test_use_proper_currency_rate(self):
        self._set_currency_rate(self.eur, 0.3, self.period_start_date)
        self._set_currency_rate(self.eur, 0.5, self.operation_date)
        self._set_currency_rate(self.eur, 0.8, self.period_end_date)
        self.revenue.currency_id = self.eur
        entry = self.revenue.generate_journal_entry()
        revenue_line = self._get_revenue_line(entry)
        assert revenue_line.credit == 37.5  # net_amount / 0.5

    def _set_currency_rate(self, currency, rate, date=None):
        values = {
            "name": date or datetime.now().date(),
            "rate": rate,
            "company_id": self.company.id,
        }
        currency.write({"rate_ids": [(0, 0, values)]})

    def _get_revenue_line(self, move):
        return move.line_ids.filtered(
            lambda
                l: l.account_id in self.revenue_account | self.other_revenue_account
        )

    def _get_receivable_line(self, move):
        return move.line_ids.filtered(
            lambda l: l.account_id == self.receivable_account)

    def _get_tax_line(self, move):
        return move.line_ids.filtered(
            lambda l: l.account_id == self.tax_account)

    def test_due_date_with_no_payment_term(self):
        self.partner.property_payment_term_id = None
        entry = self.revenue.generate_journal_entry()
        receivable_line = self._get_receivable_line(entry)
        assert receivable_line.date_maturity == self.period_end_date

    def test_payment_term_30_days(self):
        payment_term = self._create_payment_term(
            name="30 Days", lines=[("balance", 0, 30, "day_after_invoice_date")]
        )
        self.partner.property_payment_term_id = payment_term
        entry = self.revenue.generate_journal_entry()
        receivable_line = self._get_receivable_line(entry)
        expected_due_date = self.period_end_date + timedelta(30)
        assert receivable_line.date_maturity == expected_due_date

    def test_2_payment_term_lines(self):
        payment_term = self._create_payment_term(
            name=r"50% after 15 days / 50% after 30 days",
            lines=[
                ("percent", 50, 15, "day_after_invoice_date"),
                ("balance", 0, 30, "day_after_invoice_date"),
            ],
        )
        self.partner.property_payment_term_id = payment_term
        entry = self.revenue.generate_journal_entry()
        receivable_line = self._get_receivable_line(entry)
        assert len(receivable_line) == 2

    @classmethod
    def _create_payment_term(cls, name, lines):
        line_vals = (
            {
                "value": value,
                "value_amount": value_amount,
                "days": days,
                "option": option,
            }
            for value, value_amount, days, option in lines
        )
        return cls.env["account.payment.term"].create(
            {"name": name, "line_ids": [(0, 0, v) for v in line_vals]}
        )

    def test_analytic_account(self):
        entry = self.revenue.generate_journal_entry()

        revenue_line = self._get_revenue_line(entry)
        assert revenue_line.analytic_account_id == self.analytic_account

        tax_line = self._get_tax_line(entry)
        assert not tax_line.analytic_account_id

        receivable_line = self._get_receivable_line(entry)
        assert not receivable_line.analytic_account_id

    def test_if_already_posted__raise_error(self):
        self.revenue.generate_journal_entry()
        with pytest.raises(ValidationError):
            self.revenue.generate_journal_entry()

    def test_revenue_id_in_journal_entry_reference(self):
        move = self.revenue.generate_journal_entry()
        assert str(self.revenue.id) in move.ref

    def test_can_not_delete_posted_revenue(self):
        self.revenue.generate_journal_entry()
        with pytest.raises(ValidationError):
            self.revenue.unlink()

    def test_can_not_edit_posted_revenue(self):
        self.revenue.generate_journal_entry()
        with pytest.raises(ValidationError):
            self.revenue.analytic_account_id = False

    def test_recording_dimensions(self):
        entry = self.revenue.generate_journal_entry()
        revenue_line = self._get_revenue_line(entry)
        assert revenue_line.artist_id == self.artist
        assert revenue_line.recording_id == self.recording

    def test_partner(self):
        entry = self.revenue.generate_journal_entry()

        revenue_line = self._get_revenue_line(entry)
        assert revenue_line.partner_id == self.partner

        tax_line = self._get_tax_line(entry)
        assert tax_line.partner_id == self.partner

        receivable_line = self._get_receivable_line(entry)
        assert receivable_line.partner_id == self.partner

    def test_recording_not_validated(self):
        self.recording.state = "to_validate"
        with pytest.raises(ValidationError):
            self.revenue.generate_journal_entry()

    def test_currency_and_amount_currency_1(self):
        self.company.currency_id = self.cad
        move_id = self.revenue.generate_journal_entry()
        assert not move_id.mapped('line_ids.currency_id')
        assert all([l.amount_currency == 0 for l in
                    move_id.mapped('line_ids')])

    def test_currency_and_amount_currency_2(self):
        self.company.currency_id = self.eur
        move_id = self.revenue.generate_journal_entry()
        assert all(
            [l.currency_id == self.cad and l.amount_currency != 0 for l in
             move_id.mapped('line_ids')])
