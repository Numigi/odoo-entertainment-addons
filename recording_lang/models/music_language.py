# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MusicLanguage(models.Model):

    _name = 'music.language'
    _description = 'Language'

    name = fields.Char(string='Name', required=1)
    code = fields.Char(string='Code', required=1)
    active = fields.Boolean(default=True)
