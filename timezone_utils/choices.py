# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from datetime import datetime
import pytz
import re

__all__ = ('get_choices', 'ALL_TIMEZONES_CHOICES', 'COMMON_TIMEZONES_CHOICES',
           'PRETTY_ALL_TIMEZONES_CHOICES', 'PRETTY_COMMON_TIMEZONES_CHOICES')


# ==============================================================================
# DYNAMIC CHOICES FUNCTIONS
# ==============================================================================
# Compile a regex to parse a string timezone offset ('-0500')
TIMEZONE_OFFSET_REGEX = re.compile(
    r'^(?P<plus_minus>(\+|-))(?P<hours>\d{2})(?P<minutes>\d{2})$'
)


def get_choices(timezones):
    """Retrieves timezone choices from any iterable (normally pytz)."""
    timezone_choices = []

    # Iterate through the timezones and populate the timezone choices
    for tz in iter(timezones):
        # Retrieve a datetime object in this time zone
        now = datetime.now(pytz.timezone(tz))

        # Retrieve the timezone offset ("-0500" / "+0500")
        offset = now.strftime("%z")

        # Format the timezone display string
        display_string = '(GMT{plus_minus}{hours}:{minutes}) {tz}'.format(
            tz=tz,
            **TIMEZONE_OFFSET_REGEX.match(offset).groupdict()
        )

        # Append a tuple of the timezone information:
        #   (-500, 'US/Eastern', '(GMT-05:00) US/Eastern')
        timezone_choices.append((int(offset), tz, display_string))

    # Sort the timezone choices by the integer offsets (negative to positive)
    timezone_choices.sort()

    # Iterate through the timezone choices by index, and update the index to
    #   remove the integer offset, leaving the:
    #       ('US/Eastern', '(GMT-05:00) US/Eastern')
    for i in range(len(timezone_choices)):
        timezone_choices[i] = timezone_choices[i][1:]

    # Cast the timezone choices to a tuple and return
    return tuple(timezone_choices)


# ==============================================================================
# CHOICES CONSTANTS
# ==============================================================================
# Standard (unaltered) pytz timezone choices
ALL_TIMEZONES_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
COMMON_TIMEZONES_CHOICES = tuple(
    zip(pytz.common_timezones, pytz.common_timezones)
)

# Sorted by timezone offset, with "(GMT-05:00) US/Eastern" as the display name
PRETTY_ALL_TIMEZONES_CHOICES = get_choices(pytz.all_timezones)
PRETTY_COMMON_TIMEZONES_CHOICES = get_choices(pytz.common_timezones)
