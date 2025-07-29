# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Recording Languages',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Recording',
    'summary': 'Languages management for the recording application.',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/recording_language.xml',
    ],
    'demo': [
        'demo/recording_language.xml',
    ],
    'installable': True,
}
