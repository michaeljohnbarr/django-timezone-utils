Django Timezone Utils: Time Zone Utilities For Models
=====================================================

.. image:: https://pypip.in/version/django-timezone-utils/badge.svg?style=flat&text=version
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
    
.. image:: https://pypip.in/py_versions/django-timezone-utils/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/django-timezone-utils/
    :alt: Supported Python versions
    
.. image:: https://pypip.in/license/django-timezone-utils/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/django-timezone-utils/
    :alt: License
    
.. image:: https://pypip.in/status/django-timezone-utils/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/django-timezone-utils/
    :alt: Development Status
    


**django-timezone-utils** adds automatic time zone conversions and support
utilities to Django.

Please note that this project is currently marked as a development status of
*Alpha*. Suggestions, constructive criticism, and feedback are certainly
welcomed and appreciated.

Installation
------------

*django-timezone-utils* works with Django 1.4, 1.5, 1.6 and 1.7.

To install it, simply:

.. code-block:: bash

    $ pip install django-timezone-utils


Then add ``timezone_utils`` to your ``settings.INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'timezone_utils',
    )

Example Usage
-------------

Imagine you have the models ``Location`` and ``LocationReportingPeriod``:

.. code-block:: python

    from datetime import datetime
    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    from timezone_utils.fields import LinkedTZDateTimeField, TimeZoneField
    from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES

    class Location(models.Model):
        company = models.ForeignKey(
            verbose_name='company',
            to='app_label.Company',
            related_name='locations',
        )
        name = models.CharField(
            verbose_name=_('name'),
            max_length=128,
        )
        timezone = TimeZoneField(
            verbose_name=_('timezone'),
            max_length=64,
            choices=PRETTY_ALL_TIMEZONES_CHOICES,
        )

        created = LinkedTZDateTimeField(
            verbose_name=_('created'),
            auto_now=True,
        )
        modified = LinkedTZDateTimeField(
            verbose_name=_('modified'),
            auto_now_add=True,
        )


    class LocationReportingPeriod(models.Model)
        location = models.ForeignKey(
            verbose_name=_('location'),
            to='app_label.Location',
            related_name='reporting_periods',
        )
        start = LinkedTZDateTimeField(
            verbose_name=_('start'),
            # populate_from can also be a string value, provided that the string value
            #   is a field on the same model
            populate_from=lambda instance: instance.location.timezone,
            # Time override must be a datetime.time instance
            time_override=datetime.min.time,
        )
        end = LinkedTZDateTimeField(
            verbose_name=_('end'),
            populate_from=lambda instance: instance.location.timezone,
            # Time override must be a datetime.time instance
            time_override=datetime.max.time,
        )

        created = LinkedTZDateTimeField(
            verbose_name=_('created'),
            auto_now=True,
        )
        modified = LinkedTZDateTimeField(
            verbose_name=_('modified'),
            auto_now_add=True,
        )

        class Meta:
            ordering = ('location', '-start')

In the above code example, if we set the value of ``Location.timezone`` to
``US/Eastern``, each time a ``LocationReportingPeriod`` is saved, it will save
the ``LocationReportingPeriod.start`` as the date 12:00AM in US/Eastern
time zone, and the ``LocationReportingPeriod.end`` as 11:59:59.9999999PM in the
US/Eastern time zone.

So assuming the date was 2015-01-01, we would be saving the following values to
the database:

.. code-block:: python

    # LocationReportingPeriod.start
    datetime.datetime(2015, 1, 1, 0, 0, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)
    
    # LocationReportingPeriod.end
    datetime.datetime(2015, 1, 1, 23, 59, 59, 999999, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)

For each location, let's say that the client wants to see the start and end of
the reporting period in that location's time zone. One thing to remember is that
just because you saved the LocationReportingPeriod start/end dates as a
particular time zone, it does not mean that they will come that way from the
database. For example, if your application's settings.TIME_ZONE is set to
``UTC``, you would get back:

.. code-block:: python
    
    print(period.start)
    datetime.datetime(2015, 1, 1, 5, 0, tzinfo=<UTC>)
    
    print(period.end)
    datetime.datetime(2015, 1, 2, 4, 59, 59, 999999, tzinfo=<UTC>)

Here is how we would handle the displaying conversions from view to template:

.. code-block:: python

    # views.py:
    # Django
    from django.views.generic import ListView

    # App
    from app_label.models import LocationReportingPeriod

    class LocationReportingPeriodListView(ListView):
        model = LocationReportingPeriod
        template_name = 'app_label/period_list.html'

        def get_queryset(self):
            """Retrieve the queryset and perform select_related on `location` since
            we will be using it in the template.

            """
            return super(
                LocationReportingPeriodListView,
                self
            ).get_queryset().select_related(
                'location'
            )

.. code-block:: django

    {% load tz %}
    {% load i18n %}

    {% block content %}
        <table>
            <thead>
                <tr>
                    <th>{% trans "Location" %}</th>
                    <th>{% trans "Start" %}</th>
                    <th>{% trans "End" %}</th>
                </tr>
            </thead>
            <tdata>
                {% for period in object_list %}
                    {# Activate the timezone for each location #}
                    {% timezone period.location.timezone %}
                        <tr>
                            <td>{{ period.location.name }}</td>
                            <td>{{ period.start }}</td>
                            <td>{{ period.end }}</td>
                        </tr>
                    {% endtimezone %}
                {% empty %}
                    <tr>
                        <td colspan=3>{% trans "No periods to display." %}</td>
                    </tr>
                {% endfor %}
            </tdata>
        </table>
    {% endblock content %}

Inspiration
-----------

On multiple occasions, I have had the need to store time zone information to the
one model, then base another model's datetime on that time zone. If you have
ever had to deal with this, you will know how complicated this can be.

I created these fields to ease the process of manipulating times based on
another field's or models timezone choice. Instead of having to remember to use
``Model.clean_fields``, we can now create the models with the validation built
into the model field.


Contributors
------------

* `Michael Barr <http://github.com/michaeljohnbarr>`_

Changelog
---------

- 0.2 Multiple bug fixes based on testing.
- 0.1 Initial release.

License
=======

The MIT License.
