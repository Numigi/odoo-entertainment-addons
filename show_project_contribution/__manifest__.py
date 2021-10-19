# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Show Project Contribution",
    "summary": "Add employee contributions on shows",
    "version": "1.0.0",
    "website": "https://bit.ly/numigi-com",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "hr_payroll",
        "show_project",
        "show_project_role",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/hr_contribution_register.xml",
        "views/hr_contribution_base.xml",
        "views/hr_contribution_type.xml",
        "views/hr_employee.xml",
        "views/project_project.xml",
        "views/menu.xml",
    ],
    "demo": [
        "demo/hr.contribution.type.csv",
        "demo/hr.contribution.base.csv",
    ],
}
