# -*- coding: utf-8 -*-
from plone.resource.interfaces import IResourceDirectory
from zExceptions import NotFound
from zope.component import getUtilitiesFor
from zope.component import queryUtility


def iterDirectoriesOfType(type, filter_duplicates=True):
    """
    Returns a generator which iterates over all resource directories of a
    particular resource type.

    If ``filter_duplicates`` is True and multiple resource directory trees
    contain resource directories with identical names, only the
    first one found will be returned for each name. The following sources are
    checked in order:
    - the persistent portal_resources tool
    - the global resource directory
    - resource directories in distributions
    """

    found = set()

    # 1. Persistent resource directory:
    #    List (persistent resource directory)/$type
    res = queryUtility(IResourceDirectory, name=u'persistent')
    if res and res.isDirectory(type):
        typedir = res[type]
        for dirname in typedir.listDirectory():
            if not typedir.isDirectory(dirname):
                continue
            yield typedir[dirname]
            found.add(dirname)

    # 2. Global resource directory:
    #    List (global resource directory)/$type
    res = queryUtility(IResourceDirectory, name=u'')
    if res and res.isDirectory(type):
        typedir = res[type]
        for dirname in typedir.listDirectory():
            if not typedir.isDirectory(dirname):
                continue
            if not filter_duplicates or dirname not in found:
                yield typedir[dirname]
                found.add(dirname)

    # 3. Packaged resource directories:
    #    Scan the registry
    identifier = '++%s++' % type
    for name, u in getUtilitiesFor(IResourceDirectory):
        if name.startswith(identifier):
            if not filter_duplicates or u.__name__ not in found:
                yield u


def queryResourceDirectory(type, name):
    """Find the IResourceDirectory of the given name and type. Returns
    None if not found.
    """

    # 1. Persistent resource directory:
    #    Try (persistent resource directory)/$type/$name
    res = queryUtility(IResourceDirectory, name=u'persistent')
    if res:
        try:
            return res[type][name]
        except (KeyError, NotFound,):
            pass  # pragma: no cover

    # 2. Global resource directory:
    #    Try (global resource directory)/$type/$name
    res = queryUtility(IResourceDirectory, name=u'')
    if res:
        try:
            return res[type][name]
        except (KeyError, NotFound,):
            pass  # pragma: no cover

    # 3. Packaged type-specific resource directory:
    #    Try (directory named after type + name)
    identifier = u'++%s++%s' % (type, name)
    res = queryUtility(IResourceDirectory, name=identifier)
    if res is not None:
        return res

    return None


def cloneResourceDirectory(source, target):
    """Copy all directories and files in the resource directory source to
    the writable resource directory target
    """

    for name in source.listDirectory():
        if source.isDirectory(name):
            target.makeDirectory(name)
            cloneResourceDirectory(source[name], target[name])
        else:
            f = source.openFile(name)
            try:
                target.writeFile(name, f)
            finally:
                f.close()

