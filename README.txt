Introduction
============

``plone.resource`` publishes directories of static files via the ZPublisher.
These directories may be located either in the ZODB (as OFS folders and
files), or on the filesystem.

Each resource directory has a type and a name. When combined, these are used
to traverse to the resource directory. For example::

    /++theme++mytheme/<subpath>
    /++sitelayout++mylayout/<subpath>
    /++templatelayout++mylayout<subpath>


Where resources can be stored
-----------------------------

Resource directory contents can be found by the traverser in several different
places. The following locations are tried in order.

Files in the ZODB
  Installing ``plone.resource`` creates a folder called portal_resources which
  can be used to store resource directories persistently. By convention, the
  top-level folders under this folder correspond to resource types, and the
  second-level folders correspond to the resource directory name.
  
  So, the file traversable at /++theme++mytheme/myfile could be physically
  located at some_site/++etc++site/resources/theme/mytheme

  (XXX: provide a helper to upload a tarball/zip)


Files in Python distributions

  A folder in a Python distribution (e.g. egg) can be registered as a resource
  directory of a particular type and name using the plone:static ZCML
  directive.  For example, this registers a directory named "theme" as a
  resource directory of type "theme". It would be accessible at 
  ++theme++mytheme::
  
    <plone:static
      directory="theme"
      type="theme"
      name="mytheme"
      />
  
  .. note::
     You must do ``<include package="plone.resource" file="meta.zcml"/>``
     before you can use the plone:static directive.
  
  The name of the resource directory defaults to the name of the package, so
  can be omitted. e.g. the following directive in a package named "mytheme"
  would result in the same registration as above::
  
    <plone:static
      directory="resources"
      type="theme"
      />
  
  Traversing upward in directory paths using .. is not supported, as it could
  allow unwanted file access.

Files in a central resource directory

    If the plone:static directive is used from site.zcml (i.e., with
    no active package in the ZCML import context), then it may specify the
    absolute path to a top-level resources directory.  This should have the
    same subdirectory structure as the in-ZODB resources directory (i.e.,
    top-level directories are resource types and 2nd-level directories are
    resource directory names).
    
    For example, the following in site.zcml would register the path
    var/resources within the buildout root::
    
      <plone:static
        directory="/path/to/buildout/var/resources"
        />

    Typically, this could be injected into site.zcml by specifying the 
    resources option in the `plone.recipe.zope2instance`_
    buildout recipe, like this::

      resources = ${buildout:directory}/resources

.. _`plone.recipe.zope2instance`: http://pypi.python.org/pypi/plone.recipe.zope2instance
 

What types of resources can be stored
-------------------------------------

