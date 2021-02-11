# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError

ACCESS_ERROR_MESSAGE = _(
    "You are not allowed to create or edit tasks in projects of type show and tour."
)


class Task(models.Model):

    _inherit = "project.task"

    def check_extended_security_create(self):
        super().check_extended_security_create()

        restricted_tasks = self.filtered(
            lambda t: t.project_id.show_type in ("tour", "show")
        )

        if not self.env.user.is_show_manager and restricted_tasks:
            raise AccessError(ACCESS_ERROR_MESSAGE)

    def check_extended_security_write(self):
        super().check_extended_security_write()

        restricted_tasks = self.filtered(
            lambda t: t.project_id.show_type in ("tour", "show")
        )

        if not self.env.user.is_show_manager and restricted_tasks:
            raise AccessError(ACCESS_ERROR_MESSAGE)
