from setuptools import setup, find_packages

version = '1.0b3'

setup(name='plone.resource',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='https://svn.plone.org/svn/plone/plone.resource',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.interface',
          'zope.component',
          'zope.traversing',
          'zope.publisher',
          'zope.configuration',
          'zope.schema',
          'zope.filerepresentation',
          'z3c.caching',
          'python-dateutil',
          'Zope2',
      ],
      extras_require = {
          'test': ['plone.app.testing']
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
