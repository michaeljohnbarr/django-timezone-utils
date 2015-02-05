# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from __future__ import unicode_literals
import pytz

# Django
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.utils.translation import ugettext_lazy as _

__all__ = ('TimeZoneField', )


# ==============================================================================
# FORM FIELDS
# ==============================================================================
class TimeZoneField(CharField):
    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid time zone."),
    }

    def to_python(self, value):
        value = super(TimeZoneField, self).to_python(value)

        if not value:
            return value

        try:
            pytz.timezone(str(value))
        except pytz.UnknownTimeZoneError:
            raise ValidationError(
                message=self.error_messages['invalid'],
                code='invalid',
                params={'value': value}
            )
