# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import threading

from odoo import api, fields, models, tools
from odoo.modules import get_module_resource


class ResPartner(models.Model):

    _inherit = "res.partner"

    type = fields.Selection(selection_add=[("show_site", "Show Site")])
    show_place_type_id = fields.Many2one(
        "show.place.type", string="Show Place Type", prefetch=False
    )
    show_place_notes = fields.Text(string="Show Place Notes", prefetch=False)
    show_place_distance_from_productor = fields.Integer(
        string="Distance from Productor", prefetch=False
    )
    show_place_stage = fields.Selection(
        [("indoor", "Indoor"), ("outdoor", "Outdoor")], prefetch=False
    )
    show_configuration_ids = fields.One2many(
        "res.partner.show.configuration", "partner_id", string="Show Configurations"
    )
    diffuser_ids = fields.One2many(
        "res.partner.diffuser", "inverse_partner_id", string="Diffuser's Contacts"
    )

    @api.model
    def _get_default_image(self, partner_type, is_company, parent_id):
        if getattr(threading.currentThread(), "testing", False) or self._context.get(
            "install_mode"
        ):
            return False
        if partner_type == "show_site" and not is_company:
            img_path = get_module_resource(
                "show_place", "static/img", "star_regular.png"
            )
            with open(img_path, "rb") as f:
                image = f.read()
            return tools.image_resize_image_big(base64.b64encode(image))
        return super()._get_default_image(partner_type, is_company, parent_id)
