# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from datetime import datetime
from operator import itemgetter
import pytz
import re

# Django
from django.test import TestCase

# App
from timezone_utils.choices import (ALL_TIMEZONES_CHOICES,
                                    COMMON_TIMEZONES_CHOICES,
                                    GROUPED_ALL_TIMEZONES_CHOICES,
                                    GROUPED_COMMON_TIMEZONES_CHOICES,
                                    PRETTY_ALL_TIMEZONES_CHOICES,
                                    PRETTY_COMMON_TIMEZONES_CHOICES,
                                    TIMEZONE_OFFSET_REGEX, get_choices)


# ==============================================================================
# TESTS
# ==============================================================================
class TimeZoneChoicesTestCase(TestCase):
    def test_TIMEZONE_OFFSET_REGEX(self):
        now = datetime.now(pytz.timezone('US/Eastern'))
        self.assertNotEqual(str(now.strftime('%z')), None)
        self.assertEqual(
            TIMEZONE_OFFSET_REGEX.match('-' + str(now.strftime('%z'))),
            None
        )
        self.assertEqual(
            TIMEZONE_OFFSET_REGEX.match(str(now.strftime('%z') + '1')),
            None
        )

    def test_ALL_TIMEZONES_CHOICES_length(self):
        self.assertEqual(
            len(ALL_TIMEZONES_CHOICES),
            len(pytz.all_timezones),
            'The length of ALL_TIMEZONES_CHOICES does not match '
            'pytz.all_timezones.'
        )

    def test_ALL_TIMEZONES_CHOICES_values(self):
        values = map(itemgetter(0), ALL_TIMEZONES_CHOICES)
        for value in values:
            self.assertIn(
                value,
                pytz.all_timezones,
                'The value "{0}" from ALL_TIMEZONES_CHOICES was not found in '
                'pytz.all_timezones.'.format(
                    value
                )
            )

    def test_COMMON_TIMEZONES_CHOICES_length(self):
        self.assertEqual(
            len(COMMON_TIMEZONES_CHOICES),
            len(pytz.common_timezones),
            'The length of COMMON_TIMEZONES_CHOICES does not match '
            'pytz.common_timezones.'
        )

    def test_COMMON_TIMEZONES_CHOICES_values(self):
        values = map(itemgetter(0), COMMON_TIMEZONES_CHOICES)
        for value in values:
            self.assertIn(
                value,
                pytz.common_timezones,
                'The value "{0}" from COMMON_TIMEZONES_CHOICES was not found '
                'in pytz.common_timezones.'.format(
                    value
                )
            )

    def test_PRETTY_ALL_TIMEZONES_CHOICES_length(self):
        self.assertEqual(
            len(PRETTY_ALL_TIMEZONES_CHOICES),
            len(pytz.all_timezones),
            'The length of PRETTY_ALL_TIMEZONES_CHOICES does not match '
            'pytz.all_timezones.'
        )

    def test_PRETTY_ALL_TIMEZONES_CHOICES_values(self):
        values = map(itemgetter(0), PRETTY_ALL_TIMEZONES_CHOICES)
        for value in values:
            self.assertIn(
                value,
                pytz.all_timezones,
                'The value "{0}" from PRETTY_ALL_TIMEZONES_CHOICES was not '
                'found in pytz.all_timezones.'.format(
                    value
                )
            )

    def test_PRETTY_COMMON_TIMEZONES_CHOICES_length(self):
        self.assertEqual(
            len(PRETTY_COMMON_TIMEZONES_CHOICES),
            len(pytz.common_timezones),
            'The length of PRETTY_COMMON_TIMEZONES_CHOICES does not match '
            'pytz.common_timezones.'
        )

    def test_PRETTY_COMMON_TIMEZONES_CHOICES_values(self):
        values = map(itemgetter(0), PRETTY_COMMON_TIMEZONES_CHOICES)
        for value in values:
            self.assertIn(
                value,
                pytz.common_timezones,
                'The value "{0}" from PRETTY_COMMON_TIMEZONES_CHOICES was not '
                'found in pytz.common_timezones.'.format(
                    value
                )
            )

    def test_GROUPED_ALL_TIMEZONES_CHOICES_group_name(self):
        group_name_re = re.compile(r'GMT(\+|-)\d{2}:\d{2}')
        for group_name in map(lambda x: x[0], GROUPED_ALL_TIMEZONES_CHOICES):
            self.assertNotEqual(
                group_name_re.match(group_name),
                None
            )

    def test_GROUPED_COMMON_TIMEZONES_CHOICES_group_name(self):
        group_name_re = re.compile(r'GMT(\+|-)\d{2}:\d{2}')
        for group_name in map(lambda x: x[0], GROUPED_COMMON_TIMEZONES_CHOICES):
            self.assertNotEqual(
                group_name_re.match(group_name),
                None
            )

    def test_GROUPED_ALL_TIMEZONES_CHOICES_values(self):
        for name, display in map(
            lambda v: v[0],
            map(lambda x: x[1], GROUPED_ALL_TIMEZONES_CHOICES)
        ):
            self.assertIn(
                name,
                pytz.all_timezones
            )
            self.assertIn(
                display,
                pytz.all_timezones
            )

    def test_GROUPED_COMMON_TIMEZONES_CHOICES_values(self):
        for name, display in map(
            lambda v: v[0],
            map(lambda x: x[1], GROUPED_COMMON_TIMEZONES_CHOICES)
        ):
            self.assertIn(
                name,
                pytz.common_timezones
            )
            self.assertIn(
                display,
                pytz.common_timezones
            )

    def test_get_choices_values_ungrouped(self):
        choices = get_choices(pytz.common_timezones)
        values = map(itemgetter(0), choices)
        for value in values:
            self.assertIn(value, pytz.common_timezones)

        choices = get_choices(pytz.all_timezones)
        values = map(itemgetter(0), choices)
        for value in values:
            self.assertIn(value, pytz.all_timezones)
