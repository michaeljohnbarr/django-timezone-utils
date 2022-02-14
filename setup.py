# coding: utf-8
from setuptools import setup
import os

version = __import__('timezone_utils').VERSION


setup(
    name='django-timezone-utils',
    version=version,
    description='Time Zone Utilities for Django Models',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            "README.rst"
        )
    ).read(),
    author="Michael Barr",
    author_email="micbarr+developer@gmail.com",
    license="MIT",
    packages=['timezone_utils'],
    install_requires=[
        'pytz',
        'django>=1.11'
    ],
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries',
    ],
    url='http://github.com/michaeljohnbarr/django-timezone-utils/',
)
