# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Show Project",
    "summary": "Show Project",
    "version": "12.0.1.0.0",
    "website": "https://bit.ly/numigi-com",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        # Numigi-Project
        "project_iteration",
        "project_form_with_dates",
        # OCA-server-tool
        "base_view_inheritance_extension",
        # Numigi-Entertainment
        "show_place",
    ],
    "data": [
        # Views
        "views/project_project.xml",

        # Security
        "security/res_groups.xml",
        "security/ir_rule.xml",
    ],
}
