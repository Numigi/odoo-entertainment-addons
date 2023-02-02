# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Show Project Fee",
    "summary": "Add management of show fees on projects",
    "version": "1.1.1",
    "website": "https://bit.ly/numigi-com",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["show_project", "show_project_role", "show_project_sale", "project_type"],
    "data": ["views/project_project.xml", "security/ir.model.access.csv"],
}
