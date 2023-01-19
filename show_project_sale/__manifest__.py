# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Show Project Sale",
    "version": "1.1.4",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Entertainment",
    "summary": "Add sale information on project show type",
    "depends": [
        "show_project",
        "show_sale",
    ],
    "data": [
        # security
        "security/ir.model.access.csv",
        # views
        "views/project_project.xml",
        "views/project_service_fee.xml",
        "views/project_ticket_price.xml",
    ],
    "installable": True,
}
