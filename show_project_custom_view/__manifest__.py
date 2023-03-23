# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Show Project Custom View",
    "version": "12.0.1.0.2",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Entertainment",
    "summary": "Change order of tabs and fields in the form view of project.",
    "depends": [
        "show_appearance_type",
        "show_place",
        "show_project_artwork",
        "show_project_fee",
        "show_project_perdiem",
        "show_project_promotion",
        "show_project_role",
        "show_project_sale",
        "hr_timesheet",
    ],
    "data": [
        # views
        "views/project_project_views.xml",

    ],
    "installable": True,
}
