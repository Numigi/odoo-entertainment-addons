# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import Form
from odoo.tests.common import SavepointCase


class TestShowProject(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.empty_project = cls.env["project.project"]

        cls.artist = cls.env["artist"].create(
            {"name": "artist"}
        )
        cls.artist2 = cls.env["artist"].create(
            {"name": "artist2"}
        )
        cls.standard_project_1 = cls.env["project.project"].create(
            {"name": "Standard Project 1", "show_type": "standard"}
        )
        cls.tour_project_1 = cls.env["project.project"].create(
            {"name": "Tour Project 1", "show_type": "tour"}
        )
        cls.show_project_1 = cls.env["project.project"].create(
            {"name": "Show Project 1",
             "show_type": "show",
             "artist": cls.artist.id
             }
        )


    def _create_project(self, name, show_type=None, parent_id=None, artist=None):
        vals = {"name": name, "show_type": show_type, "parent_id": parent_id,
                "artist_id": artist}
        return self.env["project.project"].create(vals)

    def _update_show_date(self, project, show_date):
        project.write({"show_date": show_date})

    def test_tour_project_dont_have_parent(self):
        self.tour_project_2 = self._create_project(
            "Tour Project 2", show_type="tour", parent_id=self.standard_project_1.id
        )
        self.assertNotEqual(self.tour_project_2.parent_id, self.standard_project_1)

    def test_compute_previous_and_next_show_not_show_project(self):
        self.assertEqual(self.tour_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.standard_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.tour_project_1.next_show_id, self.empty_project)
        self.assertEqual(self.standard_project_1.next_show_id, self.empty_project)

    def test_compute_previous_and_next_show_show_project_without_show_date(self):
        self.assertEqual(self.show_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)

    def test_compute_previous_and_next_show_show_project_with_show_date(self):
        self._update_show_date(self.show_project_1, fields.Date.today())
        self.assertEqual(self.show_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)
        self.show_project_1.parent_id = self.tour_project_1
        self.assertEqual(self.show_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)
        self.show_project_2 = self._create_project("Show Project 2",
                                                   "show",
                                                   self.tour_project_1.id,
                                                   self.artist.id,
                                                   )
        self.assertEqual(self.show_project_1.previous_show_id, self.empty_project)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)
        self._update_show_date(self.show_project_2, fields.Date.today() - relativedelta(days=1))
        self.assertEqual(self.show_project_1.previous_show_id, self.show_project_2)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)
        self.show_project_3 = self._create_project("Show Project 3",
                                                   "show",
                                                   self.tour_project_1.id,
                                                   self.artist.id,
                                                   )
        self.assertEqual(self.show_project_1.previous_show_id, self.show_project_2)
        self.assertEqual(self.show_project_1.next_show_id, self.empty_project)
        self._update_show_date(self.show_project_3, fields.Date.today() + relativedelta(days=1))
        self.assertEqual(self.show_project_1.previous_show_id, self.show_project_2)
        self.assertEqual(self.show_project_1.next_show_id, self.show_project_3)

    def test_type_show_name_readonly(self):
        with self.assertRaises(AssertionError):
            self._create_project_with_form(
                {"name": "Show project",
                 "show_type": "show",
                 "artist_id": self.artist,
                 }
            )

    def test_type_standard_name_editable(self):
        form = self._create_project_with_form({"name": "Standard project", "show_type": "standard"})
        self.assertEqual(form.name, "Standard project")

    def test_type_tour_name_editable(self):
        form = self._create_project_with_form({"name": "Tour project", "show_type": "tour"})
        self.assertEqual(form.name, "Tour project")

    def test_type_show_name_is_set_automatically(self):
        show_place = self.env["res.partner"].create({"type": "show_site", "name": "Show Site A"})
        form = self._create_project_with_form(
            {
                "parent_id": self.tour_project_1,
                "show_type": "show",
                "artist_id": self.artist,
                "show_date": "2021-01-01",
                "show_place_id": show_place,
            }
        )
        self.assertEqual(
            form.name, "{} - {}".format("2021-01-01", show_place.display_name)
        )

    def test_project_city_is_set_by_related_show_place(self):
        show_place = self.env["res.partner"].create(
            {"type": "show_site", "name": "Show Site A", "city": "New York"}
        )
        form = self._create_project_with_form(
            {
                "parent_id": self.tour_project_1,
                "show_type": "show",
                "artist_id": self.artist,
                "show_date": "2021-01-01",
                "show_place_id": show_place,
            }
        )
        self.assertEqual(form.city, show_place.city)

    def test_set_project_show_place_auto_fill_diffusers(self):
        individual = self.env["res.partner"].create({"name": "Individual"})
        role = self.env["diffuser.role"].create({"name": "Test DR"})
        show_place = self.env["res.partner"].create(
            {
                "name": "Name",
                "diffuser_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": individual.id,
                            "diffuser_role_id": role.id,
                            "email": "test@email.com",
                            "mobile": "0123456789",
                            "phone": "123",
                        },
                    )
                ],
            }
        )
        f = Form(self.env["project.project"])
        f.name = "Project"
        f.show_place_id = show_place
        project = f.save()
        generated_diffuser = project.diffuser_ids[0]
        self.assertEqual(generated_diffuser.partner_id, show_place.diffuser_ids[0].partner_id)
        self.assertEqual(
            generated_diffuser.diffuser_role_id,
            show_place.diffuser_ids[0].diffuser_role_id,
        )
        self.assertEqual(generated_diffuser.email, show_place.diffuser_ids[0].email)
        self.assertEqual(generated_diffuser.mobile, show_place.diffuser_ids[0].mobile)
        self.assertEqual(generated_diffuser.phone, show_place.diffuser_ids[0].phone)

    def test_onchange_set_show_info(self):
        partner_id = self.env["res.partner"].create({"name": "Partner", "is_company": True})
        analytic_account_id = self.env['account.analytic.account'].create({
            'name': 'Analytic Account',
            'code': partner_id.vat,
            'partner_id': partner_id.id,
        })
        self.tour_project_1.artist_id = self.artist2.id
        self.tour_project_1.analytic_account_id = analytic_account_id.id
        self.show_project_1.parent_id = self.tour_project_1.id
        self.show_project_1._onchange_set_show_info()
        assert self.show_project_1.artist_id == self.tour_project_1.artist_id
        assert self.show_project_1.analytic_account_id == self.tour_project_1.analytic_account_id

    def _create_project_with_form(self, values):
        with Form(self.env["project.project"]) as project_form:
            for k, v in values.items():
                setattr(project_form, k, v)
        return project_form

