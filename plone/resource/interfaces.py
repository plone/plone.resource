from zope.interface import Interface
from zope import schema


class IResourceDirectory(Interface):
    type = schema.ASCIILine()
    name = schema.ASCIILine()


class IFilesystemResourceDirectory(IResourceDirectory):
    directory = schema.TextLine()
