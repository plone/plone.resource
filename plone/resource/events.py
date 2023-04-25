from plone.resource.interfaces import IPloneResourceCreatedEvent
from plone.resource.interfaces import IPloneResourceModifiedEvent
from zope.interface import implementer
from zope.interface.interfaces import ObjectEvent


@implementer(IPloneResourceCreatedEvent)
class PloneResourceCreatedEvent(ObjectEvent):
    """A resource has been created"""


@implementer(IPloneResourceModifiedEvent)
class PloneResourceModifiedEvent(ObjectEvent):
    """A resource has been modified"""
