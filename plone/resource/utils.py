from zope.component import queryUtility, getUtilitiesFor
from plone.resource.interfaces import IResourceDirectory


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
            yield typedir[dirname]
            found.add(dirname)
    
    # 2. Global resource directory:
    #    List (global resource directory)/$type
    res = queryUtility(IResourceDirectory, name=u'')
    if res and res.isDirectory(type):
        typedir = res[type]
        for dirname in typedir.listDirectory():
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
