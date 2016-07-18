========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/staps/badge/?style=flat
    :target: https://readthedocs.org/projects/staps
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/fladi/staps.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/fladi/staps

.. |requires| image:: https://requires.io/github/fladi/staps/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/fladi/staps/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/fladi/staps/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/fladi/staps

.. |version| image:: https://img.shields.io/pypi/v/staps.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/staps

.. |downloads| image:: https://img.shields.io/pypi/dm/staps.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/staps

.. |wheel| image:: https://img.shields.io/pypi/wheel/staps.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/staps

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/staps.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/staps

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/staps.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/staps


.. end-badges

Simple Throw-Away Publish/Subscribe. Create channels simply by connecting one or mote websocket clients to a random URL path on a webserver with staps. Not
meant to be used with webbrowsers but as a cheap way to let multiple websocket clients written outside the browser communicate with each other.

* Free software: BSD license

Installation
============

::

    pip install staps

Documentation
=============

https://staps.readthedocs.io/en/latest/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
