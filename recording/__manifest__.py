# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Recording',
    'version': '1.4.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Entertainment',
    'summary': 'The base module for the recording application',
    'depends': [
        'base',
        'mail',
        'recording_lang',
        'musical_catalog',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/recording.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/recording.xml',
    ],
    'installable': True,
    'application': True,
}
