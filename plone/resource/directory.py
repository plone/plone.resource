import os.path
from zExceptions import NotFound
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from Products.Five.browser.resource import FileResourceFactory
from plone.resource.interfaces import IResourceDirectory
from plone.resource.interfaces import IFilesystemResourceDirectory


class PersistentResourceDirectory(BTreeFolder2):
    implements(IResourceDirectory)


class FilesystemResourceDirectory(object):
    implements(IFilesystemResourceDirectory, IPublishTraverse)

    def __init__(self, directory):
        self.directory = directory

    def publishTraverse(self, request, name):
        subpath = os.path.abspath(os.path.join(self.directory, name))
        if os.path.isdir(subpath):
            return FilesystemResourceDirectory(subpath)
        elif os.path.isfile(subpath):
            return FileResourceFactory(name, subpath)(request)
        
        raise NotFound

    def __getitem__(self, name):
        return self.publishTraverse(None, name)
