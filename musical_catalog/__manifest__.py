# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Musical Catalogs',
    'version': '1.1.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Recording',
    'summary': 'Add musical catalogs as a model.',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/musical_catalog.xml',
    ],
    'demo': ["demo/demo.xml"],
    'installable': True,
}
