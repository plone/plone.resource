Introduction
============

``plone.resource`` publishes directories of static files via the ZPublisher.
These directories may be located either in the ZODB (as OFS folders and files), or on the filesystem.

Each resource directory has a type and a name. When combined, these are used to traverse to the resource directory.
For example::

    /++theme++mytheme/<subpath>
    /++sitelayout++mylayout/<subpath>
    /++templatelayout++mylayout<subpath>


Where resources can be stored
-----------------------------

Resource directory contents can be found by the traverser in several different places.
The following locations are tried in order.

Files in the ZODB
^^^^^^^^^^^^^^^^^

Installing ``plone.resource`` creates a Zope-folder called ``portal_resources``.
It can be used to store resource directories persistently.
By convention:

- the top-level folders under this folder correspond to resource types,
- the second-level folders correspond to the resource directory name.

So, the file traversable at ``/++theme++mytheme/myfile`` could be physically located at ``some_site/++etc++site/resources/theme/mytheme``

.. TODO (XXX: provide a helper to upload a tarball/zip)


Files in Python distributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A folder in a Python distribution (e.g. egg) can be registered as a resource directory of a particular type and name using the ``plone:static`` ZCML directive.
For example, this registers a directory named "theme" as a resource directory of type "theme" under the name "mytheme".
It would be accessible at ``++theme++mytheme``::

    <plone:static
        directory="theme"
        type="theme"
        name="mytheme"
    />

  .. note::
     You must do ``<include package="plone.resource" file="meta.zcml"/>``
     before you can use the plone:static directive.

The name of the resource directory defaults to the name of the package, so can be omitted.
E.g. the following directive in a package named "mytheme" would result in the same registration as above::

    <plone:static
        directory="resources"
        type="theme"
    />

Traversing upward in directory paths using ``..`` is not supported for security reasons, as it could allow unwanted file access.

Minimum zcml config example
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    <configure xmlns:plone="http://namespaces.plone.org/plone">
      <include package="plone.resource" file="meta.zcml"/>
      <plone:static
          directory="resources"
          type="theme"
          name="myproject"
        />
    </configure>

    ..

Files in a central resource directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the ``plone:static`` directive is used from ``site.zcml`` (i.e., with no active package in the ZCML import context),
then it may specify the absolute path to a top-level resources directory.

This directory should have the same sub-directory structure as explained above (in-ZODB resources directory):

- the top-level folders under this folder correspond to resource types,
- the second-level folders correspond to the resource directory name.

In addition, in order for resources to be available, the top-level directories *require a traverser* to be registered!

For example, the following in ``site.zcml`` registers the given path within the buildout root::

    <plone:static
        directory="/path/to/buildout/resources"
    />

In order to automate this at buildout time, `plone.recipe.zope2instance`_  recipe has the option ``resources``.
It injects the above zcml snippet with into ``site.zcml`` by specifying the option like this::

      [instance]
      ...
      resources = ${buildout:directory}/resources
      ...

Example:
Using ``plone.app.theming`` - which provides the ``++theme++`` traverser - given an image file located in filesystem at::

    ${buildout:directory}/resources/theme/my.project/logo.png``

This would be traversable at a URL like so::

    http://localhost:8080/Plone/++theme++my.project/logo.png

.. _`plone.recipe.zope2instance`: http://pypi.python.org/pypi/plone.recipe.zope2instance

Additional traversers
---------------------

Custom traversers can be registered via ZCML using an adapter like so::

    <adapter
        name="demo"
        for="* zope.publisher.interfaces.IRequest"
        provides="zope.traversing.interfaces.ITraversable"
        factory="my.project.traversal.MyTraverser"
    />

with a corresponding simple factory definition of::

    from plone.resource.traversal import ResourceTraverser
    class MyTraverser(ResourceTraverser):
        name = 'demo'

This, when coupled with configuration like that in the `Files in a central resource directory`_ section above, would mean that resources located at::

    ${buildout:directory}/resources/demo/my.project/logo.png

would be traversable at a URL like so::

    http://localhost:8080/Plone/++demo++my.project/logo.png

.. TODO: What types of resources can be stored

