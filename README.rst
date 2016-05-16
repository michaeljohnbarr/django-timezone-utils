Django Timezone Utils: Time Zone Utilities For Models
=====================================================

.. image:: https://img.shields.io/pypi/v/django-timezone-utils.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/django-timezone-utils/
    :alt: Latest Version

.. image:: https://travis-ci.org/michaeljohnbarr/django-timezone-utils.png?branch=master
    :target: https://travis-ci.org/michaeljohnbarr/django-timezone-utils
    :alt: Test Status

.. image:: https://coveralls.io/repos/michaeljohnbarr/django-timezone-utils/badge.svg
    :target: https://coveralls.io/r/michaeljohnbarr/django-timezone-utils
    :alt: Coverage Status

.. image:: https://landscape.io/github/michaeljohnbarr/django-timezone-utils/master/landscape.png
    :target: https://landscape.io/github/michaeljohnbarr/django-timezone-utils
    :alt: Code Health

.. image:: https://img.shields.io/pypi/pyversions/django-timezone-utils.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/django-timezone-utils/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/django-timezone-utils.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/django-timezone-utils/
    :alt: License

.. image:: https://img.shields.io/pypi/status/django-timezone-utils.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/django-timezone-utils/
    :alt: Development Status


**django-timezone-utils** adds automatic time zone conversions and support
utilities to Django.

Please note that this project is currently marked as a development status of
*Beta*. Suggestions, constructive criticism, and feedback are certainly
welcomed and appreciated.

Documentation
-------------

Documentation for django-timezone-utils is available at `Read the Docs <https://django-timezone-utils.readthedocs.org/>`_.

Inspiration
-----------

On multiple occasions, I have had the need to store time zone information to the
one model, then base another model's datetime on that time zone. If you have
ever had to deal with this, you will know how complicated this can be.

I created these fields to ease the process of manipulating times based on
another field's or models timezone choice. Instead of having to remember to use
``Model.clean_fields``, we can now create the models with the validation built
into the model field.


Quick Example
-------------

.. code-block:: python

    from datetime import datetime
    from timezone_utils.fields import LinkedTZDateTimeField, TimeZoneField
    from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES

    class Location(models.Model):
        # ...
        timezone = TimeZoneField(choices=PRETTY_ALL_TIMEZONES_CHOICES)


    def get_location_timezone(obj):
        """Returns the Location.timezone field from above"""

        return obj.location.timezone


    class LocationReport(models.Model):
        # ...
        location = models.ForeignKey('app_label.Location', related_name='reports')

        # Populates from the Location.timezone
        timestamp = LinkedTZDateTimeField(populate_from=get_location_timezone)


    class LocationPeriod(models.Model):
        # ...
        location = models.ForeignKey('app_label.Location', related_name='periods')

        # Sets the time to 12:00am in the location.timezone
        start = LinkedTZDateTimeField(
            populate_from=get_location_timezone,
            time_override=datetime.min.time()
        )

        # Sets the time to 11:59:59.99999pm in the location.timezone
        end = LinkedTZDateTimeField(
            populate_from=get_location_timezone,
            time_override=datetime.max.time()
        )


Contributors
------------

* `Michael Barr <http://github.com/michaeljohnbarr>`_
* `Kosei Kitahara <https://github.com/Surgo>`_

Changelog
---------
- 0.10 Added testing support for Python 3.5 and Django 1.9.
- 0.9 Corrected a bug to where ``time_override`` caused invalid date due to not converting to the correct timezone first. Refactored conversion code. Added testing support for Django 1.8. Removed Django from setup requirements - the onus of having a supported version of Django is on the developer.
- 0.8 Corrected a bug to where ``time_override`` caused invalid date due to not converting to the correct timezone first. Added choices ``GROUPED_ALL_TIMEZONES_CHOICES`` and ``GROUPED_COMMON_TIMEZONES_CHOICES`` to the documentation.
- 0.7 Corrected a bug where datetime.max.time() resulted in incorrect date/time. Changed tests to compare time_override models via string to prevent future regressions. Added choices ``GROUPED_ALL_TIMEZONES_CHOICES`` and ``GROUPED_COMMON_TIMEZONES_CHOICES``.
- 0.6 Added RTD documentation. LinkedTZDateTimeField now returns the datetime object in the overidden timezone and time.
- 0.5 Bug fix: time override on datetime.min.time() failed to set time properly
- 0.4 Removed support for Python 2.5
- 0.3 Code cleanup.
- 0.2 Multiple bug fixes based on testing.
- 0.1 Initial release.
