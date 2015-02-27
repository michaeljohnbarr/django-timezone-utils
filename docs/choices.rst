=======
Choices
=======
Contains constants and functions to generate model/form choices for time zones.

``ALL_TIMEZONES_CHOICES``
-------------------------
.. |pytz.all_timezones| replace:: ``pytz.all_timezones``
.. _pytz.all_timezones: http://pytz.sourceforge.net/#helpers

.. py:data:: ALL_TIMEZONE_CHOICES

    Returns choices directly populated from |pytz.all_timezones|_.

.. code-block:: python

    >>> from timezone_utils.choices import ALL_TIMEZONES_CHOICES
    >>> print ALL_TIMEZONES_CHOICES
    (
        ('Africa/Abidjan', 'Africa/Abidjan'),
        ('Africa/Accra', 'Africa/Accra'),
        ('Africa/Addis_Ababa', 'Africa/Addis_Ababa'),
        ('Africa/Algiers', 'Africa/Algiers'),
        ('Africa/Asmara', 'Africa/Asmara'),
        ('Africa/Asmera', 'Africa/Asmera'),
        ('Africa/Bamako', 'Africa/Bamako'),
        ('Africa/Bangui', 'Africa/Bangui'),
        ('Africa/Banjul', 'Africa/Banjul'),
        ('Africa/Bissau', 'Africa/Bissau'),
        ...
    )

``COMMON_TIMEZONES_CHOICES``
----------------------------
.. |pytz.common_timezones| replace:: ``pytz.common_timezones``
.. _pytz.common_timezones: http://pytz.sourceforge.net/#helpers

.. py:data:: COMMON_TIMEZONE_CHOICES

    Returns choices directly populated from |pytz.common_timezones|_.

.. code-block:: python

    >>> from timezone_utils.choices import COMMON_TIMEZONES_CHOICES
    >>> print COMMON_TIMEZONES_CHOICES
    (
        ('Africa/Abidjan', 'Africa/Abidjan'),
        ('Africa/Accra', 'Africa/Accra'),
        ('Africa/Addis_Ababa', 'Africa/Addis_Ababa'),
        ('Africa/Algiers', 'Africa/Algiers'),
        ('Africa/Asmara', 'Africa/Asmara'),
        ('Africa/Bamako', 'Africa/Bamako'),
        ('Africa/Bangui', 'Africa/Bangui'),
        ('Africa/Banjul', 'Africa/Banjul'),
        ('Africa/Bissau', 'Africa/Bissau'),
        ('Africa/Blantyre', 'Africa/Blantyre'),
        ...
    )

``GROUPED_ALL_TIMEZONES_CHOICES``
---------------------------------
.. py:data:: GROUPED_ALL_TIMEZONES_CHOICES

    Returns choices grouped by the timezone offset and ordered alphabetically by
    their Olson Time Zone name populated from |pytz.all_timezones|_.

.. code-block:: python

    >>> from timezone_utils.choices import GROUPED_ALL_TIMEZONES_CHOICES
    >>> print GROUPED_ALL_TIMEZONES_CHOICES
    (
        (
            'GMT-12:00',
            (
                ('Etc/GMT+12', 'Etc/GMT+12'),
            )
        ),
        (
            'GMT-11:00',
            (
                ('Etc/GMT+11', 'Etc/GMT+11'),
                ('Pacific/Midway', 'Pacific/Midway'),
                ('Pacific/Niue', 'Pacific/Niue'),
                ('Pacific/Pago_Pago', 'Pacific/Pago_Pago'),
                ('Pacific/Samoa', 'Pacific/Samoa'),
                ('US/Samoa', 'US/Samoa')
            )
        ),
        ...
    )

``GROUPED_COMMON_TIMEZONES_CHOICES``
------------------------------------
.. py:data:: GROUPED_COMMON_TIMEZONES_CHOICES

    Returns choices grouped by the timezone offset and ordered alphabetically by
    their Olson Time Zone name populated from |pytz.common_timezones|_.

.. code-block:: python

    >>> from timezone_utils.choices import GROUPED_ALL_TIMEZONES_CHOICES
    >>> print GROUPED_ALL_TIMEZONES_CHOICES
    (
        (
            'GMT-11:00',
            (
                ('Pacific/Midway', 'Pacific/Midway'),
                ('Pacific/Niue', 'Pacific/Niue'),
                ('Pacific/Pago_Pago', 'Pacific/Pago_Pago')
            )
        ),
        (
            'GMT-10:00',
            (
                ('America/Adak', 'America/Adak'),
                ('Pacific/Honolulu', 'Pacific/Honolulu'),
                ('Pacific/Johnston', 'Pacific/Johnston'),
                ('Pacific/Rarotonga', 'Pacific/Rarotonga'),
                ('Pacific/Tahiti', 'Pacific/Tahiti'),
                ('US/Hawaii', 'US/Hawaii')
            )
        ),
        (
            'GMT-09:30',
            (
                ('Pacific/Marquesas', 'Pacific/Marquesas'),
            )
        ),
        ...
    )

