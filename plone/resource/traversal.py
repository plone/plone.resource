from zope.traversing.namespace import SimpleHandler


class ResourceTraverser(SimpleHandler):

    name = None

    def __init__(self, context, request=None):
        self.context = context
    
    def traverse(self, name, remaining):
        for name