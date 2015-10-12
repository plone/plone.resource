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
        "Programming Language :: Python",
    ],
    keywords='',
    author='David Glick, Plone Foundation',
    author_email='davidglick@groundwire.org',
    url='https://svn.plone.org/svn/plone/plone.resource',
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
