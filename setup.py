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
        'django>=1.4,<1.10'
    ],
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries',
    ],
    url='http://github.com/michaeljohnbarr/django-timezone-utils/',
)
