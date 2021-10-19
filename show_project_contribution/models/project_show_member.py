# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectShowMember(models.Model):

    _inherit = "project.show.member"

    gmmq = fields.Boolean("GMMQ")
    uda = fields.Boolean("UDA")
    coefficient = fields.Float(default=1)

    @api.onchange("role_id")
    def onchange_role_id(self):
        super().onchange_role_id()
        self.gmmq = self.role_id.gmmq
        self.uda = self.role_id.uda
        self.coefficient = self.role_id.coefficient

