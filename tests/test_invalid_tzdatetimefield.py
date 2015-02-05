# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
import pytz

# Django
from django.core.exceptions import ValidationError
from django.test import TestCase

# App
from tests.models import (ModelWithBadPopulateFrom,
                                                  ModelWithBadTimeOverride,
                                                  ModelWithBadTimeZoneCharField)


# ==============================================================================
# TESTS: Invalid LinkedTZDateTimeField
# ==============================================================================
class InvalidDateTimeWithTimeZoneFieldTestCase(TestCase):
    def test_invalid_field_reference_string(self):
        with self.assertRaises(AttributeError):
            ModelWithBadPopulateFrom.objects.create(),

    def test_bad_time_override_value(self):
        with self.assertRaises(ValidationError):
            ModelWithBadTimeOverride.objects.create()

    def test_bad_populate_from_timezone_as_charfield(self):
        with self.assertRaises(pytz.UnknownTimeZoneError):
            ModelWithBadTimeZoneCharField.objects.create()
