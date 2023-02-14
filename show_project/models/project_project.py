# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    show_type = fields.Selection(
        selection=[("standard", "Standard"), ("tour", "Tour"), ("show", "Show")],
        default="standard",
    )
    showcase = fields.Boolean()
    formula = fields.Char()
    show_date = fields.Date()
    expected_parent_show_type = fields.Char(
        compute="_compute_expected_parent_show_type", store=True
    )
    parent_id = fields.Many2one(
        string="Tour", domain="[('show_type', '=', expected_parent_show_type)]"
    )
    show_place_id = fields.Many2one(
        comodel_name="res.partner",
        domain="[('type', '=', 'show_site')]",
        string="Venue",
    )
    show_place_configuration_id = fields.Many2one(
        "res.partner.show.configuration",
        ondelete="set null",
        domain="[('partner_id', '=', show_place_id)]",
    )
    show_place_maximum_capacity = fields.Integer(string="Maximum Capacity")
    show_place_configuration = fields.Char(string="Configuration of Room")
    show_place_minor_restriction = fields.Boolean(string="Minors Restriction")
    show_place_distance_from_productor = fields.Integer(
        string="Distance from Productor"
    )
    show_place_stage = fields.Selection([("indoor", "Indoor"), ("outdoor", "Outdoor")])
    show_place_notes = fields.Text()
    previous_show_id = fields.Many2one(
        comodel_name="project.project", compute="_compute_previous_and_next_show_id"
    )
    next_show_id = fields.Many2one(
        comodel_name="project.project", compute="_compute_previous_and_next_show_id"
    )

    recording = fields.Boolean(default=False)
    producer_id = fields.Many2one(comodel_name="res.partner")
    city = fields.Char(related="show_place_id.city", store=True)
    diffuser_ids = fields.One2many(
        "project.diffuser", "project_id", string="Diffuser's Contacts"
    )
    artist_id = fields.Many2one(comodel_name="artist")

    @api.depends("show_type")
    def _compute_expected_parent_show_type(self):
        for project in self:
            parent_show_type = ""
            if project.show_type == "standard":
                parent_show_type = "standard"
            elif project.show_type == "show":
                parent_show_type = "tour"
            project.expected_parent_show_type = parent_show_type

    @api.depends(
        "parent_id",
        "parent_id.child_ids",
        "parent_id.child_ids.show_date",
        "show_type",
        "show_date",
    )
    def _compute_previous_and_next_show_id(self):
        for project in self:
            if project.show_type == "show" and project.show_date:
                show_projects = (project.parent_id.child_ids - project).filtered(
                    lambda r: r.show_date
                )
                previous_show_projects = show_projects.filtered(
                    lambda r: r.show_date <= project.show_date
                )
                next_show_projects = show_projects.filtered(
                    lambda r: r.show_date >= project.show_date
                )
                if previous_show_projects:
                    project.previous_show_id = previous_show_projects.sorted(
                        "show_date", reverse=True
                    )[0]
                else:
                    project.previous_show_id = False
                if next_show_projects:
                    project.next_show_id = next_show_projects.sorted("show_date")[0]
                else:
                    project.next_show_id = False
            else:
                project.previous_show_id = False
                project.next_show_id = False

    @api.model
    def create(self, vals):
        vals = self._set_show_type_vals(vals)
        return super(ProjectProject, self).create(vals)

    @api.multi
    def write(self, vals):
        vals = self._set_show_type_vals(vals)
        return super(ProjectProject, self).write(vals)

    @api.onchange("show_type", "parent_id", "show_date", "show_place_id", "parent_id.artist_id",
                  "parent_id.analytic_account_id")
    def _onchange_set_show_info(self):
        if self.show_type == "show":
            values = [
                fields.Date.to_string(self.show_date),
                self.show_place_id.display_name,
            ]
            values = filter(lambda x: x, values)
            self.name = " - ".join(values)
            if self.parent_id.artist_id:
                self.artist_id = self.parent_id.artist_id.id
            if self.parent_id.analytic_account_id:
                self.analytic_account_id = self.parent_id.analytic_account_id.id

    @api.model
    def _set_show_type_vals(self, vals):
        # If project type is `tour`, parent_id should be False
        if vals.get("show_type") == "tour":
            vals.update({"parent_id": False})
        return vals

    @api.onchange("show_place_id")
    def _onchange_show_place_id(self):
        if self.show_place_id:
            self._update_from_show_place()

        if self.show_place_configuration_id.partner_id != self.show_place_id:
            self.show_place_configuration_id = None

    @api.onchange("show_place_configuration_id")
    def _onchange_show_place_configuration_id(self):
        config = self.show_place_configuration_id
        self.show_place_configuration = config.name
        self.show_place_maximum_capacity = config.maximum_capacity
        self.show_place_minor_restriction = config.minor_restriction

    @api.onchange('partner_id', 'show_type')
    def _onchange_partner_id(self):
        res = super(ProjectProject, self)._onchange_partner_id()
        if self.show_type in ('show', 'tour'):
            res['domain']['analytic_account_id'] = []
        return res

    def _update_from_show_place(self):
        place = self.show_place_id
        self.show_place_distance_from_productor = (
            place.show_place_distance_from_productor
        )
        self.show_place_stage = place.show_place_stage
        self.show_place_notes = place.show_place_notes
        self.diffuser_ids = self._get_diffuser_vals()

    def _get_diffuser_vals(self):
        diffuser_ids_vals = [(5, 0, 0)]
        for diffuser in self.show_place_id.diffuser_ids:
            diffuser_ids_vals.append(
                (
                    0,
                    0,
                    {
                        "partner_id": diffuser.partner_id.id,
                        "diffuser_role_id": diffuser.diffuser_role_id.id,
                        "email": diffuser.email,
                        "mobile": diffuser.mobile,
                        "phone": diffuser.phone,
                    },
                )
            )
        return diffuser_ids_vals
