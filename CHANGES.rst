Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

3.0.0 (2023-04-27)
------------------

Breaking changes:


- Drop Plone 5.2 and Python 2 support.
  [gforcada] (#6)


Internal:


- Update configuration files.
  [plone devs] (2a4ba395)


2.1.4 (2021-06-14)
------------------

Bug fixes:


- Do not throw an error when traversing to a FilesystemResourceDirectory (#31)


2.1.3 (2020-09-28)
------------------

Bug fixes:


- Fixed various warnings.
  [maurits] (#3130)


2.1.2 (2020-04-22)
------------------

Bug fixes:


- Minor packaging updates. (#1)


2.1.1 (2019-02-08)
------------------

Bug fixes:


- Fix deprecation and resource warnings. [gforcada] (#29)


2.1.0 (2018-11-02)
------------------

Bug fixes:

- Fix tests in py3.
  [pbauer, jensens]

- Change name of IResourceDirectoryDirective to TextLine to work with zope.configuration >= 4.2.
  See https://github.com/plone/Products.CMFPlone/issues/2591
  [pbauer]

2.0.2 (2018-06-04)
------------------

Bug fixes:

- More Python 3 fixes.
  [ale, pbauer]


2.0.1 (2018-02-05)
------------------

New features:

- Add python 2 / 3 compatibility


2.0.0 (2018-01-17)
------------------

Breaking changes:

- Remove Python2.6 support.
  [ale-rt]

Bug fixes:

- Fixed 'ValueError: substring not found' in ``FilesystemResourceDirectory`` representation.
  This happens when you register a directory with a name that differs from the directory name.
  Visiting the ``/++theme++myname`` url would then give this error.
  We also avoid listing a longer part of the path in case the directory name happens to be in the path multiple times.
  [maurits]


1.2.1 (2016-12-30)
------------------

Bug fixes:

- 'unittest2' is a test dependency, make this explicit in setup.py.
  [jensens]


1.2 (2016-11-09)
----------------

New features:

- Fire events on resources creation/modification
  [jpgimenez, ebrehault]


1.1 (2016-10-04)
----------------

New features:

- Use ``mimetypes_registry`` utility to determine mimetype if available.
  [jensens]

Bug fixes:

- Remove duplicate import
  [jensens]

- Add coding headers on python files.
  [gforcada]

1.0.7 (2016-09-08)
------------------

Bug fixes:

- Applied 20160830 security hotfix.  [maurits]


1.0.6 (2016-08-10)
------------------

Fixes:

- Do not leave an ``.svn`` file behind when running the tests.  [maurits]

- Use zope.interface decorator.
  [gforcada]


1.0.5 (2016-02-26)
------------------

Fixes:

- Test fix: ``clearZCML`` was removed from ``zope.component.tests``.
  [thet]

- Cleanup: PEP8, plone-coding conventions, ReST fixes, documentation
  overhaul, et al.
  [jensens]


1.0.4 (2015-03-21)
------------------

- use utf-8 encoding when writing more than just text/html
  [vangheem]

- provides a proper __contains__ method in FilesystemResourceDirectory
  [ebrehault]


1.0.3 (2014-10-13)
------------------

- security hardening: we don't want the anonymous user to look at our fs
  [giacomos]


1.0.2 (2013-01-01)
------------------

- Nothing changed yet.


1.0.1 (2012-05-25)
------------------

- Make sure text/html files imported as persistent files will be
  served with a utf-8 encoding. This fixes
  https://dev.plone.org/ticket/12838
  [davisagli]

1.0 (2012-04-15)
----------------

- Add __setitem__() support for writeable resource directories.
  [optilude]

1.0b6 (2011-11-24)
------------------

- Added rename() method for writable resource directories
  [optilude]

- Added cloneResourceDirectory() helper method in the utils module
  [optilude]

- Add a ++unique++ resource traverser for resource directories to cache as
  'plone.stableResource'.
  [elro]

1.0b5 (2011-06-08)
------------------

- Ensure any files are skipped in iterDirectoriesOfType.
  [elro]

1.0b4 (2011-05-29)
------------------

- Add queryResourceDirectory() helper method.
  [optilude]

1.0b3 (2011-05-23)
------------------

- Fix resource directory download bug with subdirectories.
  [elro]

1.0b2 (2011-05-16)
------------------

- Add a more compatible filestream iterator for filesystem files that allows
  coercion to string or unicode. This fixes possible compatibility issues
  with resource merging through Resource Registries.
  [optilude]

1.0b1 (2011-04-22)
------------------

- Initial release
