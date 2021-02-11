# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from ddt import ddt, data
from odoo.tests.common import SavepointCase
from odoo.exceptions import AccessError


class ShowProjectAccessCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create(
            {"name": "Project 1", "show_type": "standard"}
        )
        cls.task = cls.env["project.task"].create(
            {"name": "Task 1", "project_id": cls.project.id}
        )
        cls.user = cls.env.ref("base.user_demo")
        cls.user.groups_id = cls.env.ref("project.group_project_manager")
        cls.show_manager_group = cls.env.ref("show_project_access.group_show_manager")


@ddt
class TestProject(ShowProjectAccessCase):
    def test_create__non_member__standard_project(self):
        self.project.sudo(self.user).check_extended_security_create()

    @data("tour", "show")
    def test_create__non_member__restricted(self, show_type):
        self.project.show_type = show_type
        with pytest.raises(AccessError):
            self.project.sudo(self.user).check_extended_security_create()

    def test_write__non_member__standard_project(self):
        self.project.sudo(self.user).check_extended_security_write()

    @data("tour", "show")
    def test_write__non_member__restricted(self, show_type):
        self.project.show_type = show_type
        with pytest.raises(AccessError):
            self.project.sudo(self.user).check_extended_security_write()

    def test_create__member(self):
        self.project.show_type = "tour"
        self.user.groups_id |= self.show_manager_group
        self.project.sudo(self.user).check_extended_security_create()

    def test_write__member(self):
        self.project.show_type = "tour"
        self.user.groups_id |= self.show_manager_group
        self.project.sudo(self.user).check_extended_security_write()


@ddt
class TestTask(ShowProjectAccessCase):
    def test_create__non_member__standard_project(self):
        self.task.sudo(self.user).check_extended_security_create()

    @data("tour", "show")
    def test_create__non_member__restricted(self, show_type):
        self.project.show_type = show_type
        with pytest.raises(AccessError):
            self.task.sudo(self.user).check_extended_security_create()

    def test_write__non_member__standard_project(self):
        self.task.sudo(self.user).check_extended_security_write()

    @data("tour", "show")
    def test_write__non_member__restricted(self, show_type):
        self.project.show_type = show_type
        with pytest.raises(AccessError):
            self.task.sudo(self.user).check_extended_security_write()

    def test_create__member(self):
        self.project.show_type = "tour"
        self.user.groups_id |= self.show_manager_group
        self.task.sudo(self.user).check_extended_security_create()

    def test_write__member(self):
        self.project.show_type = "tour"
        self.user.groups_id |= self.show_manager_group
        self.task.sudo(self.user).check_extended_security_write()
