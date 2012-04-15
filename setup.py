from setuptools import setup, find_packages

version = '1.0'

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
      author='David Glick, Plone Foundation',
      author_email='davidglick@groundwire.org',
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
          'plone.caching',
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
