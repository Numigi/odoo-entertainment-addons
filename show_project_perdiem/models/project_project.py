# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Project(models.Model):

    _inherit = "project.project"

    tour_perdiem_config_ids = fields.One2many(
        "project.tour.perdiem.config",
        "project_id",
        "Configuration of Tour Per Diem",
    )

    show_perdiem_config_ids = fields.One2many(
        "project.show.perdiem.config",
        "project_id",
        "Configuration of Show Per Diem",
    )

    show_perdiem_ids = fields.One2many(
        "project.show.perdiem",
        "project_id",
        "Show Per Diem",
    )
    show_perdiem_note = fields.Text(string="Notes")

    @api.constrains("tour_perdiem_config_ids")
    def _check_duplicate_tour_perdiems(self):
        for project in self:
            types = project.mapped("tour_perdiem_config_ids.type_id")
            if len(types) != len(project.tour_perdiem_config_ids):
                raise ValidationError(_(
                    "You may not select multiple applicable per diem "
                    "of the same type."
                ))

    @api.constrains("show_perdiem_config_ids")
    def _check_duplicate_show_perdiems(self):
        for project in self:
            types = project.mapped("show_perdiem_config_ids.type_id")
            if len(types) != len(project.show_perdiem_config_ids):
                raise ValidationError(_(
                    "You may not select multiple applicable per diem "
                    "of the same type."
                ))

    def compute_show_perdiems(self):
        self.show_perdiem_ids = None

        for (
            tour_config,
            show_config,
            partner,
        ) in self._iter_perdiem_compute_parameters():
            vals = self._get_show_perdiem_vals(tour_config, show_config, partner)
            self._create_show_perdiem(vals)

    def _iter_perdiem_compute_parameters(self):
        for partner in self.mapped("show_member_ids.partner_id"):
            for show_config in self.show_perdiem_config_ids:
                tour_config = self._get_tour_perdiem_config(show_config)
                yield tour_config, show_config, partner

    def _get_tour_perdiem_config(self, show_config):
        type_ = show_config.type_id
        tour = self.parent_id

        tour_config = next(
            (p for p in tour.tour_perdiem_config_ids if p.type_id == type_),
            None,
        )

        if tour_config is None:
            raise ValidationError(
                _(
                    "The type of perdiem {perdiem_type} is not defined "
                    "on the parent tour ({tour})."
                ).format(perdiem_type=type_.display_name, tour=tour.display_name)
            )

        return tour_config

    def _create_show_perdiem(self, vals):
        self.write({"show_perdiem_ids": [(0, 0, vals)]})

    def _get_show_perdiem_vals(self, tour_config, show_config, partner):
        return {
            "partner_id": partner.id,
            "quantity": show_config.quantity,
            "type_id": show_config.type_id.id,
            "unit_amount": tour_config.unit_amount,
        }
