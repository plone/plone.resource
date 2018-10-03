# -*- coding: utf-8 -*-
from io import BytesIO
from OFS.Image import File
from plone.resource.directory import FilesystemResourceDirectory
from plone.resource.directory import PersistentResourceDirectory
from plone.resource.interfaces import IResourceDirectory
from plone.resource.testing import DEMO_TRAVERSER_FUNCTIONAL_TESTING
from plone.testing import zca
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from zope.component import provideUtility

import os.path
import unittest
import zipfile


base_path = os.path.dirname(__file__)
test_dir_path = os.path.join(base_path, 'resources')


class ZipDownloadTestCase(unittest.TestCase):
    layer = DEMO_TRAVERSER_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer.get('app')
        zca.pushGlobalRegistry()

    def tearDown(self):
        zca.popGlobalRegistry()

    def test_traverse_packaged_type_specific_directory(self):
        dir = FilesystemResourceDirectory(os.path.join(test_dir_path, 'demo', 'foo'))
        provideUtility(dir, provides=IResourceDirectory, name=u'++demo++foo')

        out = BytesIO()
        request = self.layer['request']
        response = request.response
        response.stdout = out

        zipview = self.app.unrestrictedTraverse('++demo++foo/@@download-zip')
        zipview()

        zf = zipfile.ZipFile(out)

        self.assertTrue('foo/test.html' in zf.namelist())
        self.assertEqual(b'asdf', zf.open('foo/test.html').read())

    def test_traverse_global_directory(self):
        dir = FilesystemResourceDirectory(test_dir_path)
        provideUtility(dir, provides=IResourceDirectory, name=u'')

        out = BytesIO()
        request = self.layer['request']
        response = request.response
        response.stdout = out

        zipview = self.app.unrestrictedTraverse('++demo++foo/@@download-zip')
        zipview()

        zf = zipfile.ZipFile(out)

        self.assertTrue('foo/test.html' in zf.namelist())
        self.assertEqual(b'asdf', zf.open('foo/test.html').read())

    def test_traverse_persistent_directory(self):
        root = BTreeFolder2('portal_resources')
        self.app._setOb('portal_resources', root)
        root._setOb('demo', BTreeFolder2('demo'))
        root['demo']._setOb('foo', BTreeFolder2('foo'))
        root['demo']['foo']._setOb(
            'test.html',
            File('test.html', 'test.html', b'asdf'),
        )

        dir = PersistentResourceDirectory(root)
        provideUtility(dir, provides=IResourceDirectory, name=u'persistent')

        out = BytesIO()
        request = self.layer['request']
        response = request.response
        response.stdout = out

        zipview = self.app.unrestrictedTraverse('++demo++foo/@@download-zip')
        zipview()

        zf = zipfile.ZipFile(out)

        self.assertTrue('foo/test.html' in zf.namelist())
        self.assertEqual(b'asdf', zf.open('foo/test.html').read())
