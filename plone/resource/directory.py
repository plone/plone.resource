from zope.interface import implements
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from plone.resource.interfaces import IResourceDirectory
from plone.resource.interfaces import IFilesystemResourceDirectory


class PersistentResourceDirectory(BTreeFolder2):
    implements(IResourceDirectory)
    
    type = None
    name = None


class FilesystemResourceDirectory(object):
    implements(IFilesystemResourceDirectory)

    def __init__(self, type, name, directory):
        self.type = type
        self.name = name
        self.directory = directory
