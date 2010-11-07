Introduction
============

``plone.resource`` publishes directories of static files via the ZPublisher.
These directories may be located either in the ZODB (as OFS folders and files),
or on the filesystem.

Each resource directory has a type and a name. When combined, these are used to
traverse to the resource directory.  For example::

    /++theme++mytheme/<subpath>
    /++sitelayout++mylayout/<subpath>
    /++templatelayout++mylayout<subpath>


Where resources can be stored
-----------------------------

Resource directory contents can be found by the traverser in several different
places. The following locations are tried in order.

Files in the ZODB
  Installing ``plone.resource`` creates a folder called portal_resources
  which can be used to store resource directories persistently. By convention,
  the top-level folders under this folder correspond to resource types, and the
  second-level folders correspond to the resource directory name.
  
  So, the file traversable at /++theme++mytheme/myfile could be physically
  located at some_site/++etc++site/resources/theme/mytheme

  (XXX: provide a helper to upload a tarball/zip)


Files in Python distributions

  A folder in a Python distribution (e.g. egg) can be registered as a resource
  directory using the plone:resourceDirectory ZCML directive.  For example,
  this registers a "resources" directory with the name "mytheme"::
  
    <plone:resourceDirectory
      directory="resources"
      name="mytheme"
      />
  
  .. note::
     You must do ``<include package="plone.resource" file="meta.zcml"/>``
     before you can use the plone:resourceDirectory directive.
  
  Since no resource type is specified, plone.resource expects subdirectories
  for each resource type is that is supplied. So a theme resource could be
  placed at resources/theme/myfile (relative to the package where the
  ZCML is located), and would be accessible at ++theme++mytheme/myfile.
  
  The name of the resource directory defaults to the name of the package, so can
  be omitted. e.g. the following directive in a package named "mytheme" would
  result in the same registration as above::
  
    <plone:resourceDirectory
      directory="resources"
      />
  
  (XXX don't allow absolute path in this case)
  
  A resource type can optionally be specified on the directive. In this case,
  no subdirectory named for the resource type should be present.  e.g. the
  following directive in the mytheme package would make a file placed at
  theme/myfile available at the URL ++theme++mytheme/myfile::
  
    <plone:resourceDirectory
      directory="theme"
      type="theme"
      />
  
  Traversing upward in directory paths using .. is not supported, as it could
  allow unwanted file access.

Files in a central resource directory

    If the plone:resourceDirectory directive is used from site.zcml (i.e., with
    no active package in the ZCML import context), then it may specify the
    absolute path to a top-level resources directory.  This should have the
    same subdirectory structure as the in-ZODB resources directory (i.e.,
    top-level directories are resource types and 2nd-level directories are
    resource directory names).
    
    For example, the following in site.zcml would register the path
    var/resources within the buildout root:
    
      <plone:resourceDirectory
        directory="/path/to/buildout/var/resources"
        />

    (Typically, this could be injected into site.zcml by specifying the 
    zcml_additional option in the plone.recipe.zope2instance buildout recipe.)


What types of resources can be stored
-------------------------------------

A new resource type traverser can be registered using the plone:resourceType
ZCML directive.
