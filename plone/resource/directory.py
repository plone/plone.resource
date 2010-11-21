import re
import os.path
import zipfile
from Acquisition import aq_base, aq_parent
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
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

# filter dot files, Mac resource forks
FILTERS = (r'\..*', '__MACOSX')
FILTERS = [re.compile(pattern) for pattern in FILTERS]


class PersistentResourceDirectory(object):
    """A resource directory stored in the ZODB.
    
    It is assumed that directories provide IObjectManager and that files
    are instances of OFS.Image.File.
    """
    implements(IWritableResourceDirectory)
    adapts(IObjectManager)
    
    def __init__(self, context=None):
        if context is None:
            # This is also used as a local IResourceDirectory utility,
            # named u'persistent', which wraps the root folder.
            # This gets pickled, so we can't keep the acquisition chain.
            context = aq_base(getToolByName(getSite(), 'portal_resources'))
        self.context = context
        self.__name__ = context.getId()
    
    def __repr__(self):
        return '<%s object at %s>' % (self.__class__.__name__,
                                      '/'.join(self.context.getPhysicalPath()))
    
    def publishTraverse(self, request, name):
        if isinstance(name, unicode):
            name = name.encode('utf-8')
        
        context = self.context
        if aq_parent(context) is None:
            # Re-supply the acquisition chain if this is the root resource
            # directory, so that security checks work.
            site = getSite()
            if site is not None:
                context = context.__of__(site)
        
        if self.isDirectory(name):
            return self.__class__(context.unrestrictedTraverse(name).__of__(context))
        elif self.isFile(name):
            return context.unrestrictedTraverse(name).__of__(context)

        raise NotFound

    def __getitem__(self, name):
        return self.publishTraverse(None, name)
    
    def __delitem__(self, name):
        del self.context[name]
    
    def __contains__(self, name):
        return name in self.context
    
    def openFile(self, path):
        return StringIO(self.readFile(path))
    
    def readFile(self, path):
        try:
            f = self.context.unrestrictedTraverse(path)
        except Exception, e:
            raise IOError(str(e))
        
        return str(f.data)
    
    def listDirectory(self):
        return [n for n in self.context.objectIds()
                  if not any(filter.match(n) for filter in FILTERS)]
    
    def isDirectory(self, path):
        try:
            obj = self.context.unrestrictedTraverse(path)
        except:
            obj = None
        
        return IObjectManager.providedBy(obj)
    
    def isFile(self, path):
        try:
            obj = self.context.unrestrictedTraverse(path)
        except:
            obj = None
        
        return isinstance(obj, File)
    
    def exportZip(self):
        raise NotImplemented
    
    def makeDirectory(self, path):
        parent = self.context
        names = path.strip('/').split('/')
        for name in names:
            if name not in parent:
                if isinstance(name, unicode):
                    name = name.encode('utf-8')
                f = BTreeFolder2(name)
                parent._setOb(name, f)
            parent = parent[name]
    
    def writeFile(self, path, data):
        basepath = os.path.dirname(path)
        self.makeDirectory(basepath)
        filename = path.split('/')[-1]
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        f = File(filename, filename, data)
        container = self.context.unrestrictedTraverse(basepath)
        if filename in container:
            container._delOb(filename)
        container._setOb(filename, f)
    
    def importZip(self, f):
        if not isinstance(f, zipfile.ZipFile):
            f = zipfile.ZipFile(f)
        for name in f.namelist():
            member = f.getinfo(name)
            path = member.filename.lstrip('/')
            
            # test each part of the path against the filters
            if any(any(filter.match(n) for filter in FILTERS)
                   for n in path.split('/')):
                continue

            if path.endswith('/'):
                self.makeDirectory(path)
            else:
                data = f.open(member).read()
                self.writeFile(path, data)


class FilesystemResourceDirectory(object):
    """A resource directory based on files in the filesystem.
    """
    implements(IResourceDirectory)
    adapts(str)

    def __init__(self, directory, name=None):
        self.directory = directory
        self.__name__ = name or os.path.basename(directory)

    def __repr__(self):
        return '<%s object at %s>' % (self.__class__.__name__, self.directory)

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
        return self.openFile(path).read()

    def listDirectory(self):
        names = os.listdir(self.directory)
        return [n for n in names
                  if not any(filter.match(n) for filter in FILTERS)]
    
    def isDirectory(self, path):
        return os.path.isdir(self._resolveSubpath(path))
    
    def isFile(self, path):
        return os.path.isfile(self._resolveSubpath(path))
    
    def exportZip(self):
        raise NotImplemented
