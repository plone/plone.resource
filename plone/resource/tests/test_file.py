# -*- coding: utf-8 -*-
from dateutil.tz import tzlocal
from email.utils import formatdate
from plone.resource.file import FileLastModified
from plone.resource.file import FilesystemFile
from plone.resource.file import rawReadFile
from plone.testing.zca import UNIT_TESTING
from z3c.caching.interfaces import ILastModified
from zope.component import provideAdapter
from zope.filerepresentation.interfaces import IRawReadFile
from zope.publisher.browser import TestRequest

import datetime
import io
import os.path
import six
import unittest


class TestFilesystemResourceDirectory(unittest.TestCase):

    layer = UNIT_TESTING

    def test_render(self):
        name = 'test.html'
        path = os.path.join(os.path.dirname(__file__), 'resources', 'demo', 'foo', name)
        mtime = os.path.getmtime(path)

        request = TestRequest()

        f = FilesystemFile(None, request, path, name)
        iterator = f()

        data = b''.join(iterator)
        self.assertEqual(data, b'asdf')
        self.assertEqual(request.response.getHeader('Content-Type'), 'text/html')
        self.assertEqual(request.response.getHeader('Content-Length'), '4')
        self.assertEqual(request.response.getHeader('Last-Modified'), formatdate(mtime, usegmt=True))

    def test_last_modified(self):
        provideAdapter(FileLastModified)

        name = 'test.html'
        path = os.path.join(os.path.dirname(__file__), 'resources', 'demo', 'foo', name)
        mtime = os.path.getmtime(path)

        request = TestRequest()

        f = FilesystemFile(None, request, path, name)

        lastModified = ILastModified(f)
        mdate = datetime.datetime.fromtimestamp(mtime, tz=tzlocal())

        self.assertEqual(lastModified(), mdate)

    def test_raw_read_file(self):
        provideAdapter(rawReadFile)

        name = 'test.html'
        path = os.path.join(os.path.dirname(__file__), 'resources', 'demo', 'foo', name)

        request = TestRequest()

        f = FilesystemFile(None, request, path, name)

        rf = IRawReadFile(f)

        if six.PY2:
            self.assertTrue(isinstance(rf, file))
        else:
            self.assertTrue(isinstance(rf, io.IOBase))
        self.assertEqual(rf.read(), b'asdf')

        rf.close()
