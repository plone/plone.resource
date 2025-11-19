from pathlib import Path
from setuptools import setup


version = "4.0.0a1"

test_requires = [
    "plone.app.testing",
    "plone.testing",
]

long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)

setup(
    name="plone.resource",
    version=version,
    description="Static files for Plone",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="plone resource",
    author="David Glick, Plone Foundation",
    author_email="davidglick@groundwire.org",
    url="https://pypi.org/project/plone.resource",
    license="GPL version 2 or later",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "plone.caching",
        "python-dateutil",
        "z3c.caching",
        "Zope",
        "Products.BTreeFolder2",
        "Products.CMFCore",
        "Products.GenericSetup",
    ],
    extras_require={
        "test": test_requires,
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
