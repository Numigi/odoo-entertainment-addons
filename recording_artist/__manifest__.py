# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Recording Artist",
    "version": "1.1.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Entertainment",
    "summary": "Add artists to the recording application",
    "depends": [
        "artist",
        "recording",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/recording.xml",
        "views/recording_company.xml",
        "views/artist.xml",
        "views/menu.xml",
    ],
    "installable": True,
    "auto_install": True,
    "demo": [
        "demo/artist.xml",
    ]
}
