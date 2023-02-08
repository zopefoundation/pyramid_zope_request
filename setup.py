##############################################################################
#
# Copyright (c) 2013 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import os

from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

install_requires = [
    'pyramid',
    'zope.interface',
    'zope.publisher',
    'zope.testrunner',
]

tests_require = install_requires

testing_extras = [
    'six',  # some zope.publisher versions miss to declare the dep.
    'zope.browserpage',  # some z3c.form misses this
    'z3c.form [test]',
]

setup(name='pyramid_zope_request',
      version='1.0.dev0',
      description='Zope publisher request support for Pyramid',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: Implementation :: CPython',
          'Framework :: Pylons',
          'Framework :: Zope :: 3',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: WSGI',
          'License :: OSI Approved :: Zope Public License',
      ],
      keywords='web wsgi pylons pyramid zope3 webob',
      author="Adam Groszer and the Zope Community",
      author_email="zope-dev@zope.org",
      url='https://github.com/zopefoundation/pyramid_zope_request',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite="pyramid_zope_request",
      extras_require={
          'test': testing_extras,
      },
      entry_points="""
      """
      )