``PRETTY_ALL_TIMEZONES_CHOICES``
--------------------------------
.. py:data:: PRETTY_ALL_TIMEZONES_CHOICES

    Returns choices formatted for display ordered by their timezone offsets
    populated from |pytz.all_timezones|_.

.. code-block:: python

    >>> from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES
    >>> print PRETTY_ALL_TIMEZONES_CHOICES
    (
        ('Etc/GMT+12', '(GMT-12:00) Etc/GMT+12'),
        ('Etc/GMT+11', '(GMT-11:00) Etc/GMT+11'),
        ('Pacific/Midway', '(GMT-11:00) Pacific/Midway'),
        ('Pacific/Niue', '(GMT-11:00) Pacific/Niue'),
        ('Pacific/Pago_Pago', '(GMT-11:00) Pacific/Pago_Pago'),
        ('Pacific/Samoa', '(GMT-11:00) Pacific/Samoa'),
        ('US/Samoa', '(GMT-11:00) US/Samoa'),
        ('America/Adak', '(GMT-10:00) America/Adak'),
        ('America/Atka', '(GMT-10:00) America/Atka'),
        ('Etc/GMT+10', '(GMT-10:00) Etc/GMT+10'),
        ...
    )

``PRETTY_COMMON_TIMEZONES_CHOICES``
-----------------------------------
.. py:data:: PRETTY_COMMON_TIMEZONES_CHOICES

    Returns choices formatted for display ordered by their timezone offsets
    populated from  |pytz.common_timezones|_.

.. code-block:: python

    >>> from timezone_utils.choices import PRETTY_COMMON_TIMEZONES_CHOICES
    >>> print PRETTY_COMMON_TIMEZONES_CHOICES
    (
        ('Pacific/Midway', '(GMT-11:00) Pacific/Midway'),
        ('Pacific/Niue', '(GMT-11:00) Pacific/Niue'),
        ('Pacific/Pago_Pago', '(GMT-11:00) Pacific/Pago_Pago'),
        ('America/Adak', '(GMT-10:00) America/Adak'),
        ('Pacific/Honolulu', '(GMT-10:00) Pacific/Honolulu'),
        ('Pacific/Johnston', '(GMT-10:00) Pacific/Johnston'),
        ('Pacific/Rarotonga', '(GMT-10:00) Pacific/Rarotonga'),
        ('Pacific/Tahiti', '(GMT-10:00) Pacific/Tahiti'),
        ('US/Hawaii', '(GMT-10:00) US/Hawaii'),
        ('Pacific/Marquesas', '(GMT-09:30) Pacific/Marquesas'),
        ...
    )

``get_choices(timezones, grouped=False)``
-----------------------------------------
.. py:function:: get_choices(timezones, grouped=False)

        Retrieves timezone choices from any iterable (normally from `pytz <pytz.sourceforge.net/>`_).

        :param timezones: Any iterable that contains valid Olson Time Zone strings.
        :type timezones: iterable
        :param grouped: Whether to group the choices by time zone offset.
        :type grouped: bool
        :return: A tuple containing tuples of time zone choices.
        :rtype: tuple
        :raises pytz.exceptions.UnknownTimeZoneError: if the string from the iterable ``timezones``
                                                      parameter is not recognized as a valid Olson time zone.
        :raises TypeError: if the ``timezones`` parameter is not iterable.

Using ``get_choices(timezones)`` for custom time zone choices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to limit choices to a particular country (as an example), you could
do this:

.. code-block:: python

    >>> import pytz
    >>> from timezone_utils.choices import get_choices
    >>> choices = get_choices(pytz.country_timezones('US'))
    >>> print choices
    (
        (u'America/Adak', '(GMT-10:00) America/Adak'),
        (u'Pacific/Honolulu', '(GMT-10:00) Pacific/Honolulu'),
        (u'America/Anchorage', '(GMT-09:00) America/Anchorage'),
        (u'America/Juneau', '(GMT-09:00) America/Juneau'),
        (u'America/Nome', '(GMT-09:00) America/Nome'),
        (u'America/Sitka', '(GMT-09:00) America/Sitka'),
        (u'America/Yakutat', '(GMT-09:00) America/Yakutat'),
        (u'America/Los_Angeles', '(GMT-08:00) America/Los_Angeles'),
        (u'America/Metlakatla', '(GMT-08:00) America/Metlakatla'),
        (u'America/Boise', '(GMT-07:00) America/Boise'),
        (u'America/Denver', '(GMT-07:00) America/Denver'),
        ...
    )
