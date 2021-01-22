# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from psycopg2 import IntegrityError

from odoo.exceptions import AccessError
from odoo.tests.common import SavepointCase
from odoo.tools import mute_logger


class TestProjectRoleShow(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_user = (
            cls.env["res.users"]
                .with_context(tracking_disable=True, no_reset_password=True)
                .create({"login": "project_user", "name": "project_user", "email": "admin@admin.com"})
        )
        cls.project_role_tour = cls.env["project.tour.role"].create({
            "name": "Project Role Tour 1"
        })
        cls.artist_partner = cls.env["res.partner"].create({
            "name": "Artist",
            "is_artist": True,
        })
        cls.guide_role = cls.env["project.tour.role"].create({
            "name": "Guide Role",
        })
        cls.tour_project = cls.env["project.project"].create({
            "name": "Tour Project",
            "show_type": "tour",
        })

    def _set_user_groups(self, groups=[]):
        self.project_user.write({
            "groups_id": [(6, 0, [group_id.id for group_id in groups])]
        })

    def _create_project_role_tour(self):
        self.env["project.tour.role"].sudo(user=self.project_user).create({
            "name": "Project Role Tour",
        })

    def _create_project_member(self):
        self.env["project.member"].sudo(user=self.project_user).create({
            "project_id": self.tour_project.id,
            "partner_id": self.artist_partner.id,
            "role_id": self.guide_role.id,
        })

    def test_project_user_can_read_project_role_tour(self):
        self._set_user_groups([self.env.ref("project.group_project_user")])
        self.assertEqual(self.project_role_tour.sudo(user=self.project_user).name, "Project Role Tour 1")

    def test_project_user_can_not_create_project_role_tour(self):
        self._set_user_groups([self.env.ref("project.group_project_user")])
        with self.assertRaises(AccessError):
            self._create_project_role_tour()

    def test_project_manager_can_create_project_role_tour(self):
        self._set_user_groups([self.env.ref("project.group_project_manager")])
        self._create_project_role_tour()

    @mute_logger('odoo.sql_db')
    def test_cannot_add_twice_partner_as_team_member_one_project(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"), self.env.ref("show_project.group_show_manager")])
        self._create_project_member()
        with self.assertRaises(IntegrityError):
            self._create_project_member()
