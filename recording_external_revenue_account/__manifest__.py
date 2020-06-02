# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Recording External Revenue Account",
    "tag": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Recording",
    "summary": "Generate journal entries for external revenue of recording.",
    "depends": [
        "recording_external_revenue",
        "onchange_helper",
    ],
    "data": [
        "views/menu.xml",
    ],
    "installable": True,
}
