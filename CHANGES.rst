Changelog
=========

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

- Use ``mimetypes_registry`` utility to dertermine mimetype if available.
  [jensens]

Bug fixes:

- Remove duplicte import
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
