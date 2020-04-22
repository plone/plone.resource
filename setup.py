# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '2.1.2'

test_requires = [
    'plone.app.testing',
]

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
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords='plone resource',
    author='David Glick, Plone Foundation',
    author_email='davidglick@groundwire.org',
    url='https://pypi.org/project/plone.resource',
    license='GPL version 2 or later',
    packages=find_packages(),
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
        'six',
    ],
    extras_require={
        'test': test_requires,
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
