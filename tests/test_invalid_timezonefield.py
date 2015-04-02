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
        with self.assertRaises(ValidationError):
            TZWithBadStringDefault.objects.create()

    def test_run_validators(self):
        with self.assertRaises(ValidationError):
            TZWithLowMaxLength._meta.get_field('timezone').run_validators('Bad')

    def test_validate(self):
        instance = TZWithLowMaxLength.objects.create(timezone='US/Eastern')
        with self.assertRaises(ValidationError):
            TZWithLowMaxLength._meta.get_field('timezone').validate(
                value='Bad',
                model_instance=instance
            )

    def test_validate_no_error(self):
        instance = TZWithLowMaxLength.objects.create(timezone='US/Eastern')
        self.assertIsNone(
            obj=TZWithLowMaxLength._meta.get_field('timezone').validate(
                value='US/Eastern',
                model_instance=instance
            )
        )
