# -*- coding: utf-8 -*-
from plone.caching.interfaces import IRulesetLookup
from plone.resource.interfaces import IUniqueResourceRequest
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IRulesetLookup)
@adapter(Interface, IUniqueResourceRequest)
class UniqueResourceLookup(object):
    """Unique resource ruleset lookup.

    Returns 'plone.stableResource' for requests marked with
    IUniqueResourceRequest.
    """

    def __init__(self, published, request):
        pass

    def __call__(self):
        return 'plone.stableResource'
