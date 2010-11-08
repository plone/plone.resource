from zope.interface import Interface
from zope import schema


class IResourceDirectory(Interface):
    pass


class IFilesystemResourceDirectory(IResourceDirectory):
    directory = schema.TextLine()
