# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Show Place",
    "version": "1.1.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Entertainment",
    "summary": "Add Show Place Types/Configuration",
    "depends": ["contacts", "sales_team"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner.xml",
        "views/show_place_configuration.xml",
        "views/show_place_type.xml",
    ],
    "installable": True,
}
