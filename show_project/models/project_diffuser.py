# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectDiffuser(models.Model):

    _name = "project.diffuser"
    _inherit = ["diffuser.mixin"]
    _description = "Project Diffuser"

    project_id = fields.Many2one("project.project", required=True, ondelete="cascade")
