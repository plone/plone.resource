# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.0.5.dev0'

setup(
    name='plone.resource',
    version=version,
    description="",
    long_description=(
        open("README.rst").read() +
        "\n" +
        open("CHANGES.txt").read()
    ),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone : 4.3",
        "Framework :: Plone : 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='',
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
        'test': ['plone.app.testing']
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
