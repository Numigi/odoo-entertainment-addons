# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo.tests.common import SavepointCase


class TestSoldTickets(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Project 1"})
        cls.project2 = cls.env["project.project"].create({"name": "Project 2"})

        cls.date_1 = datetime.now().date()
        cls.date_2 = datetime.now().date() + timedelta(30)
        cls.date_3 = datetime.now().date() + timedelta(50)

        cls.ticket_1 = cls._add_ticket_sold(cls.project, cls.date_1, 10)
        cls.ticket_2 = cls._add_ticket_sold(cls.project, cls.date_2, 20)


    def test_add_tickets_before(self):
        ticket_3 = self._add_ticket_sold(self.project, self.date_1 - timedelta(1), 15)
        assert ticket_3.new_sold_tickets == 15

    def test_add_tickets_after(self):
        ticket_3 = self._add_ticket_sold(self.project, self.date_2 + timedelta(1), 15)
        assert ticket_3.new_sold_tickets == -5  # 20 - 15

    def test_add_tickets_between(self):
        ticket_3 = self._add_ticket_sold(self.project, self.date_1 + timedelta(1), 14)
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
    def _add_ticket_sold(cls, project, date_, total_sold_tickets):
        return cls.env["show.ticket.sold"].create(
            {
                "show_id": project.id,
                "record_date": date_,
                "total_sold_tickets": total_sold_tickets,
            }
        )

    def test_compute_favour_tickets(self):
        self.project.artist_favour_tickets = 10
        self.project.diffisor_favour_tickets = 20
        assert self.ticket_2.favour_tickets == 30

    def test_compute_sold_tickets(self):
        self.project.show_place_maximum_capacity = 100
        self.project.artist_favour_tickets = 5
        self.project.diffisor_favour_tickets = 1
        assert self.ticket_1.sold_tickets == 0.11  # 10 /(100-5-1)
        assert self.ticket_2.sold_tickets == 0.21  # 20 /(100-5-1)

    def test_lastEntry_onCreation(self):
        assert not self.ticket_1.last_entry
        assert self.ticket_2.last_entry

    def test_lastEntry_afterModifyRecordDate(self):
        self.ticket_1.write({'record_date': self.date_3})
        assert self.ticket_1.last_entry
        assert not self.ticket_2.last_entry

    def test_ifOneTicket_thenlastEntryIsTrue(self):
        ticket_3 = self._add_ticket_sold(self.project2, self.date_2, 20)
        assert ticket_3.last_entry
