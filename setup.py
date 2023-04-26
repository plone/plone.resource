from setuptools import find_packages
from setuptools import setup


version = "3.0.0"

test_requires = [
    "plone.app.testing",
    "plone.testing",
]

setup(
    name="plone.resource",
    version=version,
    description="Static files for Plone",
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="plone resource",
    author="David Glick, Plone Foundation",
    author_email="davidglick@groundwire.org",
    url="https://pypi.org/project/plone.resource",
    license="GPL version 2 or later",
    packages=find_packages(),
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "plone.caching",
        "python-dateutil",
        "setuptools",
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
