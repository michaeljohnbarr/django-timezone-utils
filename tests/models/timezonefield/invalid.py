# ==============================================================================
# IMPORTS
# ==============================================================================
# Django
from django.db import models

# App
from timezone_utils.fields import TimeZoneField


# ==============================================================================
# MODELS
# ==============================================================================
class TZWithLowMaxLength(models.Model):
    """Test should check to make sure that the `max_length` is set to the
    maximum length of the longest value provided by pytz.all_timezones.

    """
    timezone = TimeZoneField(
        max_length=15,
        null=True,
    )


class TZWithBadStringDefault(models.Model):
    """Test should check that a ValidationError is raised when..."""
    timezone = TimeZoneField(
        default='Bad/Worse',
        max_length=64,
        null=True,
    )
