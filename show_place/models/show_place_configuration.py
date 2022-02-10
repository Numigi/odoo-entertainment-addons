# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ShowPlaceConfiguration(models.Model):

    _name = 'show.place.configuration'
    _description = 'Show Place Configuration'

    name = fields.Char(string='Name', translate=True)
    description = fields.Text(string='Description', translate=True)
    active = fields.Boolean(string='Active', default=True)
