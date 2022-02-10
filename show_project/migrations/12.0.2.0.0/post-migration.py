# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    domain = [("show_type", "=", "show"), ("show_place_id", "!=", False)]
    for project in env["project.project"].search(domain):
        _propagate_configuration_from_show_place(project)


def _propagate_configuration_from_show_place(project):
    _logger.info(f"Updating show configuration of project {project.id}")
    place = project.show_place_id
    config = place.show_configuration_ids[:1]
    project.write(
        {
            "show_place_configuration_id": config.id,
            "show_place_configuration": config.name,
            "show_place_distance_from_productor": place.show_place_distance_from_productor,
            "show_place_stage": place.show_place_stage,
            "show_place_maximum_capacity": config.maximum_capacity,
            "show_place_minor_restriction": config.minor_restriction,
        }
    )
