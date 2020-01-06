# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Main Module',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Install all addons required for testing.',
    'depends': [
        'artist',
        'artist_url_link',
        'musical_artwork',  # TA#16242
        'recording',
        'recording_artist',
        'recording_contributor',
        'recording_genre',
        'recording_lang',
        'recording_musical_artwork',
        'recording_subgenre',
        'recording_tag',
        'recording_url_link',
        'recording_version',
        'show_place',
    ],
    'installable': True,
}
