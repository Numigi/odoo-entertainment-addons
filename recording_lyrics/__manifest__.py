# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Recording Lyrics',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Recording',
    'summary': 'Languages management for the recording application.',
    'depends': [
        'recording',
        'recording_lang',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/recording.xml',
    ],
    'installable': True,
}
