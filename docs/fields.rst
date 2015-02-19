======
Fields
======
Contains timezone-related fields.

.. _TimeZoneField:

TimeZoneField
-------------
.. |django.core.exceptions.ValidationError| replace:: ``django.core.exceptions.ValidationError``
.. _django.core.exceptions.ValidationError: https://docs.djangoproject.com/en/dev/ref/exceptions/#django.core.exceptions.ValidationError

.. |datetime.tzinfo| replace:: ``datetime.tzinfo``
.. _datetime.tzinfo: https://docs.python.org/2/library/datetime.html#tzinfo-objects

.. |models.CharField| replace:: ``models.CharField``
.. _models.CharField: https://docs.djangoproject.com/en/dev/ref/models/fields/#charfield

.. |None| replace:: ``None``
.. _None: https://docs.python.org/2/library/constants.html#None

.. |models.DateTimeField| replace:: ``models.DateTimeField``
.. _models.DateTimeField: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateTimeField

..  |datetime.time| replace:: ``datetime.time``
..  _datetime.time: https://docs.python.org/2/library/datetime.html#time-objects

.. |pytz.all_timezones| replace:: ``pytz.all_timezones``
.. _pytz.all_timezones: http://pytz.sourceforge.net/#helpers

.. py:class:: TimeZoneField(*args, **kwargs)

    A |models.CharField|_ subclass that stores a valid Olson Timezone string
    found in |pytz.all_timezones|_ to the database.

    :raises |django.core.exceptions.ValidationError|_: if the value is not a valid Olson Time zone string.
    :return: A |datetime.tzinfo|_ object based on the value or |None|_.
    :rtype: |datetime.tzinfo|_

.. code-block:: python

    from timezone_utils.fields import TimeZoneField
    from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES

    class Location(models.Model):
        # ...
        timezone = TimeZoneField(choices=PRETTY_ALL_TIMEZONES_CHOICES)

You can pass a default Olson timezone value to the model as a string:

.. code-block:: python

    from timezone_utils.fields import TimeZoneField

    class Location(models.Model):
        # ...
        timezone = TimeZoneField(default='US/Pacific')

You can also pass a default Olson timezone value to the model as a
``pytz.timezone`` instance:

.. code-block:: python

    import pytz
    from timezone_utils.fields import TimeZoneField

    class Location(models.Model):
        # ...
        timezone = TimeZoneField(default=pytz.timezone('US/Eastern'))

Accessing a ``TimeZoneField`` on a model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
As a convenience, ``TimeZoneField`` automatically converts its model instance
attribute representation to a ``pytz.timezone`` instance:

.. code-block:: python

    >>> from datetime import datetime
    >>> from django.utils.timezone import make_aware
    >>> from app_label.models import Location
    >>> location = Location.objects.create(timezone='US/Eastern')
    >>> print(location.timezone)
    <DstTzInfo 'US/Eastern' LMT-1 day, 19:04:00 STD>
    >>> unaware_dt = datetime(2015, 1, 1)
    >>> aware_dt = make_aware(unaware_dt, location.timezone)
    >>> print(aware_dt)
    datetime.datetime(2015, 1, 1, 0, 0, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)


.. _LinkedTZDateTimeField:

LinkedTZDateTimeField
---------------------

.. py:class:: LinkedTZDateTimeField(populate_from=None, time_override=None, *args, **kwargs)

    A |models.DateTimeField|_ subclass that will automatically save a datetime object
    as a particular time zone as declared in the kwarg ``populate_from``. You can
    also override the time each time the object is saved with the kwarg
    ``time_override``, which must be a |datetime.time|_ instance.

    :param populate_from: The location of the field which contains the time zone
                          that will be used for this field. Must be either a
                          function which returns a ``models.ForeignKey`` path to
                          the timezone or a string (if the timezone field is
                          located on the model).
    :param time_override: Automatically overrides the time value each time the
                          object is saved to the time that is declared.Must be a
                          |datetime.time|_ instance.

.. note:: If ``auto_now`` or ``auto_now_add`` is declared, the value of ``time_override`` is ignored.
.. caution:: `Django cannot serialize lambdas! <https://docs.djangoproject.com/en/1.7/ref/models/fields/#default>`_
   If you provide a ``lambda`` for ``populate_from``, your model will fail to
   migrate in Django 1.7+.


.. code-block:: python

    from datetime import datetime
    from timezone_utils.fields import LinkedTZDateTimeField, TimeZoneField
    from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES

    class Location(models.Model):
        # ...
        timezone = TimeZoneField(choices=PRETTY_ALL_TIMEZONES_CHOICES)


    def get_location_timezone(obj):
        return obj.location.timezone


    class LocationReport(models.Model):
        # ...
        location = models.ForeignKey('app_label.Location', related_name='reports')
        timestamp = LinkedTZDateTimeField(populate_from=get_location_timezone)


    class LocationPeriod(models.Model):
        # ...
        location = models.ForeignKey('app_label.Location', related_name='reports')
        start = LinkedTZDateTimeField(
            populate_from=get_location_timezone,
            time_override=datetime.min.time()
        )
        end = LinkedTZDateTimeField(
            populate_from=get_location_timezone,
            time_override=datetime.max.time()
        )

Accessing a ``LinkedTZDateTimeField`` on a model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
As a convenience, ``LinkedTZDateTimeField`` automatically converts its model
instance attribute representation to the time zone declared in the
``populate_from``, regardless of what ``settings.TIME_ZONE`` is set to:

.. code-block:: python

    >>> from datetime import datetime
    >>> from app_label.models import LocationPeriod
    >>> location = location.objects.get(pk=1)
    >>> location_period = LocationPeriod.objects.create(location=location, start=datetime(2015, 1, 1), end=datetime(2015, 12, 31))
    >>> print(location_period.start)
    datetime.datetime(2015, 1, 1, 0, 0, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)
    >>> print(location_period.end)
    datetime.datetime(2015, 12, 31, 23, 59, 59, 999999, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)


Accessing a ``LinkedTZDateTimeField`` in templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Django templates will automatically cast the timezones to the currently-activated
time zone for the user viewing the page. An example of how to display our fields
with the appropriate time zone would look something like this:

**app_label/views.py:**

.. code-block:: python

    # Django
    from django.views.generic import ListView

    # App
    from app_label.models import LocationPeriod


    class LocationReportingPeriodListView(ListView):
        model = LocationPeriod
        template_name = 'app_label/location_period_list.html'

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

**templates/app_label/location_period_list.html:**

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
