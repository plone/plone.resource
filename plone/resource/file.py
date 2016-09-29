# -*- coding: utf-8 -*-
from datetime import time
from dateutil.tz import tzlocal
from email.utils import formatdate
from z3c.caching.interfaces import ILastModified
from zope.component import adapter
from zope.filerepresentation.interfaces import IRawReadFile
from zope.interface import implementer
from ZPublisher.Iterators import filestream_iterator
from zope.component import queryUtility

import datetime
import mimetypes
import os
import os.path


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
        self.lastModifiedTimestamp = float(
            os.path.getmtime(path)
        ) or time.time()

    def getContentType(self, default='application/octet-stream'):
        extension = os.path.splitext(self.__name__)[1].lower()
        mtr = queryUtility('mimetypes_registry')
        mt = None
        if mtr:
            mt = mtr.lookupExtension(extension)
        if mt is None:
            mt = mimetypes.types_map.get(extension, default)
        return mt

    def __call__(self, REQUEST=None, RESPONSE=None):
        contentType = self.getContentType()
        lastModifiedHeader = formatdate(
            self.lastModifiedTimestamp,
            usegmt=True
        )

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


@implementer(ILastModified)
@adapter(FilesystemFile)
class FileLastModified(object):
    """Determine when a file was last modified, for caching purposes
    """

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return datetime.datetime.fromtimestamp(
            self.context.lastModifiedTimestamp,
            tz=tzlocal()
        )


@implementer(IRawReadFile)
@adapter(FilesystemFile)
def rawReadFile(context):
    return open(context.path, 'rb')
