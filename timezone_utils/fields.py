# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from __future__ import unicode_literals
from datetime import datetime, tzinfo, time as datetime_time
import pytz
import warnings

# Django
import django
try:
    from django.core import checks
except ImportError:     # pragma: no cover
    pass
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import DateTimeField, CharField
from django.utils.six import with_metaclass
from django.utils.timezone import get_default_timezone, is_naive, make_aware
from django.utils.translation import ugettext_lazy as _

# App
from timezone_utils import forms


TimeZoneFieldBase = type if django.VERSION >= (1, 8) else models.SubfieldBase

__all__ = ('TimeZoneField', 'LinkedTZDateTimeField')


# ==============================================================================
# MODEL FIELDS
# ==============================================================================
class TimeZoneField(    # pylint: disable=E0239
    with_metaclass(TimeZoneFieldBase, CharField)
):
    # Enforce the minimum length of max_length to be the length of the longest
    #   pytz timezone string
    MIN_LENGTH = max(map(len, pytz.all_timezones))
    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid time zone."),
    }

    # pylint: disable=newstyle
    def __init__(self, *args, **kwargs):
        # Retrieve the model field's declared max_length or default to pytz's
        #   maximum length
        declared_max_length = kwargs.get('max_length', self.MIN_LENGTH)

        # Set the max length to the highest value between the timezone maximum
        #   length and the declared max_length
        kwargs['max_length'] = max(declared_max_length, self.MIN_LENGTH)

        # Warn that we changed the value of max_length so that they can
        if declared_max_length and declared_max_length != kwargs['max_length']:
            warnings.warn(
                message='TimeZoneField max_length updated from {declared} to '
                '{current}.'.format(
                    declared=declared_max_length,
                    current=kwargs['max_length']
                ),
                category=UserWarning,
            )

        super(TimeZoneField, self).__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        """
        Validates value and throws ValidationError. Subclasses should override
        this to provide validation logic.
        """
        # pylint: disable=newstyle
        super(TimeZoneField, self).validate(
            value=self.get_prep_value(value),
            model_instance=model_instance
        )

        # Insure the value is can be converted to a timezone
        self.to_python(value)

    def run_validators(self, value):
        # pylint: disable=newstyle
        super(TimeZoneField, self).run_validators(self.get_prep_value(value))

    def get_prep_value(self, value):
        """Converts timezone instances to strings for db storage."""
        # pylint: disable=newstyle
        value = super(TimeZoneField, self).get_prep_value(value)

        if isinstance(value, tzinfo):
            return value.zone

        return value

    def from_db_value(self, value, expression, connection, context):    # noqa
        """
        Converts a value as returned by the database to a Python object. It is
        the reverse of get_prep_value(). - New in Django 1.8
        """
        if value:
            value = self.to_python(value)

        return value

    def to_python(self, value):
        """Returns a datetime.tzinfo instance for the value."""
        # pylint: disable=newstyle
        value = super(TimeZoneField, self).to_python(value)

        if not value:
            return value

        try:
            return pytz.timezone(str(value))
        except pytz.UnknownTimeZoneError:
            raise ValidationError(
                message=self.error_messages['invalid'],
                code='invalid',
                params={'value': value}
            )

    # pylint: disable=E0239
    def formfield(self, **kwargs):
        """Returns a custom form field for the TimeZoneField."""

        defaults = {'form_class': forms.TimeZoneField}
        defaults.update(**kwargs)
        return super(TimeZoneField, self).formfield(**defaults)

    # --------------------------------------------------------------------------
    # Django >= 1.7 Checks Framework
    # --------------------------------------------------------------------------
    # pylint: disable=E0239
    def check(self, **kwargs):  # pragma: no cover
        """Calls the TimeZoneField's custom checks."""

        errors = super(TimeZoneField, self).check(**kwargs)
        errors.extend(self._check_timezone_max_length_attribute())
        errors.extend(self._check_choices_attribute())
        return errors

    def _check_timezone_max_length_attribute(self):     # pragma: no cover
        """
        Checks that the `max_length` attribute covers all possible pytz timezone
        lengths.
        """

        # Retrieve the maximum possible length for the time zone string
        possible_max_length = max(map(len, pytz.all_timezones))

        # Make sure that the max_length attribute will handle the longest time
        #   zone string
        if self.max_length < possible_max_length:   # pragma: no cover
            return [
                checks.Error(
                    msg=(
                        "'max_length' is too short to support all possible pytz"
                        " time zones."
                    ),
                    hint=(
                        "pytz {version}'s longest time zone string has a length"
                        " of {value}, although it is recommended that you leave"
                        " room for longer time zone strings to be added in the "
                        "future.".format(
                            version=pytz.VERSION,
                            value=possible_max_length
                        )
                    ),
                    obj=self,
                )
            ]

        # When no error, return an empty list
        return []

    def _check_choices_attribute(self):   # pragma: no cover
        """Checks to make sure that choices contains valid timezone choices."""

        if self.choices:
            warning_params = {
                'msg': (
                    "'choices' contains an invalid time zone value '{value}' "
                    "which was not found as a supported time zone by pytz "
                    "{version}."
                ),
                'hint': "Values must be found in pytz.all_timezones.",
                'obj': self,
            }

            for option_key, option_value in self.choices:
                if isinstance(option_value, (list, tuple)):
                    # This is an optgroup, so look inside the group for
                    # options.
                    for optgroup_key in map(lambda x: x[0], option_value):
                        if optgroup_key not in pytz.all_timezones:
                            # Make sure we don't raise this error on empty
                            #   values
                            if optgroup_key not in self.empty_values:
                                # Update the error message by adding the value
                                warning_params.update({
                                    'msg': warning_params['msg'].format(
                                        value=optgroup_key,
                                        version=pytz.VERSION
                                    )
                                })

                            # Return the warning
                            return [
                                checks.Warning(**warning_params)
                            ]
                elif option_key not in pytz.all_timezones:
                    # Make sure we don't raise this error on empty
                    #   values
                    if option_key not in self.empty_values:
                        # Update the error message by adding the value
                        warning_params.update({
                            'msg': warning_params['msg'].format(
                                value=option_key,
                                version=pytz.VERSION
                            )
                        })

                    # Return the warning
                    return [
                        checks.Warning(**warning_params)
                    ]

        # When no error, return an empty list
        return []


