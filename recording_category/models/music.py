# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MusicType(models.Model):

    _name = 'music.type'
    _description = 'Genre'

    name = fields.Char(string='Genre', required=1)
    active = fields.Boolean(string='Active', default=True)


class MusicSubtype(models.Model):
    _name = 'music.subtype'
    _description = 'Subgenre'

    name = fields.Char(string='Subgenre', required=1)
    active = fields.Boolean(string='Active', default=True)


class MusicTag(models.Model):
    _name = 'music.tag'
    _description = 'Tag'

    name = fields.Char(string='Name', required=1)
    active = fields.Boolean(string='Active', default=True)
    parent_category_id = fields.Many2one('music.tag', string="Parent Category")
