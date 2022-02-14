# ==============================================================================
# IMPORTS
# ==============================================================================
# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from __future__ import unicode_literals
from datetime import datetime, time as datetime_time
import pytz

# Django
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# App
from timezone_utils.fields import LinkedTZDateTimeField, TimeZoneField
from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES


# ==============================================================================
# MODELS
# ==============================================================================
class TZWithLowMaxLength(models.Model):
    """Test should check to make sure that the `max_length` is set to the
    maximum length of the longest value provided by pytz.all_timezones.

    """
    id = models.AutoField(primary_key=True)
    timezone = TimeZoneField(
        max_length=15,
        null=True,
    )


class TZWithBadStringDefault(models.Model):
    """Test should check that a ValidationError is raised when..."""
    id = models.AutoField(primary_key=True)
    timezone = TimeZoneField(
        default='Bad/Worse',
        max_length=64,
        null=True,
    )


class ModelWithBadTimeOverride(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        time_override='<invalid>',
    )


class ModelWithBadPopulateFrom(models.Model):
    id = models.AutoField(primary_key=True)
    timezone = TimeZoneField(default='US/Eastern')
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from='invalid_field_reference',
    )


class ModelWithBadTimeZoneCharField(models.Model):
    id = models.AutoField(primary_key=True)
    timezone = models.CharField(default='Bad/Worse', max_length=64)
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from='timezone',
    )


class LocationTimeZone(models.Model):
    id = models.AutoField(primary_key=True)
    timezone = TimeZoneField(
        verbose_name=_('timezone'),
        max_length=64,
        null=True,
        blank=True
    )


class LocationTimeZoneChoices(models.Model):
    id = models.AutoField(primary_key=True)
    timezone = TimeZoneField(
        verbose_name=_('timezone'),
        max_length=64,
        null=True,
        blank=True,
        choices=PRETTY_ALL_TIMEZONES_CHOICES,
    )


class LocationTimeZoneChoicesWithEmpty(models.Model):
    id = models.AutoField(primary_key=True)
    timezone = TimeZoneField(
        verbose_name=_('timezone'),
        max_length=64,
        null=True,
        blank=True,
        choices=[('', 'No time zone')] + list(PRETTY_ALL_TIMEZONES_CHOICES),
    )


class LocationTimeZoneBadChoices(models.Model):
    id = models.AutoField(primary_key=True)
    timezone = TimeZoneField(
        verbose_name=_('timezone'),
        max_length=64,
        null=True,
        blank=True,
        choices=[('Bad/Worse', 'Bad Choice')],
    )


class TZWithGoodStringDefault(models.Model):
    id = models.AutoField(primary_key=True)
    """Test should validate that"""
    timezone = TimeZoneField(
        default='US/Eastern',
        max_length=64,
        null=True,
    )


class TZWithGoodTZInfoDefault(models.Model):
    id = models.AutoField(primary_key=True)
    timezone = TimeZoneField(
        default=pytz.timezone('US/Pacific'),
        max_length=64,
        null=True,
    )


class ModelWithDateTimeOnly(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
    )


class NullModelWithDateTimeOnly(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = LinkedTZDateTimeField(
        null=True,
    )


class CallableTimeStampedModel(models.Model):
    id = models.AutoField(primary_key=True)
    start = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        time_override=datetime.min.time
    )
    end = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        time_override=datetime.max.time()
    )


class StaticTimeStampedModel(models.Model):
    id = models.AutoField(primary_key=True)
    start = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        time_override=datetime_time(0, 0)
    )
    end = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        time_override=datetime_time(23, 59, 59, 999999)
    )


def get_other_model_timezone(obj):
    return obj.other_model.timezone


class ModelWithForeignKeyToTimeZone(models.Model):
    id = models.AutoField(primary_key=True)
    other_model = models.ForeignKey(
        to='tests.TZWithGoodStringDefault',
        related_name='fk_to_tz',
        on_delete=models.CASCADE,
    )
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from=get_other_model_timezone,
    )


class ModelWithLocalTimeZone(models.Model):
    id = models.AutoField(primary_key=True)
    timezone = TimeZoneField(default='US/Eastern')
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from='timezone'
    )


class ModelWithLocalTZCharField(models.Model):
    id = models.AutoField(primary_key=True)
    timezone = models.CharField(default='US/Eastern', max_length=64)
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from='timezone'
    )


class TZTimeFramedModel(models.Model):
    id = models.AutoField(primary_key=True)
    other_model = models.ForeignKey(
        to='tests.TZWithGoodStringDefault',
        related_name='fk_to_tz_too',
        on_delete=models.CASCADE,
    )
    start = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from=get_other_model_timezone,
        time_override=datetime.min.time()
    )
    end = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from=get_other_model_timezone,
        time_override=datetime.max.time()
    )
