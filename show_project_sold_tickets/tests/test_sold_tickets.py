# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests.common import SavepointCase


class TestSoldTickets(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Project 1"})

        cls.date_1 = datetime.now().date()
        cls.date_2 = datetime.now().date() + timedelta(30)

        cls.ticket_1 = cls._add_ticket_sold(cls.date_1, 10)
        cls.ticket_2 = cls._add_ticket_sold(cls.date_2, 20)

    def test_add_tickets_before(self):
        ticket_3 = self._add_ticket_sold(self.date_1 - timedelta(1), 15)
        assert ticket_3.new_sold_tickets == 15

    def test_add_tickets_after(self):
        ticket_3 = self._add_ticket_sold(self.date_2 + timedelta(1), 15)
        assert ticket_3.new_sold_tickets == -5  # 20 - 15

    def test_add_tickets_between(self):
        ticket_3 = self._add_ticket_sold(self.date_1 + timedelta(1), 14)
        assert self.ticket_1.new_sold_tickets == 10
        assert ticket_3.new_sold_tickets == 4
        assert self.ticket_2.new_sold_tickets == 6

    def test_update_existing_ticket(self):
        self.ticket_1.total_sold_tickets = 15
        assert self.ticket_1.new_sold_tickets == 15
        assert self.ticket_2.new_sold_tickets == 5

    def test_unlink_existing_ticket(self):
        self.ticket_1.unlink()
        assert self.ticket_2.new_sold_tickets == 20

    @classmethod
    def _add_ticket_sold(cls, date_, total_sold_tickets):
        return cls.env["show.ticket.sold"].create(
            {
                "show_id": cls.project.id,
                "record_date": date_,
                "total_sold_tickets": total_sold_tickets,
            }
        )
