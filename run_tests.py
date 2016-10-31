# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from datetime import datetime
import pytz
import sys

# Django
from django import VERSION
from django.conf import settings
from django.core.management import execute_from_command_line
from django.utils import timezone

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'timezone_utils',
    'tests',
]

if not settings.configured:
    test_runners_args = {}
    if VERSION < (1, 6):    # pragma: no cover
        INSTALLED_APPS.append('discover_runner')
        test_runners_args = {
            'TEST_RUNNER': 'discover_runner.DiscoverRunner',
        }
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=tuple(INSTALLED_APPS),
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
        ),
        ROOT_URLCONF=None,
        USE_TZ=True,
        TIME_ZONE='UTC',
        SECRET_KEY='secret',
        LANGUAGE_CODE = 'en-us',
        USE_I18N=True,
        USE_L10N=True,
        SITE_ID=1,
        TEST_DATETIME=timezone.make_aware(
            datetime(2014, 1, 1), pytz.timezone('UTC')
        ),
        # SILENCED_SYSTEM_CHECKS=['1_7.W001'],
        **test_runners_args
    )


def runtests():
    argv = sys.argv[:1] + ['test'] + sys.argv[1:]
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
