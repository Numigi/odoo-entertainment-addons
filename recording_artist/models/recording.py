# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Recording(models.Model):

    _inherit = 'recording'

    artist_id = fields.Many2one('artist', 'Artist', ondelete='restrict')
    secondary_artist_id = fields.Many2one('artist', 'Secondary Artist', ondelete='restrict')
    record_company_id = fields.Many2one('recording.company')
