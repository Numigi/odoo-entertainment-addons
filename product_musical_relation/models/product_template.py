# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.addons.recording.models.recording import SOUND, GROUP


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    musical_relation = fields.Selection(
        [(SOUND, 'Sound Record'), (GROUP, 'Grouping of Records')],
        string='Musical Relation',
    )
    recording_id = fields.Many2one('recording', 'Recording', ondelete='restrict')
    artist_id = fields.Many2one('artist', 'Artist', ondelete='restrict')

    recording_release_date = fields.Date(
        related='recording_id.release_date',
    )
    sale_date = fields.Date()
    commercialization_date = fields.Date()

    catalogue_reference = fields.Char(
        related='recording_id.catalogue_reference',
    )

    musical_catalog_reference_ids = fields.One2many(
        'musical.catalog.reference',
        'product_template_id',
        'External Catalog References',
    )

    @api.onchange('musical_relation')
    def _empty_record_id(self):
        """ When the selection in musical relation change, the field record_id
        is emptied to guide the user to select a new record
        """
        self.recording_id = False

    @api.onchange('recording_id')
    def _set_artist_id(self):
        self.artist_id = self.recording_id.artist_id

    @api.model
    def create(self, vals):
        product = super().create(vals)
        if product.recording_id:
            product._propagate_artist_from_recording()
        return product

    @api.multi
    def write(self, vals):
        super().write(vals)
        if 'recording_id' in vals:
            products_with_recording = self.filtered(lambda p: p.recording_id)
            for product in products_with_recording:
                product._propagate_artist_from_recording()
        return True

    def _propagate_artist_from_recording(self):
        if self.artist_id != self.recording_id.artist_id:
            self.artist_id = self.recording_id.artist_id
