# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    for partner in env["res.partner"].search([("type", "=", "show_site")]):
        _make_default_configurations(partner)


def _make_default_configurations(partner):
    _logger.info(
        f"Creating default show configuration for partner {partner.id}"
    )
    vals = _get_default_configuration_vals(partner)
    partner.write({"show_configuration_ids": [(0, 0, vals)]})


def _get_default_configuration_vals(partner):
    partner._cr.execute(
        """
        SELECT
            legacy_show_place_configuration_id,
            legacy_show_place_maximum_capacity,
            legacy_show_place_minor_restriction
        FROM res_partner
        WHERE id = %s
        """,
        (partner.id,),
    )
    row = partner._cr.fetchone()
    config = partner.env["show.place.configuration"].browse(row[0])
    return {
        "name": config.name,
        "configuration_id": config.id,
        "maximum_capacity": row[1],
        "minor_restriction": row[2],
    }
