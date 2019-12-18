# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Recording / Musical Artwork',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Entertainment',
    'summary': 'Binding between recordings and musical artworks',
    'depends': [
        'musical_artwork',
        'recording',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/musical_artwork.xml',
        'views/recording.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/recording.xml',
    ],
    'installable': True,
}
