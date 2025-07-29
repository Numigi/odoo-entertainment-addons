# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    show_appearance_type_id = fields.Many2one(
        "show.appearance.type",
        "Appearance Type",
        ondelete="restrict",
    )
