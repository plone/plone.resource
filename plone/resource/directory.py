import os.path
from Acquisition import aq_base, aq_parent
from StringIO import StringIO
from zExceptions import NotFound
from zope.component import adapts
from zope.interface import implements
from zope.site.hooks import getSite
from OFS.interfaces import IObjectManager
from OFS.Image import File
from Products.Five.browser.resource import FileResourceFactory
from Products.CMFCore.utils import getToolByName
from plone.resource.interfaces import IResourceDirectory
from plone.resource.interfaces import IWritableResourceDirectory


class PersistentResourceDirectory(object):
    """A resource directory stored in the ZODB.
    
    It is assumed that directories provide IObjectManager and that files
    are instances of OFS.Image.File.
    """
    implements(IWritableResourceDirectory)
    adapts(IObjectManager)
    
    def __init__(self, context=None):
        if context is None:
            context = aq_base(getToolByName(getSite(), 'portal_resources'))
        self.context = context
    
    def publishTraverse(self, request, name):
        context = self.context
        if aq_parent(context) is None:
            site = getSite()
            if site is not None:
                context = context.__of__(site)
        
        if self.isDirectory(name):
            return self.__class__(context.restrictedTraverse(name).__of__(context))
        elif self.isFile(name):
            return context.restrictedTraverse(name).__of__(context)

        raise NotFound

    def __getitem__(self, name):
        return self.publishTraverse(None, name)

    def openFile(self, path):
        return StringIO(self.readFile(path))
    
    def readFile(self, path):
        try:
            f = self.context.restrictedTraverse(path)
        except Exception, e:
            raise IOError(str(e))
        
        return str(f.data)
    
    def listDirectory(self):
        return self.context.objectIds()
    
    def isDirectory(self, path):
        try:
            obj = self.context.restrictedTraverse(path)
        except:
            obj = None
        
        return IObjectManager.providedBy(obj)
    
    def isFile(self, path):
        try:
            obj = self.context.restrictedTraverse(path)
        except:
            obj = None
        
        return isinstance(obj, File)
    
    def exportZip(self):
        raise NotImplemented
    
    def importZip(self, zip):
        raise NotImplemented


class FilesystemResourceDirectory(object):
    """A resource directory based on files in the filesystem.
    """
    implements(IResourceDirectory)
    adapts(str)

    def __init__(self, directory):
        self.directory = directory

    def _resolveSubpath(self, path):
        parts = path.split('/')
        filepath = os.path.join(self.directory, *parts)
        return filepath

    def publishTraverse(self, request, name):
        filepath = self._resolveSubpath(name)
        if self.isDirectory(name):
            return self.__class__(filepath)
        elif self.isFile(name):
            return FileResourceFactory(name, filepath)(request)

        raise NotFound

    def __getitem__(self, name):
        return self.publishTraverse(None, name)

    def openFile(self, path):
        filepath = self._resolveSubpath(path)
        return open(filepath, 'rb')
    
    def readFile(self, path):
        return self.openFile(self, path).read()

    def listDirectory(self):
        return os.listdir(self.directory)
    
    def isDirectory(self, path):
        return os.path.isdir(self._resolveSubpath(path))
    
    def isFile(self, path):
        return os.path.isfile(self._resolveSubpath(path))
    
    def exportZip(self):
        raise NotImplemented
