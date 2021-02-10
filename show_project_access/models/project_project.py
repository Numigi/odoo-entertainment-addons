# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError

ACCESS_ERROR_MESSAGE = _(
    "You are not allowed to create or edit projects of type show and tour."
)


class Project(models.Model):

    _inherit = "project.project"

    def check_extended_security_create(self):
        super().check_extended_security_create()

        restricted_projects = self.filtered(lambda p: p.show_type in ("tour", "show"))

        if not self.env.user.is_show_manager and restricted_projects:
            raise AccessError(ACCESS_ERROR_MESSAGE)

    def check_extended_security_write(self):
        super().check_extended_security_write()

        restricted_projects = self.filtered(lambda p: p.show_type in ("tour", "show"))

        if not self.env.user.is_show_manager and restricted_projects:
            raise AccessError(ACCESS_ERROR_MESSAGE)
