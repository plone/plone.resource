# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_parent
from OFS.Image import File
from OFS.interfaces import IObjectManager
from plone.resource.events import PloneResourceCreatedEvent
from plone.resource.events import PloneResourceModifiedEvent
from plone.resource.file import FilesystemFile
from plone.resource.interfaces import IResourceDirectory
from plone.resource.interfaces import IWritableResourceDirectory
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from Products.CMFCore.utils import getToolByName
from zExceptions import Forbidden
from zExceptions import NotFound
from zope.component.hooks import getSite
from zope.event import notify
from zope.interface import implementer

import os.path
import re
import six
import zipfile


# filter dot files, Mac resource forks
FILTERS = (r'\..*', '__MACOSX')
FILTERS = [re.compile(pattern) for pattern in FILTERS]


@implementer(IWritableResourceDirectory)
class PersistentResourceDirectory(object):
    """A resource directory stored in the ZODB.

    It is assumed that directories provide IObjectManager
    and that files are instances of OFS.Image.File.
    """

    def __init__(self, context=None):
        if context is None:
            # This is also used as a local IResourceDirectory utility,
            # named u'persistent', which wraps the root folder.
            # This gets pickled, so we can't keep the acquisition chain.
            context = aq_base(getToolByName(getSite(), 'portal_resources'))
        self.context = self.__parent__ = context
        self.__name__ = context.getId()

    def __repr__(self):
        return '<%s object at %s>' % (self.__class__.__name__,
                                      '/'.join(self.context.getPhysicalPath()))

    def publishTraverse(self, request, name):
        if six.PY2 and isinstance(name, six.text_type):
            name = name.encode('utf-8')

        context = self.context
        if aq_parent(context) is None:
            # Re-supply the acquisition chain if this is the root resource
            # directory, so that security checks work.
            site = getSite()
            if site is not None:
                context = context.__of__(site)

        if self.isDirectory(name):
            return self.__class__(
                context.unrestrictedTraverse(name).__of__(context)
            )
        elif self.isFile(name):
            return context.unrestrictedTraverse(name).__of__(context)

        raise NotFound

    def __getitem__(self, name):
        return self.publishTraverse(None, name)

    def __setitem__(self, name, item):
        if six.PY2 and isinstance(name, six.text_type):
            name = name.encode('utf-8')

        if IResourceDirectory.providedBy(item):
            item = item.context
        self.context[name] = item
        item.id = item.__name__ = name

    def __delitem__(self, name):
        del self.context[name]

    def __contains__(self, name):
        return name in self.context

    def openFile(self, path):
        return six.BytesIO(self.readFile(path))

    def readFile(self, path):
        try:
            f = self.context.unrestrictedTraverse(path)
        except Exception as e:
            raise IOError(str(e))
        if isinstance(f.data, six.binary_type):
            return f.data
        return f.data.__bytes__()

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

    def rename(self, oldName, newName):
        obj = self.context[oldName]
        obj.id = obj.__name__ = newName
        self.context._delOb(oldName)
        self.context._setOb(newName, obj)

    def exportZip(self, out):
        prefix = self.__name__

        zf = zipfile.ZipFile(out, 'w')

        def write(dir, prefix, zf):
            for name in dir.listDirectory():
                relativeName = "%s/%s" % (prefix, name,)
                if dir.isDirectory(name):
                    write(dir[name], relativeName, zf)
                elif dir.isFile(name):
                    zf.writestr(relativeName, dir.readFile(name))

        write(self, prefix, zf)
        zf.close()

    def makeDirectory(self, path):
        if six.PY2:
            path = path.encode('utf-8')

        parent = self.context
        names = path.strip('/').split('/')
        for name in names:
            if name not in parent:
                f = BTreeFolder2(name)
                parent._setOb(name, f)
            parent = parent[name]

    def writeFile(self, path, data):
        if isinstance(data, six.text_type):
            data = data.encode('utf8')
        basepath = '/'.join(path.split('/')[:-1])
        if basepath:
            self.makeDirectory(basepath)
        filename = path.split('/')[-1]
        f = File(filename, filename, data)
        ct = f.getContentType()
        if ct.startswith('text/') or ct == 'application/javascript':
            # otherwise HTTPResponse.setBody assumes latin1 and mangles things
            f.content_type = ct + '; charset=utf-8'
        container = self.context.unrestrictedTraverse(basepath)
        if filename in container:
            container._delOb(filename)
            event = PloneResourceModifiedEvent
        else:
            event = PloneResourceCreatedEvent
        container._setOb(filename, f)
        obj = container._getOb(filename)
        notify(event(obj))

    def importZip(self, f):
        if not isinstance(f, zipfile.ZipFile):
            f = zipfile.ZipFile(f)
        for name in f.namelist():
            member = f.getinfo(name)
            path = member.filename.lstrip('/')

            # test each part of the path against the filters
            if any(any(filter.match(n) for filter in FILTERS)
                   for n in path.split('/')
                   ):
                continue

            if path.endswith('/'):
                self.makeDirectory(path)
            else:
                data = f.open(member).read()
                self.writeFile(path, data)


@implementer(IResourceDirectory)
class FilesystemResourceDirectory(object):
    """A resource directory based on files in the filesystem.
    """

    __allow_access_to_unprotected_subobjects__ = True

    def __init__(self, directory, name=None, parent=None):
        self.directory = directory
        self.__name__ = name
        if name is None:
            self.__name__ = os.path.basename(directory)
        self._parent = parent

    @property
    def __parent__(self):
        if self._parent is None:
            return getSite()
        return self._parent

    @__parent__.setter
    def __parent__(self, value):
        self._parent = value

    def __repr__(self):
        return '<%s object at %s>' % (self.__class__.__name__, self.__name__)

    def __bytes__(self):
        if six.PY2:
            return repr(self)
        return repr(self).encode()

    def _resolveSubpath(self, path):
        parts = path.split('/')
        filepath = os.path.abspath(os.path.join(self.directory, *parts))
        if not filepath.startswith(self.directory):
            raise Forbidden('Invalid path resource')
        return filepath

    def publishTraverse(self, request, name):
        filepath = self._resolveSubpath(name)
        if self.isDirectory(name):
            return self.__class__(filepath, parent=self)
        elif self.isFile(name):
            return FilesystemFile(self, request, filepath, name)

        raise NotFound

    def __contains__(self, name):
        if self.publishTraverse(None, name):
            return True
        return False

    def __getitem__(self, name):
        return self.publishTraverse(None, name)

    def openFile(self, path):
        filepath = self._resolveSubpath(path)
        return open(filepath, 'rb')

    def readFile(self, path):
        with self.openFile(path) as f:
            return f.read()

    def listDirectory(self):
        names = os.listdir(self.directory)
        return [n for n in names
                if not any(filter.match(n) for filter in FILTERS)]

    def isDirectory(self, path):
        return os.path.isdir(self._resolveSubpath(path))

    def isFile(self, path):
        return os.path.isfile(self._resolveSubpath(path))

    def exportZip(self, out):
        with zipfile.ZipFile(out, 'w') as zf:
            toStrip = len(self.directory.replace(os.path.sep, '/')) + 1

            for (dirpath, dirnames, filenames) in os.walk(self.directory):
                subpath = dirpath.replace(os.path.sep, '/')[toStrip:].strip('/')

                for filename in filenames:
                    path = '/'.join([subpath, filename]).strip('/')

                    if any(any(filter.match(n) for filter in FILTERS)
                           for n in path.split('/')
                           ):
                        continue

                    zf.writestr(
                        '/'.join([self.__name__, path, ]),
                        self.readFile(path),
                    )
