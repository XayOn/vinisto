#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Vinisto
"""


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('docs/Readme.rst') as readme_file:
    README = readme_file.read()

with open('docs/History.rst') as history_file:
    HISTORY = history_file.read().replace('.. :changelog:', '')

setup(
    name='vinisto',
    version='0.1.1',
    description="""
        Vinisto - a simple-minded home butler
    """,
    long_description=README + '\n\n' + HISTORY,
    author="David Francos Cuartero",
    author_email='me@davidfrancos.net',
    url='https://github.com/XayOn/vinisto',
    packages=[
        'vinisto',
    ],
    package_dir={'vinisto':
                 'vinisto'},
    include_package_data=True,
    install_requires=[
        'gtts',
        'speechrecognition',
        #'pygame'
    ],
    license="BSD",
    zip_safe=False,
    keywords='vinisto',
    entry_points={
        'console_scripts': [
            'vinisto = vinisto.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests'
)
