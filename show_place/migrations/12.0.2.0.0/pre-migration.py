# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from openupgradelib.openupgrade import logged_query

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    columns = [
        "show_place_configuration_id",
        "show_place_maximum_capacity",
        "show_place_minor_restriction",
    ]
    for column in columns:
        logged_query(
            cr,
            f"""
            ALTER TABLE res_partner
            RENAME {column}
            TO legacy_{column};
            """,
        )
