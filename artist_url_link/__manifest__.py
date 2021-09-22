# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Artist URL Links',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Artist',
    'summary': 'Add URL links to artists',
    'depends': [
        'artist',
        'url_link_type',
        'web_list_column_width',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/artist.xml',
    ],
    'installable': True,
}
