# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from __future__ import unicode_literals

# Django
from django.conf import settings
from django.db import models

# App
from timezone_utils.fields import LinkedTZDateTimeField, TimeZoneField


# ==============================================================================
# MODELS
# ==============================================================================
class ModelWithBadTimeOverride(models.Model):
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        time_override='<invalid>',
    )


class ModelWithBadPopulateFrom(models.Model):
    timezone = TimeZoneField(default='US/Eastern')
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from='invalid_field_reference',
    )


class ModelWithBadTimeZoneCharField(models.Model):
    timezone = models.CharField(default='Bad/Worse', max_length=64)
    timestamp = LinkedTZDateTimeField(
        default=settings.TEST_DATETIME,
        populate_from='timezone',
    )
