from plone.resource.interfaces import IPloneResourceCreatedEvent
from plone.resource.interfaces import IPloneResourceModifiedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implementer


@implementer(IPloneResourceCreatedEvent)
class PloneResourceCreatedEvent(ObjectEvent):
    """A resource has been created"""


@implementer(IPloneResourceModifiedEvent)
class PloneResourceModifiedEvent(ObjectEvent):
    """A resource has been modified"""
