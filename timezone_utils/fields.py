# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from __future__ import unicode_literals
from datetime import datetime, tzinfo, time as datetime_time
import pytz

# Django
try:
    from django.core import checks
except ImportError:
    pass
from django.core.exceptions import ValidationError
from django.db.models import SubfieldBase
from django.db.models.fields import DateTimeField, CharField
from django.utils.six import with_metaclass
from django.utils.timezone import get_default_timezone
from django.utils.translation import ugettext_lazy as _

# App
from timezone_utils import forms

__all__ = ('TimeZoneField', 'LinkedTZDateTimeField')


# ==============================================================================
# MODEL FIELDS
# ==============================================================================
class TimeZoneField(with_metaclass(SubfieldBase, CharField)):
    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid time zone."),
    }

    def __init__(self, *args, **kwargs):
        # Retrieve the maximum length of the timezone values from pytz
        timezone_max_length = max(map(len, pytz.all_timezones))

        # Retrieve the model field's declared max_length or default to pytz's
        #   maximum length
        declared_max_length = kwargs.get('max_length', timezone_max_length)

        # Set the max length to the highest value between the timezone maximum
        #   length and the declared max_length
        kwargs['max_length'] = max(declared_max_length, timezone_max_length)

        super(TimeZoneField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if isinstance(value, tzinfo):
            return value.zone
        return value

    def to_python(self, value):
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

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.TimeZoneField}
        defaults.update(**kwargs)
        return super(TimeZoneField, self).formfield(**defaults)

    # --------------------------------------------------------------------------
    # Django >= 1.7 Checks Framework
    # --------------------------------------------------------------------------
    def check(self, **kwargs):  # pragma: no cover
        errors = super(TimeZoneField, self).check(**kwargs)
        errors.extend(self._check_timezone_max_length_attribute())
        errors.extend(self._check_choices_attribute())
        return errors

    def _check_timezone_max_length_attribute(self):     # pragma: no cover
        """Custom check() method that verifies that the `max_length` attribute
        covers all possible pytz timezone lengths.

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
        if self.choices:
            warning_params = {
                'msg': (
                    "'choices' contains an invalid time zone value '{value}' "
                    "which was not found as a supported time zone by pytz "
                    "{version}."
                ),
                'hint': "Values must be found in pytz.common_timezones.",
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


class LinkedTZDateTimeField(with_metaclass(SubfieldBase, DateTimeField)):
    def __init__(self, *args, **kwargs):
        self.populate_from = kwargs.pop('populate_from', None)
        self.time_override = kwargs.pop('time_override', None)

        super(LinkedTZDateTimeField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        # Retrieve the currently entered datetime
        value = super(
            LinkedTZDateTimeField,
            self
        ).pre_save(
            model_instance=model_instance,
            add=add
        )

        if not value:
            return value

        # Retrieve the default timezone
        tz = get_default_timezone()

        if self.populate_from:
            if hasattr(self.populate_from, '__call__'):
                # LinkedTZDateTimeField(
                #     populate_from=lambda instance: instance.field.timezone
                # )
                tz = self.populate_from(model_instance)
            else:
                # LinkedTZDateTimeField(populate_from='field')
                from_attr = getattr(model_instance, self.populate_from)
                tz = callable(from_attr) and from_attr() or from_attr

            try:
                tz = pytz.timezone(str(tz))
            except pytz.UnknownTimeZoneError:
                # It was a valiant effort. Resistance is futile.
                raise

            # We don't want to double-convert the value. This leads to incorrect
            #   dates being generated when the overridden time goes back a day.
            if self.time_override is None:
                datetime_as_timezone = value.astimezone(tz)
                value = tz.normalize(
                    tz.localize(
                        datetime.combine(
                            date=datetime_as_timezone.date(),
                            time=datetime_as_timezone.time()
                        )
                    )
                )

        if self.time_override is not None and not (
            self.auto_now or (self.auto_now_add and add)
        ):
            if callable(self.time_override):
                time_override = self.time_override()
            else:
                time_override = self.time_override

            if not isinstance(time_override, datetime_time):
                raise ValueError(
                    'Invalid type. Must be a datetime.time instance.'
                )

            value = tz.normalize(
                tz.localize(
                    datetime.combine(
                        date=value.date(),
                        time=time_override,
                    )
                )
            )

        setattr(model_instance, self.attname, value)
        setattr(model_instance, '_timezone', tz)

        return value

    def deconstruct(self):  # pragma: no cover
        name, path, args, kwargs = super(
            LinkedTZDateTimeField,
            self
        ).deconstruct()

        # Only include kwarg if it's not the default
        if self.populate_from is not None:
            kwargs['populate_from'] = self.populate_from

        if self.time_override is not None:
            kwargs['time_override'] = self.time_override

        return name, path, args, kwargs
