# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Show Appearance Type",
    "summary": "Add new object Show Appearance Type and new field Appearance Type on Project",
    "version": "1.0.0",
    "website": "https://numigi.com/r/home",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["show_project"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_project.xml",
        "views/show_appearance_type.xml",
    ],
}
