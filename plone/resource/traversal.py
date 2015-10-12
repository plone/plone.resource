# -*- coding: utf-8 -*-
from plone.resource.interfaces import IUniqueResourceRequest
from plone.resource.utils import queryResourceDirectory
from zExceptions import NotFound
from zope.interface import alsoProvides
from zope.traversing.namespace import SimpleHandler
import urllib


class ResourceTraverser(SimpleHandler):

    name = None

    def __init__(self, context, request=None):
        self.context = context

    def traverse(self, name, remaining):
        _type = self.name

        # Note: also fixes possible unicode problems
        name = urllib.quote(name)

        res = queryResourceDirectory(_type, name)
        if res is not None:
            return res

        raise NotFound


class UniqueResourceTraverser(SimpleHandler):
    """A traverser to allow unique URLs for caching"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, remaining):
        alsoProvides(self.request, IUniqueResourceRequest)
        return self.context
