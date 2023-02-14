# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Show Project",
    "summary": "Show Project",
    "version": "2.0.4",
    "website": "https://bit.ly/numigi-com",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        # Numigi-Project
        "project_iteration",
        "project_form_with_dates",
        "project_type",
        # OCA-server-tool
        "base_view_inheritance_extension",
        # Numigi-Entertainment
        "artist",
        "show_place",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project_diffuser.xml",
        "views/project_project.xml",
    ],
}
