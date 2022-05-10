# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Show Place",
    "version": "2.0.1",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Entertainment",
    "summary": "Add Show Place Types/Configuration",
    "depends": ["contacts", "partner_contact_type_visible", "sales_team", "project"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner.xml",
        "views/res_partner_diffuser.xml",
        "views/show_place_configuration.xml",
        "views/show_place_type.xml",
        "views/diffuser_role.xml",
    ],
    "installable": True,
}
