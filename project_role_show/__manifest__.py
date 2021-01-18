# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Project Role Show",
    "summary": "Project Role Show",
    "version": "12.0.1.0.0",
    "website": "https://bit.ly/numigi-com",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        # Numigi-entertainment
        "show_project",
    ],
    "data": [
        # Security
        "security/ir.model.access.csv",

        # Views
        "views/project_tour_role.xml",
        "views/menu.xml",
    ],
}
