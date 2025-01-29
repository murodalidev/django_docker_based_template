import re

from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value):
    uzbek_regex = r'^998\d{9}$'
    validate = re.match(uzbek_regex, value)
    if not validate:
        raise ValidationError(_('Invalid phone number format! Phone number must be uzbek number! 998 XX XXX XX XX'))


def alpha_numeric_validator(value):
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', value):
        raise ValidationError(
            'Value can only contain letters and numbers.'
        )
    if len(value) < 2:
        raise ValidationError('Value must be at least 2 characters long.')
