# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from psycopg2 import IntegrityError

from odoo.exceptions import AccessError
from odoo.tests.common import SavepointCase
from odoo.tools import mute_logger


class TestProjectRoleShow(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {"name": "Artist", "is_artist": True}
        )
        cls.role = cls.env["project.show.role"].create({"name": "Role 1"})
        cls.tour = cls.env["project.project"].create(
            {"name": "Tour Project", "show_type": "tour"}
        )

        cls.member = cls.env["project.show.member"].create(
            {
                "project_id": cls.tour.id,
                "partner_id": cls.partner.id,
                "role_id": cls.role.id,
            }
        )

        cls.show = cls.env["project.project"].create(
            {"name": "Tour Project", "show_type": "show", "parent_id": cls.tour.id}
        )

    def test_onchange_parent(self):
        self.show._onchange_tour_propagate_members()
        member = self.show.show_member_ids
        assert len(member) == 1
        assert member != self.member
        assert member.partner_id == self.partner
        assert member.role_id == self.role

    def test_onchange_parent__not_show(self):
        self.show.show_type = "standard"
        self.show._onchange_tour_propagate_members()
        assert not self.show.show_member_ids

    def test_onchange_parent__main_artist(self):
        self.member.main_artist = True
        self.show._onchange_tour_propagate_members()
        assert self.show.show_member_ids.main_artist

    def test_two_members_with_same_partner(self):
        with pytest.raises(IntegrityError):
            self.member.copy({})
