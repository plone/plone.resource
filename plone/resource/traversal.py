import urllib
from zope.component import queryUtility
from zope.traversing.namespace import SimpleHandler
from plone.resource.interfaces import IResourceDirectory
from zExceptions import NotFound

class ResourceTraverser(SimpleHandler):

    name = None

    def __init__(self, context, request=None):
        self.context = context
    
    def traverse(self, name, remaining):
        type = self.name
        
        # Note: also fixes possible unicode problems
        name = urllib.quote(name)
        
        # 1. Persistent resource directory:
        #    Try (persistent resource directory)/$type/$name
        res = queryUtility(IResourceDirectory, name=u'persistent')
        if res:
            try:
                return res[type][name]
            except (KeyError, NotFound,):
                pass # pragma: no cover
        
        # 2. Global resource directory:
        #    Try (global resource directory)/$type/$name
        res = queryUtility(IResourceDirectory, name=u'')
        if res:
            try:
                return res[type][name]
            except (KeyError, NotFound,):
                pass # pragma: no cover
        
        # 3. Packaged type-specific resource directory:
        #    Try (directory named after type + name)
        identifier = u'++%s++%s' % (type, name)
        res = queryUtility(IResourceDirectory, name=identifier)
        if res is not None:
            return res
        
        raise NotFound
