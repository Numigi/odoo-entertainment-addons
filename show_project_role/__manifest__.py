# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Show Project Role",
    "summary": "Add member roles for tour/show projects",
    "version": "1.1.1",
    "website": "https://bit.ly/numigi-com",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        # Numigi-entertainment
        "show_project",
        # Numigi-herpy
        "partner_organization_membership",
    ],
    "data": [
        # Security
        "security/ir.model.access.csv",
        # Views
        "views/project_project.xml",
        "views/project_show_role.xml",
        "views/menu.xml",
    ],
    "demo": [
        "demo/project.show.role.csv",
    ],
}
