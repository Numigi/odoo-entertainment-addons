# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ResPartner(models.Model):

    _inherit = 'res.partner'

    is_artist = fields.Boolean(string="Artist/Musician")
    artisti = fields.Char(string="ARTISTI")
    guild = fields.Char(string="GUILD")
    sacem = fields.Char(string="SACEM")
    socan = fields.Char(string="SOCAN")
    sodrac = fields.Char(string="SODRAC")
    sound_ex = fields.Char(string="SOUND EX.")
    soproq = fields.Char(string="SOPROQ")
    spacq = fields.Char(string="SPACQ")
    uda = fields.Char(string="UDA")
    organization_ids = fields.One2many('res.partner.organization', 'partner_id', string="Other organizations")
    isni = fields.Char(string="ISNI")
    ipi = fields.Char(string="IPI")
    ipn = fields.Char(string="IPN")
    is_canadian_artist = fields.Boolean(string="Canadian artist")
    is_resident_qc = fields.Boolean(string="Resident of Quebec")
    is_emerging_artist = fields.Boolean(string="Emerging artist")
    is_closm = fields.Boolean(string="CLOSM")
    is_autochthon = fields.Boolean(string="Autochthon")
    is_visible_minority = fields.Boolean(string="Visible minority")
    birth_city_id = fields.Many2one('res.partner.birth.city', string="City of birth")

    @api.onchange('company_type', 'is_artist')
    def _onchange_company_type(self):
        """Change company type."""
        if self.company_type == 'company':
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

    _name = 'res.partner.organization'
    _description = 'Other Management Organizations'

    name = fields.Char(string="Name", required='1')
    number = fields.Char(string="Member number", required=1)
    partner_id = fields.Many2one('res.partner', string="Partner")
