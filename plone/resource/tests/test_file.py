# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone.testing.zca import UNIT_TESTING

class TestFilesystemResourceDirectory(unittest.TestCase):

    layer = UNIT_TESTING

    def test_render(self):
        import os.path
        from email.utils import formatdate
        from plone.resource.file import FilesystemFile
        from zope.publisher.browser import TestRequest

        name = 'test.html'
        path = os.path.join(os.path.dirname(__file__), 'resources', 'demo', 'foo', name)
        mtime = os.path.getmtime(path)

        request = TestRequest()

        f = FilesystemFile(None, request, path, name)
        iterator = f()

        data = ''.join(iterator)
        self.assertEqual(data, 'asdf')
        self.assertEqual(request.response.getHeader('Content-Type'), 'text/html')
        self.assertEqual(request.response.getHeader('Content-Length'), '4')
        self.assertEqual(request.response.getHeader('Last-Modified'), formatdate(mtime, usegmt=True))

    def test_last_modified(self):
        import os.path
        import datetime

        from dateutil.tz import tzlocal

        from zope.component import provideAdapter
        from zope.publisher.browser import TestRequest

        from plone.resource.file import FilesystemFile
        from plone.resource.file import FileLastModified

        from z3c.caching.interfaces import ILastModified

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
        import os.path

        from zope.component import provideAdapter
        from zope.publisher.browser import TestRequest

        from plone.resource.file import FilesystemFile
        from plone.resource.file import rawReadFile

        from zope.filerepresentation.interfaces import IRawReadFile

        provideAdapter(rawReadFile)

        name = 'test.html'
        path = os.path.join(os.path.dirname(__file__), 'resources', 'demo', 'foo', name)

        request = TestRequest()

        f = FilesystemFile(None, request, path, name)

        rf = IRawReadFile(f)

        self.assertTrue(isinstance(rf, file))
        self.assertEqual(rf.read(), 'asdf')

        rf.close()
