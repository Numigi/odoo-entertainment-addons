# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Project(models.Model):

    _inherit = "project.project"

    gmmq_main_artist_base_id = fields.Many2one(
        "hr.contribution.base",
        "GMMQ Base For Main Artist",
        domain=[("is_gmmq", "=", True)],
        ondelete="restrict",
    )

    gmmq_other_artist_base_id = fields.Many2one(
        "hr.contribution.base",
        "GMMQ Base For Accompanying Artists",
        domain=[("is_gmmq", "=", True)],
        ondelete="restrict",
    )

    uda_base_id = fields.Many2one(
        "hr.contribution.base",
        "UDA Base",
        domain=[("is_uda", "=", True)],
        ondelete="restrict",
    )

    show_contribution_ids = fields.One2many(
        "project.show.contribution",
        "project_id",
        "Contributions",
    )

    def compute_show_contributions(self):
        self.show_contribution_ids = None
        for partner in self.mapped("show_member_ids.partner_id"):
            self._create_show_contributions(partner)

    def _create_show_contributions(self, partner):
        vals_list = []

        vals_list.extend(self._iter_uda_contribution_vals(partner))
        vals_list.extend(self._iter_gmmq_contribution_vals(partner))

        self.write({"show_contribution_ids": [(0, 0, vals) for vals in vals_list]})

    def _iter_uda_contribution_vals(self, partner):
        base = self.uda_base_id

        for type_ in base.register_id.type_ids:
            vals = self._get_show_contribution_values(partner, base, type_)
            yield vals

    def _iter_gmmq_contribution_vals(self, partner):
        base = self.gmmq_main_artist_base_id

        for type_ in base.register_id.type_ids:
            vals = self._get_show_contribution_values(partner, base, type_)
            yield vals

    def _get_show_contribution_values(self, partner, base, type_):
        return {
            "partner_id": partner.id,
            "base_amount": base.amount,
            "code": type_.code,
            "register_id": base.register_id.id,
        }
