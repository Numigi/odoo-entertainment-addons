# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Artist',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Entertainment',
    'summary': 'Manage artists',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/artist.xml',
        'views/artist_role.xml',
        'views/artist_tag.xml',
    ],
    'installable': True,
    'demo': [
        'demo/artist.xml',
    ]
}
