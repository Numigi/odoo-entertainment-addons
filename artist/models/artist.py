# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Artist(models.Model):

    _name = 'artist'
    _description = 'Artist'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda s: s.env.user.company_id
    )

    partner_id = fields.Many2one('res.partner', ondelete='restrict', index=True)

    isni = fields.Char(
        string='ISNI',
        help="International Standard Name Identifier (ISO 27729)"
    )

    tag_ids = fields.Many2many(
        'artist.tag',
        'artist_tag_rel',
        'artist_id',
        'tag_id',
        'Tags',
    )

    website = fields.Char()
    note = fields.Text()

    member_ids = fields.One2many(
        'artist.member', 'artist_id', 'Members',
        context={"active_test": False}
    )
