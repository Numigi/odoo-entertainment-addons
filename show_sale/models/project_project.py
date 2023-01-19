# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class Project(models.Model):
    _inherit = "project.project"

    show_sale_order_ids = fields.One2many(
        "sale.order",
        "show_project_id",
    )

    show_sale_order_count = fields.Integer(compute="_compute_show_sale_order_count")
    check_so_exist = fields.Boolean(compute="_compute_check_so_exist", store=False)

    def _compute_show_sale_order_count(self):
        for project in self:
            project.show_sale_order_count = len(project.show_sale_order_ids)

    @api.multi
    @api.depends("show_sale_order_ids", "show_sale_order_ids.state")
    def _compute_check_so_exist(self):
        for p in self:
            p.check_so_exist = (
                    len(p.show_sale_order_ids.filtered(lambda s: s.state != "cancel")) > 0
            )

    @api.multi
    def action_create_sale_order_show(self):
        self.ensure_one()
        SaleOrderType = self.env["sale.order.type"]
        type_id = SaleOrderType.search(
            [("is_show", "=", True),
             ('company_id', 'in', [self.env.user.company_id.id, False])]
            , limit=1)
        if not type_id:
            raise UserError(
                _(
                    "No Sale Type with Show option existing. Create one before using this function."
                )
            )
        context = self.env.context.copy()
        context.update(
            {
                "default_partner_id": self.partner_id.id if self.partner_id else False,
                "default_analytic_account_id": self.analytic_account_id.id
                if self.analytic_account_id
                else False,
                "default_show_project_id": self.ids[0],
                "default_type_id": type_id.ids[0],
            }
        )
        return {
            "name": _("Create Sale"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "context": context,
            "res_model": "sale.order",
            "target": "current",
        }
