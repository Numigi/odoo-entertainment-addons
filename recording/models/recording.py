# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Recording(models.Model):

    _name = 'recording'
    _description = 'Recording'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)

    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda s: s.env.user.company_id
    )
