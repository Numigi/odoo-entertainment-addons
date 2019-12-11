# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Recording Show',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Recording',
    'summary': 'Shows Places Types/Configuration',
    'depends': ['contacts', 'sales_team', 'product'],
    'data': ['security/ir.model.access.csv',
             'views/show_place_views.xml',
             'views/res_partner_views.xml'],
    'installable': True,
}
