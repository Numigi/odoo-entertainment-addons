# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from ..isrc import check_isrc_code
from odoo.exceptions import ValidationError

SOUND = 'sound'
VIDEO = 'video'
GROUP = 'group'


RECORDING_TYPES = (
    (SOUND, 'Sound'),
    (VIDEO, 'Video'),
    (GROUP, 'Group of Recordings'),
)


class Recording(models.Model):

    _name = 'recording'
    _description = 'Recording'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        required=True, string="Title",
        track_visibility="onchange",
    )
    active = fields.Boolean(
        default=True,
        track_visibility="onchange",
    )

    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda s: s.env.user.company_id,
    )

    ttype = fields.Selection(
        RECORDING_TYPES,
        string='Type of Recording',
        required=True,
        track_visibility="onchange",
        default=SOUND,
    )

    duration = fields.Float(
        track_visibility="onchange",
    )

    production_start_date = fields.Date(
        track_visibility="onchange",
    )

    publication_country_id = fields.Many2one(
        'res.country',
        string='Place of Publication',
        track_visibility="onchange",
    )

    note = fields.Text()

    release_date = fields.Date(
        track_visibility="onchange",
    )

    upc = fields.Char('UPC')
    upc_packshot = fields.Char('UPC Packshot')

    commercial_territory_id = fields.Many2one(
        'res.country.group',
        'Commercial Territory',
        ondelete='restrict',
    )

    catalogue_reference = fields.Char()

    musical_catalog_reference_ids = fields.One2many(
        'musical.catalog.reference',
        'recording_id',
        'External Catalog References',
    )

    _sql_constraints = [
        (
            'catalogue_reference', 'unique (catalogue_reference)',
            'The catalogue reference has to be unique.'
        ),
    ]


class RecordingWithISRC(models.Model):

    _inherit = 'recording'

    isrc = fields.Char('ISRC', size=12)

    other_isrc_ids = fields.One2many(
        'recording.other.isrc',
        'recording_id',
        'Other ISRC',
    )

    @api.constrains('isrc')
    def _check_isrc(self):
        records_with_isrc = self.filtered(lambda r: r.isrc)
        for record in records_with_isrc:
            check_isrc_code(record.isrc, record._context)


class RecordingSound(models.Model):

    _inherit = 'recording'

    video_recording_ids = fields.One2many(
        'recording',
        'sound_recording_id',
        'Video Recordings',
    )
    related_video_count = fields.Integer(
        compute='_compute_related_video_count'
    )

    def _compute_related_video_count(self):
        for rec in self:
            rec.related_video_count = self.env['recording'].search([
                ('sound_recording_id', '=', rec.id),
                ('ttype', '=', 'video'),
            ], count=True)

    related_group_count = fields.Integer(
        compute='_compute_related_group_count'
    )

    def _compute_related_group_count(self):
        for rec in self:
            rec.related_group_count = self.env['recording'].search([
                ('track_ids.recording_id', '=', rec.id),
                ('ttype', '=', 'group'),
            ], count=True)


class RecordingVideo(models.Model):

    _inherit = 'recording'

    sound_recording_id = fields.Many2one(
        'recording',
        track_visibility="onchange",
    )
    filming_location = fields.Char(
        track_visibility="onchange",
    )


class RecordingGroup(models.Model):

    _inherit = 'recording'

    group_type = fields.Selection([
        ('album', 'Album'),
        ('ep', 'EP'),
        ('single', 'Single'),
        ('compilation', 'Compilation'),
        ('split', 'Split'),
    ])

    track_ids = fields.One2many(
        'recording.track', 'recording_group_id', 'Related Recordings',
    )

    @api.constrains("track_ids")
    def _unique_couple_recording_group_recording(self):
        for record in self:
            recording_track_record = []

            for track in record.track_ids:

                if track.recording_id in recording_track_record:
                    raise ValidationError(
                        _(
                            'The recording "%s" has been selected twice in the list.'
                            ' It can be selected only once.'
                        ) % track.recording_id.name
                    )

                recording_track_record.append(track.recording_id)

    number_of_tracks = fields.Integer(
        string="Total Number of Tracks",
        compute='_compute_number_of_tracks'
    )

    def _compute_number_of_tracks(self):
        for rec in self:
            rec.number_of_tracks = len(rec.track_ids)

    group_duration = fields.Float(
        string="Group Duration",
        compute='_compute_group_duration',
        store=True,
    )

    @api.depends('track_ids.recording_id.duration')
    def _compute_group_duration(self):
        for rec in self:
            rec.group_duration = sum(t.recording_id.duration for t in rec.track_ids)

    next_volume_number = fields.Char(
        compute='_compute_next_track_values'
    )

    next_track_number = fields.Char(
        compute='_compute_next_track_values'
    )

    @api.depends('track_ids.track', 'track_ids.volume')
    def _compute_next_track_values(self):
        recordings_with_tracks = self.filtered(lambda r: r.track_ids)
        recordings_without_tracks = self - recordings_with_tracks

        for rec in recordings_with_tracks:
            last_track = rec.track_ids[-1]

            rec.next_volume_number = last_track.volume

            last_track_number = (rec.track_ids[-1].track or '').strip()
            if last_track_number.isdigit():
                rec.next_track_number = str(int(last_track_number) + 1)

        for rec in recordings_without_tracks:
            rec.next_volume_number = '1'
            rec.next_track_number = '1'
