# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MusicRecordContributor(models.Model):

    _name = 'music.record.contributor'
    _description = 'Recording role'

    name = fields.Char(string='Name', required=1)
    active = fields.Boolean(string='Active', default=True)
