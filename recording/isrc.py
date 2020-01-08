# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _
from odoo.exceptions import ValidationError


def check_isrc_code(code: str, context: dict):
    _check_code_is_alphanumeric(code, context)
    _check_code_has_12_chars(code, context)


def _check_code_is_alphanumeric(code, context):
    if not code.isalnum():
        raise ValidationError(_(
            'The given ISRC ({}) is invalid. '
            'It must contain only letters and digits. '
            'No special caracters are authorized.'
        ).format(code))


def _check_code_has_12_chars(code, context):
    if len(code) != 12:
        raise ValidationError(_(
            'The given ISRC ({}) is invalid. '
            'It must have exactly 12 caracters.'
        ).format(code))
