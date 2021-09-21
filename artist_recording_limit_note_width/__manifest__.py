# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Artist Recording Limit Note Width',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Artist',
    'summary': 'Limits the note field width in artists and recordings menus.',
    'depends': [
        'artist_url_link',
        'recording_url_link',
        'web_list_column_width',
    ],
    'data': [
        'views/artist.xml',
        'views/recording.xml',
    ],
    'installable': True,
}
