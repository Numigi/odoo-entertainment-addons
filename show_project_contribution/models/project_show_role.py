# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectShowRole(models.Model):

    _inherit = "project.show.role"

    gmmq = fields.Boolean()
    uda = fields.Boolean()
    coefficient = fields.Float(default=1)
