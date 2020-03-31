# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Recording External Revenue',
    'tag': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Recording',
    'summary': 'Manage external revenue of recording.',
    'depends': [
        'recording',
    ],
    'data': [
        'views/recording_external_revenue.xml',
        'views/menu.xml',

        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    'installable': True,
}
