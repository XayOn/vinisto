#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Vinisto
"""

from setuptools import setup, find_packages


with open('docs/Readme.rst') as readme_file:
    README = readme_file.read()

with open('docs/History.rst') as history_file:
    HISTORY = history_file.read().replace('.. :changelog:', '')

setup(
    name='vinisto',
    version='0.2.2',
    description="""
        Vinisto - a simple-minded home butler
    """,
    long_description=README + '\n\n' + HISTORY,
    author="David Francos Cuartero",
    author_email='me@davidfrancos.net',
    url='https://github.com/XayOn/vinisto',
    packages=find_packages(exclude=["tests", "docs"]),
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
