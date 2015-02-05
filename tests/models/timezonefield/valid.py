# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
import pytz

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# App
from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES
from timezone_utils.fields import TimeZoneField


# ==============================================================================
# MODELS
# ==============================================================================
class LocationTimeZone(models.Model):
    timezone = TimeZoneField(
        verbose_name=_('timezone'),
        max_length=64,
        null=True,
        blank=True
    )


class LocationTimeZoneChoices(models.Model):
    timezone = TimeZoneField(
        verbose_name=_('timezone'),
        max_length=64,
        null=True,
        blank=True,
        choices=PRETTY_ALL_TIMEZONES_CHOICES,
    )


class TZWithGoodStringDefault(models.Model):
    """Test should validate that"""
    timezone = TimeZoneField(
        default='US/Eastern',
        max_length=64,
        null=True,
    )


class TZWithGoodTZInfoDefault(models.Model):
    timezone = TimeZoneField(
        default=pytz.timezone('US/Pacific'),
        max_length=64,
        null=True,
    )
