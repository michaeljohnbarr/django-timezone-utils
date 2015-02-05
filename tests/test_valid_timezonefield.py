# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from datetime import tzinfo
import pytz

# Django
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.test import TestCase

from .models.timezonefield.valid import (LocationTimeZone,
                                         LocationTimeZoneChoices,
                                         TZWithGoodStringDefault,
                                         TZWithGoodTZInfoDefault)


# ==============================================================================
# TESTS: Valid TimeZoneField
# ==============================================================================
class TimeZoneFieldTestCase(TestCase):
    def setUp(self):
        LocationTimeZone.objects.create(timezone='US/Eastern')
        LocationTimeZone.objects.create()

    def test_location_is_tzinfo_instance(self):
        """Location should return a datetime.tzinfo instance, not a string."""
        location = LocationTimeZone.objects.get(timezone='US/Eastern')
        self.assertIsInstance(
            location.timezone,
            tzinfo,
            'Was not a tzinfo object. Got {0} instead.'.format(
                type(location.timezone)
            )
        )

    def test_location_object_set_tzinfo_instance(self):
        location = LocationTimeZone.objects.get(timezone='US/Eastern')
        location.timezone = pytz.timezone('Australia/ACT')
        location.save()
        location = LocationTimeZone.objects.get(timezone='Australia/ACT')
        self.assertIsNotNone(
            obj=location,
            msg='Settings location as a valid tzinfo instance failed.'
        )

    def test_location_object_set_invalid_object_string(self):
        location = LocationTimeZone.objects.get(timezone='US/Eastern')
        with self.assertRaises(ValidationError):
            location.timezone = 'Bad/Timezone'

    def test_location_is_equals_correct_timezone(self):
        """Location should return a datetime.tzinfo instance, not a string."""
        location = LocationTimeZone.objects.get(timezone='US/Eastern')
        self.assertEquals(
            location.timezone,
            pytz.timezone('US/Eastern'),
        )

    def test_location_is_none(self):
        """Location should return None without failing due to the to_python."""
        location = LocationTimeZone.objects.get(timezone=None)
        self.assertEquals(
            location.timezone,
            None,
            'Should have been None. Got {0} instead.'.format(
                type(location.timezone)
            )
        )

    def test_good_location_default_string(self):
        self.assertIsNotNone(
            obj=TZWithGoodStringDefault.objects.create(),
            msg='Location save failed with a good default string.'
        )

    def test_good_location_default_tzinfo_object(self):
        self.assertIsNotNone(
            obj=TZWithGoodTZInfoDefault.objects.create(),
            msg='Location save failed with a good default tzinfo object.'
        )

    def test_bad_timezone_form(self):
        class TimeZoneForm(ModelForm):
            class Meta:
                model = LocationTimeZone
                fields = ('timezone', )

        form = TimeZoneForm(data={'timezone': 'Bad/Value'})
        self.assertFalse(
            form.is_valid(),
            msg='Form with bad timezone should not be valid.'
        )

    def test_null_timezone_form(self):
        class TimeZoneForm(ModelForm):
            class Meta:
                model = LocationTimeZone
                fields = ('timezone', )

        form = TimeZoneForm(data={})
        self.assertTrue(
            form.is_valid(),
            msg='Form should allow itself to be null.'
        )

    def test_form_with_invalid_choice(self):
        class TimeZoneForm(ModelForm):
            class Meta:
                model = LocationTimeZoneChoices
                fields = ('timezone', )

        form = TimeZoneForm(data={'timezone': 'Bad/Value'})
        form.is_valid()

        self.assertFalse(
            form.is_valid(),
            msg='The choice should not be valid.'
        )