class LinkedTZDateTimeField(
    with_metaclass(TimeZoneFieldBase, DateTimeField)
):  # pylint: disable=E0239
    # pylint: disable=newstyle
    def __init__(self, *args, **kwargs):
        self.populate_from = kwargs.pop('populate_from', None)
        self.time_override = kwargs.pop('time_override', None)
        self.timezone = get_default_timezone()

        super(LinkedTZDateTimeField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        # pylint: disable=W0613
        if value:
            value = self.to_python(value)


        return value

    def to_python(self, value):
        """Convert the value to the appropriate timezone."""
        # pylint: disable=newstyle
        value = super(LinkedTZDateTimeField, self).to_python(value)

        if not value:
            return value

        if is_naive(value):
            return make_aware(value=value, timezone=self.timezone)

        return value.astimezone(self.timezone)

    def pre_save(self, model_instance, add):
        """
        Converts the value being saved based on `populate_from` and
        `time_override`
        """
        # pylint: disable=newstyle
        # Retrieve the currently entered datetime
        value = super(
            LinkedTZDateTimeField,
            self
        ).pre_save(
            model_instance=model_instance,
            add=add
        )

        # Convert the value to the correct time/timezone
        value = self._convert_value(
            value=value,
            model_instance=model_instance,
            add=add
        )

        setattr(model_instance, self.attname, value)

        return value

    def deconstruct(self):  # pragma: no cover
        """Add our custom keyword arguments for migrations."""
        # pylint: disable=newstyle
        name, path, args, kwargs = super(
            LinkedTZDateTimeField,
            self
        ).deconstruct()

        # Only include kwarg if it's not the default
        if self.populate_from is not None:
            # Since populate_from requires a model instance and Django does not,
            #   allow lambda, we hope that we have been provided a function that
            #   can be parsed
            kwargs['populate_from'] = self.populate_from

        # Only include kwarg if it's not the default
        if self.time_override is not None:
            if hasattr(self.time_override, '__call__'):
                # Call the callable datetime.time instance
                kwargs['time_override'] = self.time_override()
            else:
                kwargs['time_override'] = self.time_override

        return name, path, args, kwargs

    def _get_populate_from(self, model_instance):
        """Retrieves the timezone or None from the `populate_from` attribute."""

        if hasattr(self.populate_from, '__call__'):
            tz = self.populate_from(model_instance)
        else:
            from_attr = getattr(model_instance, self.populate_from)
            tz = callable(from_attr) and from_attr() or from_attr

        try:
            tz = pytz.timezone(str(tz))
        except pytz.UnknownTimeZoneError:
            # It was a valiant effort. Resistance is futile.
            raise

        # If we have a timezone, set the instance's timezone attribute
        self.timezone = tz

        return tz

    def _get_time_override(self):
        """
        Retrieves the datetime.time or None from the `time_override` attribute.
        """

        if callable(self.time_override):
            time_override = self.time_override()
        else:
            time_override = self.time_override

        if not isinstance(time_override, datetime_time):
            raise ValueError(
                'Invalid type. Must be a datetime.time instance.'
            )

        return time_override

    def _convert_value(self, value, model_instance, add):
        """
        Converts the value to the appropriate timezone and time as declared by
        the `time_override` and `populate_from` attributes.
        """

        if not value:
            return value

        # Retrieve the default timezone as the default
        tz = get_default_timezone()

        # If populate_from exists, override the default timezone
        if self.populate_from is not None:
            tz = self._get_populate_from(model_instance)

        if is_naive(value):
            value = make_aware(value=value, timezone=tz)

        # Convert the value to a datetime object in the correct timezone. This
        # insures that we will have the correct date if we are performing a time
        #   override below.
        value = value.astimezone(tz)

        # Do not convert the time to the time override if auto_now or
        #   auto_now_add is set
        if self.time_override is not None and not (
            self.auto_now or (self.auto_now_add and add)
        ):
            # Retrieve the time override
            time_override = self._get_time_override()

            # Convert the value to the date/time with the appropriate timezone
            value = make_aware(
                value=datetime.combine(
                    date=value.date(),
                    time=time_override
                ),
                timezone=tz
            )

        return value
