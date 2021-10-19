# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectShowMember(models.Model):

    _inherit = "project.show.member"

    gmmq = fields.Boolean()
    uda = fields.Boolean()
    main_artist = fields.Boolean()
    coefficient = fields.Float(default=1)
