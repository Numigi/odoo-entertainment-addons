# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProject(models.Model):

    _inherit = "project.project"

    show_sale_amount = fields.Monetary()

    show_fee_ids = fields.One2many("project.show.fee", "project_id", "Show Fees")
