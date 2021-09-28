# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class MusicalArtworkDistributionLine(models.Model):
    _inherit = 'musical.artwork.distribution.line'

    musical_artwork_title = fields.Char(related="distribution_id.musical_artwork_id.title", store=True)
