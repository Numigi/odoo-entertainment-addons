# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ShowPlaceType(models.Model):

    _name = 'show.place.type'
    _description = 'Shows Places Types'

    name = fields.Char(string='Name', required=1, translate=True)
    active = fields.Boolean(string='Active', default=True)


class ShowPlaceConfiguration(models.Model):

    _name = 'show.place.configuration'
    _description = 'Place Configuration'

    name = fields.Char(string='Name', required=1, translate=True)
    description = fields.Text(string='Description', translate=True)
    active = fields.Boolean(string='Active', default=True)
