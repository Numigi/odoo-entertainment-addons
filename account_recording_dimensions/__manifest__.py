# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Account Recording Dimensions',
    'tag': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Recording',
    'summary': 'Create link between acount move lines and recordings and artists.',
    'depends': [
        'recording_artist',
        'account'
    ],
    'data': [
        'views/account_move.xml',
        'views/account_move_line.xml',
    ],
    'installable': True,
}
