# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from collections import defaultdict, namedtuple
from datetime import datetime
from operator import attrgetter
import pytz
import re

__all__ = ('get_choices', 'ALL_TIMEZONES_CHOICES', 'COMMON_TIMEZONES_CHOICES',
           'GROUPED_ALL_TIMEZONES_CHOICES', 'GROUPED_COMMON_TIMEZONES_CHOICES',
           'PRETTY_ALL_TIMEZONES_CHOICES', 'PRETTY_COMMON_TIMEZONES_CHOICES')


# ==============================================================================
# DYNAMIC CHOICES FUNCTIONS
# ==============================================================================
# Compile a regex to parse a string timezone offset ('-0500')
TIMEZONE_OFFSET_REGEX = re.compile(
    r'^(?P<plus_minus>(\+|-))(?P<hours>\d{2})(?P<minutes>\d{2})$'
)


def get_choices(timezones, grouped=False):
    """Retrieves timezone choices from any iterable (normally pytz)."""

    # Created a namedtuple to store the "key" for the choices_dict
    TZOffset = namedtuple('TZOffset', 'value offset_string')

    choices_dict = defaultdict(list)

    # Iterate through the timezones and populate the timezone choices
    for tz in iter(timezones):
        # Retrieve a datetime object in this time zone
        now = datetime.now(pytz.timezone(tz))

        # Retrieve the timezone offset ("-0500" / "+0500")
        offset = now.strftime("%z")

        # Retrieve the offset string ("GMT-12:00" / "GMT+12:00")
        timezone_offset_string = 'GMT{plus_minus}{hours}:{minutes}'.format(
            **TIMEZONE_OFFSET_REGEX.match(offset).groupdict()
        )

        if not grouped:
            # Format the timezone display string
            display_string = '({timezone_offset_string}) {tz}'.format(
                timezone_offset_string=timezone_offset_string,
                tz=tz,
            )
        else:
            display_string = tz

        choices_dict[
            TZOffset(value=int(offset), offset_string=timezone_offset_string)
        ].append(
            (tz, display_string)
        )

    choices = []

    for tz_offset in sorted(choices_dict, key=attrgetter('value')):
        if not grouped:
            choices.extend(
                tuple(choices_dict[tz_offset])
            )
        else:
            choices.append(
                (
                    tz_offset.offset_string,
                    tuple(choices_dict[tz_offset])
                )
            )

    # Cast the timezone choices to a tuple and return
    return tuple(choices)


# ==============================================================================
# CHOICES CONSTANTS
# ==============================================================================
# Standard (unaltered) pytz timezone choices
ALL_TIMEZONES_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
COMMON_TIMEZONES_CHOICES = tuple(
    zip(pytz.common_timezones, pytz.common_timezones)
)

# Grouped by timezone offset, with "GMT-05:00" as the group name
GROUPED_ALL_TIMEZONES_CHOICES = get_choices(
    timezones=pytz.all_timezones,
    grouped=True
)
GROUPED_COMMON_TIMEZONES_CHOICES = get_choices(
    timezones=pytz.common_timezones,
    grouped=True
)

# Sorted by timezone offset, with "(GMT-05:00) US/Eastern" as the display name
PRETTY_ALL_TIMEZONES_CHOICES = get_choices(timezones=pytz.all_timezones)
PRETTY_COMMON_TIMEZONES_CHOICES = get_choices(timezones=pytz.common_timezones)
