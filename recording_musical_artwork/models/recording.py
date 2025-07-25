# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RecordingMusicalArtwork(models.Model):

    _inherit = 'recording'

    musical_artwork_id = fields.Many2one(
        'musical.artwork',
        ondelete='restrict',
        string='Related Artwork',
    )
