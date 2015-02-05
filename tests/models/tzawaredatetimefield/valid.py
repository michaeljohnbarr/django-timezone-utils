# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from __future__ import unicode_literals
from datetime import datetime, time as datetime_time

# Django
from django.conf import settings
from django.db import models

# App
from timezone_utils.fields import LinkedTZDateTimeField, TimeZoneField


# ==============================================================================
# MODELS
# ==============================================================================
class ModelWithDateTimeOnly(models.Model):
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
    )


class NullModelWithDateTimeOnly(models.Model):
    timestamp = LinkedTZDateTimeField(
        null=True,
    )


class CallableTimeStampedModel(models.Model):
    start = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        time_override=datetime.min.time
    )
    end = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        time_override=datetime.max.time
    )


class StaticTimeStampedModel(models.Model):
    start = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        time_override=datetime_time(0, 0)
    )
    end = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        time_override=datetime_time(23, 59, 59, 999999)
    )


class ModelWithForeignKeyToTimeZone(models.Model):
    other_model = models.ForeignKey(
        to='tests.TZWithGoodStringDefault'
    )
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from=lambda instance: instance.other_model.timezone
    )


class ModelWithLocalTimeZone(models.Model):
    timezone = TimeZoneField(default='US/Eastern')
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from='timezone'
    )


class ModelWithLocalTZCharField(models.Model):
    timezone = models.CharField(default='US/Eastern', max_length=64)
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from='timezone'
    )
