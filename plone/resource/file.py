import os
import os.path
import datetime
import mimetypes
from dateutil.tz import tzlocal

from datetime import time
from email.utils import formatdate

from zope.component import adapts
from zope.component import adapter

from zope.interface import implementer
from zope.interface import implements

from z3c.caching.interfaces import ILastModified

from zope.filerepresentation.interfaces import IRawReadFile

from ZPublisher.Iterators import filestream_iterator

class ResourceIterator(filestream_iterator):
    """Resource iterator that allows (inefficient) coercion to str/unicode.

    This is needed for ResourceRegistries support, for example.
    """

    def __str__(self):
        return self.read()

    def __unicode__(self):
        return self.read().decode('utf-8')

class FilesystemFile(object):
    """Representation of a file. When called, it will set response headers
    and return the file's contents
    """

    def __init__(self, parent, request, path, name):
        self.path = path
        self.request = request
        self.__name__ = name
        self.__parent__ = parent

        self.lastModifiedTimestamp = float(os.path.getmtime(path)) or time.time()

    def getContentType(self, default='application/octet-stream'):
        extension = os.path.splitext(self.__name__)[1].lower()
        return mimetypes.types_map.get(extension, default)

    def __call__(self, REQUEST=None, RESPONSE=None):

        contentType = self.getContentType()
        lastModifiedHeader = formatdate(self.lastModifiedTimestamp, usegmt=True)

        request = REQUEST
        if request is None:
            request = self.request

        response = RESPONSE
        if response is None:
            response = self.request.response

        response.setHeader('Content-Type', contentType)
        response.setHeader('Content-Length', os.path.getsize(self.path))
        response.setHeader('Last-Modified', lastModifiedHeader)

        return ResourceIterator(self.path, 'rb')

class FileLastModified(object):
    """Determine when a file was last modified, for caching purposes
    """
    implements(ILastModified)
    adapts(FilesystemFile)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return datetime.datetime.fromtimestamp(self.context.lastModifiedTimestamp, tz=tzlocal())

@implementer(IRawReadFile)
@adapter(FilesystemFile)
def rawReadFile(context):
    return open(context.path, 'rb')
