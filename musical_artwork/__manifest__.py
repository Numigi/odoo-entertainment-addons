# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Musical Artwork',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Entertainment',
    'summary': 'Manage musical artwork',
    'depends': [
        'contacts',
        'recording',
        'recording_lang',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/musical_artwork.xml',
        'views/recording.xml',
        'views/musical_artwork_role.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/musical_artwork_role.xml',
        'demo/musical_artwork.xml',
    ],
    'installable': True,
}
