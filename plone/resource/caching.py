from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from plone.caching.interfaces import IRulesetLookup
from plone.resource.interfaces import IUniqueResourceRequest

class UniqueResourceLookup(object):
    """Unique resource ruleset lookup.

    Returns 'plone.stableResource' for requests marked with
    IUniqueResourceRequest.
    """

    implements(IRulesetLookup)
    adapts(Interface, IUniqueResourceRequest)

    def __init__(self, published, request):
        pass

    def __call__(self):
        return 'plone.stableResource'
