#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016, OpenServices e.U.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN

# Standard Library
import io
import re
from os.path import dirname
from os.path import join

from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='staps',
    version='0.1.6',
    license='BSD',
    description='Simple Throw-Away Publish/Subscribe',
    long_description='%s\n%s' % (
        re.compile(
            '^.. start-badges.*^.. end-badges', re.M | re.S
        ).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Michael Fladischer',
    author_email='michael@openservices.at',
    url='https://github.com/fladi/staps',
    packages=['staps'],
    package_dir={'staps': 'src/staps'},
    package_data={'staps': ['*.html']},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords=[
        'amqp',
        'websockets',
        'tornado',
        'pubsub',
        'publish',
        'subscribe'
    ],
    install_requires=[
        'cement',
        'pika',
        'tornado',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'staps = staps.cli.__main__:main',
        ]
    },
)
