# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
import pytz

# Django
from django.core.exceptions import ValidationError
from django.test import TestCase

# App
from tests.models import (TZWithBadStringDefault, TZWithLowMaxLength)


# ==============================================================================
# TESTS
# ==============================================================================
class InvalidTimeZoneFieldTestCase(TestCase):
    def test_location_max_length(self):
        """If a value is too low, we adjust it for convenience."""
        self.assertEquals(
            TZWithLowMaxLength._meta.get_field('timezone').max_length,
            max(map(len, pytz.all_timezones)),
        )

    def test_bad_location_default_string(self):
        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message="'Bad/Worse' is not a valid time zone."
        ):
            TZWithBadStringDefault.objects.create()
