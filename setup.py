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

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

install_requires = [
    'pyramid',
    'zope.interface',
    'zope.publisher',
]

tests_require = install_requires

testing_extras = ['six',  # some zope.publisher versions miss to declare the dep.
                  'zope.browserpage',  # some z3c.form misses this
                  'z3c.form [test]']

setup(name='pyramid_zope_request',
      version='0.2.dev0',
      description='Zope publisher request support for Pyramid',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
      "Intended Audience :: Developers",
      "Programming Language :: Python",
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 2.6",
      "Programming Language :: Python :: 2.7",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.3",
      "Programming Language :: Python :: Implementation :: CPython",
      "Framework :: Pylons",
      'Framework :: Zope3',
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Internet :: WWW/HTTP :: WSGI",
      'License :: OSI Approved :: Zope Public License',
      ],
      keywords='web wsgi pylons pyramid zope3 webob',
      author="Adam Groszer and the Zope Community",
      author_email="zope-dev@zope.org",
      url='http://pypi.python.org/pypi/pyramid_zope_request',
      license='ZPL 2.1',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite="pyramid_zope_request",
      extras_require={
          'testing': testing_extras,
      },
      entry_points="""
      """
      )
