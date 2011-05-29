import urllib
from zope.traversing.namespace import SimpleHandler

from plone.resource.utils import queryResourceDirectory

from zExceptions import NotFound

class ResourceTraverser(SimpleHandler):

    name = None

    def __init__(self, context, request=None):
        self.context = context
    
    def traverse(self, name, remaining):
        type = self.name
        
        # Note: also fixes possible unicode problems
        name = urllib.quote(name)
        
        res = queryResourceDirectory(type, name)
        if res is not None:
            return res
        
        raise NotFound
