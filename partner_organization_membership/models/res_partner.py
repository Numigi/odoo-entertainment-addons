# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ResPartner(models.Model):

    _inherit = "res.partner"

    is_artist = fields.Boolean(string="Artist / Musician", prefetch=False)
    artisti = fields.Char(string="ARTISTI", prefetch=False)
    guilde = fields.Char(string="GUILDE", prefetch=False)
    sacem = fields.Char(string="SACEM", prefetch=False)
    socan = fields.Char(string="SOCAN", prefetch=False)
    sodrac = fields.Char(string="SODRAC", prefetch=False)
    sound_ex = fields.Char(string="SOUND EX.", prefetch=False)
    soproq = fields.Char(string="SOPROQ", prefetch=False)
    spacq = fields.Char(string="SPACQ", prefetch=False)
    uda = fields.Char(string="UDA", prefetch=False)
    organization_ids = fields.One2many(
        "res.partner.organization",
        "partner_id",
        string="Other Organizations",
        prefetch=False,
    )
    isni = fields.Char(string="ISNI", prefetch=False)
    ipi = fields.Char(string="IPI", prefetch=False)
    ipn = fields.Char(string="IPN", prefetch=False)
    is_canadian_artist = fields.Boolean(string="Canadian Artist", prefetch=False)
    is_resident_qc = fields.Boolean(string="Resident of Quebec", prefetch=False)
    is_emerging_artist = fields.Boolean(string="Emerging Artist", prefetch=False)
    is_closm = fields.Boolean(string="CLOSM", prefetch=False)
    is_autochthon = fields.Boolean(string="Autochthon", prefetch=False)
    is_visible_minority = fields.Boolean(string="Visible Minority", prefetch=False)
    birth_city_id = fields.Many2one(
        "res.partner.birth.city", string="City of Birth", prefetch=False
    )

    @api.onchange("company_type", "is_artist")
    def _onchange_company_type(self):
        """Change company type."""
        if self.company_type == "company":
            self.is_artist = False

        if not self.is_artist:
            self.artisti = False
            self.guild = False
            self.sacem = False
            self.socan = False
            self.sodrac = False
            self.sound_ex = False
            self.soproq = False
            self.spacq = False
            self.uda = False
            self.organization_ids = False
            self.isni = False
            self.ipi = False
            self.ipn = False
            self.is_canadian_artist = False
            self.is_resident_qc = False
            self.is_emerging_artist = False
            self.is_closm = False
            self.is_autochthon = False
            self.is_visible_minority = False
            self.birth_city_id = False


class ResPartnerOrganization(models.Model):

    _name = "res.partner.organization"
    _description = "Other Management Organizations"

    name = fields.Char(string="Name", required="1")
    number = fields.Char(string="Member Number", required=1)
    partner_id = fields.Many2one("res.partner", string="Partner")
