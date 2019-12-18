# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Recording Subkinds',
    'type': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Recording',
    'summary': 'Subkinds for the recording application.',
    'depends': [
        'recording_kind',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/recording_subkind.xml',
        'views/recording.xml',
        'views/menu.xml',
    ],
    'installable': True,
}
