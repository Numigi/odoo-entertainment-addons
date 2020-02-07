# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Product Musical Relation',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Entertainment',
    'summary': 'Add relation between product and records.',
    'depends': [
        'recording',
        'artist',
        'product',
        'musical_catalog',
    ],
    'data': [
        "views/product_template.xml",
        "views/recording.xml",
    ],
    'installable': True,
}
