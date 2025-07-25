# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Recording(models.Model):

    _inherit = 'recording'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        ondelete="restrict"
    )
