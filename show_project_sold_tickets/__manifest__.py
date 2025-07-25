# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Show Project Sold Tickets",
    "summary": "Show Project Sold Tickets",
    "version": "12.0.1.1.2",
    "website": "https://numigi.com/r/home",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        # Numigi-entertainment
        "show_project",
        "show_project_sale",

    ],
    "data": [
        # Security
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        # Views
        "views/show_ticket_sold.xml",
        "views/project_project.xml",
        "views/menu.xml",
    ],
}
