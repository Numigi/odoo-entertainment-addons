# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Show Sale",
    "version": "1.1.2",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Entertainment",
    "summary": "Add sales orders of type show",
    "depends": ["sale_order_type", "show_project", "artist"],
    "data": [
        "security/ir.model.access.csv",
        "views/project.xml",
        "views/sale_order.xml",
        "views/sale_order_type.xml",
        "views/sale_order_type.xml",
        "views/show_customer_segment.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
