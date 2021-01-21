# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import AccessError
from odoo.tests.common import SavepointCase


class TestShowProjectSecurity(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_user = (
            cls.env["res.users"]
                .with_context(tracking_disable=True, no_reset_password=True)
                .create({"login": "project_user", "name": "project_user", "email": "admin@admin.com"})
        )
        cls.project_employee = cls.env["hr.employee"].create({
            "name": "Project Employee",
            "user_id": cls.project_user.id,
        })
        cls.standard_project = cls.env["project.project"].create(
            {
                "name": "Standard Project 1",
                "show_type": "standard"}
        )
        cls.show_project = cls.env["project.project"].create(
            {
                "name": "Show Project 1",
                "show_type": "show"}
        )
        cls.tour_project = cls.env["project.project"].create(
            {
                "name": "Tour Project 1",
                "show_type": "tour"}
        )
        cls.standard_project_task = cls.env["project.task"].create(
            {
                "name": "Standard Project task",
                "project_id": cls.standard_project.id,
            }
        )
        cls.show_project_task = cls.env["project.task"].create(
            {
                "name": "Show Project task",
                "project_id": cls.show_project.id,
            }
        )
        cls.tour_project_task = cls.env["project.task"].create(
            {
                "name": "Tour Project task",
                "project_id": cls.tour_project.id,
            }
        )
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {"name": "Analytic Account", }
        )
        cls.standard_timesheet = cls.env["account.analytic.line"].create(
            {
                "name": "Standard Timesheet",
                "project_id": cls.standard_project_task.project_id.id,
                "task_id": cls.standard_project_task.id,
                "employee_id": cls.project_employee.id,
                "account_id": cls.analytic_account.id,
            }
        )
        cls.tour_timesheet = cls.env["account.analytic.line"].create(
            {
                "name": "Tour Timesheet",
                "project_id": cls.tour_project_task.project_id.id,
                "task_id": cls.tour_project_task.id,
                "employee_id": cls.project_employee.id,
                "account_id": cls.analytic_account.id,
            }
        )
        cls.show_timesheet = cls.env["account.analytic.line"].create(
            {
                "name": "Show Timesheet",
                "project_id": cls.show_project_task.project_id.id,
                "task_id": cls.show_project_task.id,
                "employee_id": cls.project_employee.id,
                "account_id": cls.analytic_account.id,
            }
        )

    def _set_user_groups(self, groups=[]):
        self.project_user.write({
            "groups_id": [(6, 0, [group_id.id for group_id in groups])]
        })

    def _create_project(self, type):
        self.env["project.project"].sudo(user=self.project_user).create({
            "show_type": type,
            "name": "Project"
        })

    def _create_task(self, project):
        self.env["project.task"].sudo(user=self.project_user).create({
            "project_id": project.id,
            "name": "Task",
        })

    def _create_timesheet(self, task):
        self.env["account.analytic.line"].sudo(user=self.project_user).create({
            "project_id": task.project_id.id,
            "name": "Timesheet",
            "employee_id": self.project_employee.id,
            "task_id": task.id,
            "account_id": self.analytic_account.id,
        })

    ############## Project User Group Without Show Manager Group ##############
    def test_project_user_without_show_manager_group_can_not_create_standard_project(self):
        self._set_user_groups([self.env.ref("project.group_project_user")])
        with self.assertRaises(AccessError):
            self._create_project("standard")

    def test_project_user_without_show_manager_group_can_not_create_tour_or_show_project(self):
        self._set_user_groups([self.env.ref("project.group_project_user")])
        with self.assertRaises(AccessError):
            self._create_project("tour")
        with self.assertRaises(AccessError):
            self._create_project("show")

    def test_project_user_without_show_manager_group_can_not_create_tour_or_show_project_task(self):
        self._set_user_groups([self.env.ref("project.group_project_user")])
        with self.assertRaises(AccessError):
            self._create_task(self.show_project)
        with self.assertRaises(AccessError):
            self._create_task(self.tour_project)

    def test_project_user_without_show_manager_group_can_not_edit_tour_or_show_project_task(self):
        self._set_user_groups([self.env.ref("project.group_project_user")])
        with self.assertRaises(AccessError):
            self.show_project_task.sudo(user=self.project_user).write({"name": "Updated Show Project Task"})
        with self.assertRaises(AccessError):
            self.tour_project_task.sudo(user=self.project_user).write({"name": "Tour Show Project Task"})

    def test_project_user_without_show_manager_group_can_read_all_project(self):
        self._set_user_groups([self.env.ref("project.group_project_user")])
        self.assertEqual(self.standard_project.sudo(user=self.project_user).search_count([]),
                         self.standard_project.sudo(user=self.project_user).search_count([("show_type", "in", ("tour", "show", "standard"))]))

    def test_project_user_without_show_manager_group_can_read_all_project_task(self):
        self._set_user_groups([self.env.ref("project.group_project_user")])
        self.assertEqual(self.standard_project_task.sudo(user=self.project_user).search_count([]),
                         self.standard_project_task.sudo(user=self.project_user).search_count([("project_id.show_type", "in", ("tour", "show", "standard"))]))

    def test_project_user_without_show_manager_group_can_create_standard_project_task(self):
        self._set_user_groups([self.env.ref("project.group_project_user")])
        self._create_task(self.standard_project)

    ############## Project Manager Group Without Show Manager Group ###########
    def test_project_manager_without_show_manager_group_can_not_create_tour_or_show_project(
        self):
        self._set_user_groups([self.env.ref("project.group_project_manager")])
        with self.assertRaises(AccessError):
            self._create_project("tour")
        with self.assertRaises(AccessError):
            self._create_project("show")

    def test_project_manager_without_show_manager_group_can_not_create_tour_or_show_project_task(self):
        self._set_user_groups([self.env.ref("project.group_project_manager")])
        with self.assertRaises(AccessError):
            self._create_task(self.show_project)
        with self.assertRaises(AccessError):
            self._create_task(self.tour_project)

    def test_project_manager_without_show_manager_group_can_not_edit_tour_or_show_project_task(self):
        self._set_user_groups([self.env.ref("project.group_project_manager")])
        with self.assertRaises(AccessError):
            self.show_project_task.sudo(user=self.project_user).write(
                {"name": "Updated Show Project Task"})
        with self.assertRaises(AccessError):
            self.tour_project_task.sudo(user=self.project_user).write(
                {"name": "Tour Show Project Task"})

    def test_project_manager_without_show_manager_group_can_create_standard_project(self):
        self._set_user_groups([self.env.ref("project.group_project_manager")])
        self._create_project("standard")

    def test_project_manager_without_show_manager_group_can_read_all_project(self):
        self._set_user_groups([self.env.ref("project.group_project_manager")])
        self.assertEqual(self.standard_project.sudo(user=self.project_user).search_count([]),
                         self.standard_project.sudo(user=self.project_user).search_count([("show_type", "in", ("tour", "show", "standard"))]))

    def test_project_manager_without_show_manager_group_can_read_all_project_task(self):
        self._set_user_groups([self.env.ref("project.group_project_manager")])
        self.assertEqual(self.standard_project_task.sudo(user=self.project_user).search_count([]),
                         self.standard_project_task.sudo(user=self.project_user).search_count([("project_id.show_type", "in", ("tour", "show", "standard"))]))

    def test_project_manager_without_show_manager_group_can_create_standard_project_task(self):
        self._set_user_groups([self.env.ref("project.group_project_manager")])
        self._create_task(self.standard_project)

    def test_project_manager_without_show_manager_group_can_edit_standard_project_task(self):
        self._set_user_groups([self.env.ref("project.group_project_manager")])
        self.standard_project_task.sudo(user=self.project_user).write({"name": "Updated Standard Project Task"})

    ###### Project User Group, User Timesheet Group Without Show Manager Group ######
    def test_project_user_timesheet_user_without_show_manager_group_can_not_create_tour_or_show_project_timesheet(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user")])
        with self.assertRaises(AccessError):
            self._create_timesheet(self.tour_project_task)
        with self.assertRaises(AccessError):
            self._create_timesheet(self.show_project_task)

    def test_project_user_timesheet_user_without_show_manager_group_can_not_edit_tour_or_show_project_timesheet(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user")])
        with self.assertRaises(AccessError):
            self.tour_timesheet.sudo(user=self.project_user).write({"name": "Updated Tour Timesheet"})
        with self.assertRaises(AccessError):
            self.show_timesheet.sudo(user=self.project_user).write({"name": "Updated Show Timesheet"})

    def test_project_user_timesheet_user_without_show_manager_group_can_create_standard_project_timesheet(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user")])
        self._create_timesheet(self.standard_project_task)

    def test_project_user_timesheet_user_without_show_manager_group_can_edit_standard_project_timesheet(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user")])
        self.standard_timesheet.sudo(user=self.project_user).write({"name": "Updated Standard Timesheet"})

    ###### Project Manager Group, User Timesheet Group Without Show Manager Group ######
    def test_project_manager_timesheet_user_without_show_manager_group_can_not_create_tour_or_show_project_timesheet(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user")])
        with self.assertRaises(AccessError):
            self._create_timesheet(self.tour_project_task)
        with self.assertRaises(AccessError):
            self._create_timesheet(self.show_project_task)

    def test_project_manager_timesheet_user_without_show_manager_group_can_not_edit_tour_or_show_project_timesheet(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user")])
        with self.assertRaises(AccessError):
            self.tour_timesheet.sudo(user=self.project_user).write(
                {"name": "Updated Tour Timesheet"})
        with self.assertRaises(AccessError):
            self.show_timesheet.sudo(user=self.project_user).write(
                {"name": "Updated Show Timesheet"})

    def test_project_manager_timesheet_user_without_show_manager_group_can_create_standard_project_timesheet(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user")])
        self._create_timesheet(self.standard_project_task)

    def test_project_manager_timesheet_user_without_show_manager_group_can_edit_standard_project_timesheet(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user")])
        self.standard_timesheet.sudo(user=self.project_user).write(
            {"name": "Updated Standard Timesheet"})

    ############## Project User Group With Show Manager Group ##############
    def test_project_user_with_show_manager_group_can_not_create_standard_project(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("show_project.group_show_manager")])
        with self.assertRaises(AccessError):
            self._create_project("standard")

    def test_project_user_with_show_manager_group_can_not_create_tour_or_show_project(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("show_project.group_show_manager")])
        with self.assertRaises(AccessError):
            self._create_project("tour")
        with self.assertRaises(AccessError):
            self._create_project("show")

    def test_project_user_with_show_manager_group_can_create_project_task_all_type(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("show_project.group_show_manager")])
        self._create_task(self.show_project)
        self._create_task(self.tour_project)
        self._create_task(self.standard_project)

    def test_project_user_with_show_manager_group_can_edit_project_task_all_type(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("show_project.group_show_manager")])
        self.show_project_task.sudo(user=self.project_user).write(
                {"name": "Updated Show Project Task"})
        self.tour_project_task.sudo(user=self.project_user).write(
                {"name": "Tour Show Project Task"})
        self.standard_project_task.sudo(user=self.project_user).write(
            {"name": "Standard Show Project Task"})

    def test_project_user_with_show_manager_group_can_read_all_show_type(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("show_project.group_show_manager")])
        self.assertEqual(self.standard_project.sudo(user=self.project_user).search_count([]),
                         self.standard_project.sudo(user=self.project_user).search_count([("show_type", "in", ("tour", "show", "standard"))]))

    def test_project_user_with_show_manager_group_can_read_all_project_task_type(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("show_project.group_show_manager")])
        self.assertEqual(self.standard_project_task.sudo(user=self.project_user).search_count([]),
                         self.standard_project_task.sudo(user=self.project_user).search_count([("project_id.show_type", "in", ("tour", "show", "standard"))]))

    ############## Project Manager Group With Show Manager Group ##############
    def test_project_manager_with_show_manager_group_can_create_all_show_type(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("show_project.group_show_manager")])
        self._create_project("standard")
        self._create_project("tour")
        self._create_project("show")

    def test_project_manager_with_show_manager_group_can_create_all_project_task_type(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("show_project.group_show_manager")])
        self._create_task(self.show_project)
        self._create_task(self.tour_project)
        self._create_task(self.standard_project)

    def test_project_manager_with_show_manager_group_can_edit_all_project_task_type(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("show_project.group_show_manager")])
        self.show_project_task.sudo(user=self.project_user).write(
            {"name": "Updated Show Project Task"})
        self.tour_project_task.sudo(user=self.project_user).write(
            {"name": "Tour Show Project Task"})
        self.standard_project_task.sudo(user=self.project_user).write(
            {"name": "Standard Show Project Task"})

    def test_project_manager_with_show_manager_group_can_read_all_show_type(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("show_project.group_show_manager")])
        self.assertEqual(self.standard_project.sudo(user=self.project_user).search_count([]),
                         self.standard_project.sudo(user=self.project_user).search_count([("show_type", "in", ("tour", "show", "standard"))]))

    def test_project_manager_with_show_manager_group_can_read_all_project_task_type(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("show_project.group_show_manager")])
        self.assertEqual(self.standard_project_task.sudo(user=self.project_user).search_count([]),
                         self.standard_project_task.sudo(user=self.project_user).search_count([("project_id.show_type", "in", ("tour", "show", "standard"))]))

    ###### Project User Group, User Timesheet Group With Show Manager Group ######
    def test_project_user_timesheet_user_with_show_manager_group_can_create_timesheet_all_show_type(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user"),
                               self.env.ref("show_project.group_show_manager")])
        self._create_timesheet(self.tour_project_task)
        self._create_timesheet(self.show_project_task)
        self._create_timesheet(self.standard_project_task)

    def test_project_user_timesheet_user_with_show_manager_group_can_edit_timesheet_all_show_type(self):
        self._set_user_groups([self.env.ref("project.group_project_user"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user"),
                               self.env.ref("show_project.group_show_manager")])
        self.tour_timesheet.sudo(user=self.project_user).write(
                {"name": "Updated Tour Timesheet"})
        self.show_timesheet.sudo(user=self.project_user).write(
                {"name": "Updated Show Timesheet"})
        self.standard_timesheet.sudo(user=self.project_user).write(
            {"name": "Updated Standard Timesheet"})

    ###### Project Manager Group, User Timesheet Group With Show Manager Group ######
    def test_project_manager_timesheet_user_with_show_manager_group_can_create_timesheet_all_show_type(
        self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user"),
                               self.env.ref("show_project.group_show_manager")])
        self._create_timesheet(self.tour_project_task)
        self._create_timesheet(self.show_project_task)
        self._create_timesheet(self.standard_project_task)

    def test_project_manager_timesheet_user_with_show_manager_group_can_edit_timesheet_all_show_type(self):
        self._set_user_groups([self.env.ref("project.group_project_manager"),
                               self.env.ref("hr_timesheet.group_hr_timesheet_user"),
                               self.env.ref("show_project.group_show_manager")])
        self.tour_timesheet.sudo(user=self.project_user).write(
            {"name": "Updated Tour Timesheet"})
        self.show_timesheet.sudo(user=self.project_user).write(
            {"name": "Updated Show Timesheet"})
        self.standard_timesheet.sudo(user=self.project_user).write(
            {"name": "Updated Standard Timesheet"})
