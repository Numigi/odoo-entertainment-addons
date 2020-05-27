# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Recording Platforms",
    "type": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Recording",
    "summary": "Platforms for the recording application.",
    "depends": ["recording",],
    "data": [
        "security/ir.model.access.csv",
        "views/recording_platform.xml",
        "views/recording_subplatform.xml",
        "views/menu.xml",
    ],
    "demo": ["demo/demo.xml"],
    "installable": True,
}
