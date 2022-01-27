# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectServiceFee(models.Model):

    _name = "project.service.fee"
    _inherit = "project.price.mixin"
    _description = "Project Service Fee"
