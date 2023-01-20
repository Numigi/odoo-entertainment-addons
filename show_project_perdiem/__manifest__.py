# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Show Project Per Diem",
    "summary": "Add perdiems on shows",
    "version": "1.1.2",
    "website": "https://bit.ly/numigi-com",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "show_project",
        "show_project_role",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project_perdiem_type.xml",
        "views/project_project.xml",
        "views/menu.xml",
    ],
    "demo": [
        "demo/project.perdiem.type.csv",
    ],
}
