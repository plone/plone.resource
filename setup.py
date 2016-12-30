# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.2.1'

setup(
    name='plone.resource',
    version=version,
    description="Static files for Plone",
    long_description=(
        open("README.rst").read() +
        "\n" +
        open("CHANGES.rst").read()
    ),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='plone resource',
    author='David Glick, Plone Foundation',
    author_email='davidglick@groundwire.org',
    url='https://pypi.python.org/pypi/plone.resource',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.caching',
        'python-dateutil',
        'setuptools',
        'z3c.caching',
        'zope.component',
        'zope.configuration',
        'zope.filerepresentation',
        'zope.interface',
        'zope.publisher',
        'zope.schema',
        'zope.traversing',
        'Zope2',
    ],
    extras_require={
        'test': [
	    'plone.app.testing',
            'unittest2',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
