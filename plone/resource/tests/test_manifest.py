# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone.testing import zca

from plone.resource.testing import DEMO_TRAVERSER_INTEGRATION_TESTING

import zipfile
import os.path

from zope.component import provideUtility

from plone.resource.interfaces import IResourceDirectory

from plone.resource.manifest import ManifestFormat
from plone.resource.manifest import getManifest
from plone.resource.manifest import extractManifestFromZipFile
from plone.resource.manifest import getAllResources
from plone.resource.manifest import getZODBResources

from plone.resource.directory import FilesystemResourceDirectory
from plone.resource.directory import PersistentResourceDirectory

from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2

base_path = os.path.dirname(__file__)
test_dir_path = os.path.join(base_path, 'resources')

TEST_FORMAT = ManifestFormat('demo', ['title', 'description', 'bar'], {'bar': 'baz'})
TEST_FORMAT_PARAMS = ManifestFormat('demo', ['title', 'description', 'bar'], {'bar': 'baz'}, ['params'])

class TestManifest(unittest.TestCase):
    layer = DEMO_TRAVERSER_INTEGRATION_TESTING

    def setUp(self):
        zca.pushGlobalRegistry()

    def tearDown(self):
        zca.popGlobalRegistry()

    def test_get_manifest(self):
        fp = open(os.path.join(test_dir_path, 'demo', 'manifest-test', 'manifest.cfg'))
        manifest = getManifest(fp, TEST_FORMAT)
        self.assertEqual(manifest['title'], 'Manifest test')
        self.assertEqual(manifest['description'], None)
        self.assertEqual(manifest['bar'], 'baz')

        fp.close()

    def test_get_manifest_params(self):
        fp = open(os.path.join(test_dir_path, 'demo', 'manifest-test', 'manifest.cfg'))
        manifest = getManifest(fp, TEST_FORMAT_PARAMS)
        self.assertEqual(manifest['title'], 'Manifest test')
        self.assertEqual(manifest['description'], None)
        self.assertEqual(manifest['bar'], 'baz')
        self.assertEqual(manifest['params'], {'alpha': 'beta', 'delta': 'theta'})

        fp.close()

    def test_get_manifest_ignores_extra(self):
        fp = open(os.path.join(test_dir_path, 'demo', 'manifest-test', 'manifest.cfg'))
        manifest = getManifest(fp, TEST_FORMAT)
        self.assertFalse('baz' in manifest)
        fp.close()

    def test_get_manifest_override_defaults(self):
        fp = open(os.path.join(test_dir_path, 'demo', 'manifest-test', 'manifest.cfg'))
        manifest = getManifest(fp, TEST_FORMAT, {'bar': 'foo', 'title': 'foo'})
        self.assertEqual(manifest['title'], 'Manifest test')
        self.assertEqual(manifest['bar'], 'foo')
        fp.close()

    def test_extract_from_zip_file(self):
        zf = zipfile.ZipFile(os.path.join(base_path, 'zipfiles', 'normal.zip'))
        resourceName, manifestDict = extractManifestFromZipFile(zf, TEST_FORMAT)

        self.assertEqual(resourceName, 'demo1')
        self.assertEqual(
                manifestDict,
                {'bar': 'baz', 'description': None, 'title': 'No top level dir'}
            )

    def test_extract_from_zip_file_override_defaults(self):
        zf = zipfile.ZipFile(os.path.join(base_path, 'zipfiles', 'normal.zip'))
        resourceName, manifestDict = extractManifestFromZipFile(zf, TEST_FORMAT,
            defaults={'bar': 'foo', 'description': 'desc'})

        self.assertEqual(resourceName, 'demo1')
        self.assertEqual(
                manifestDict,
                {'bar': 'foo', 'description': 'desc', 'title': 'No top level dir'}
            )

    def test_extract_from_zip_file_no_top_level_dir(self):
        zf = zipfile.ZipFile(os.path.join(base_path, 'zipfiles', 'no-top-level-dir.zip'))
        self.assertRaises(ValueError, extractManifestFromZipFile, zf, TEST_FORMAT)

    def test_extract_from_zip_file_multiple_top_level_dirs(self):
        zf = zipfile.ZipFile(os.path.join(base_path, 'zipfiles', 'multiple-top-level-dirs.zip'))
        self.assertRaises(ValueError, extractManifestFromZipFile, zf, TEST_FORMAT)

    def test_extract_from_zip_file_no_manifest(self):
        zf = zipfile.ZipFile(os.path.join(base_path, 'zipfiles', 'no-manifest.zip'))
        resourceName, manifestDict = extractManifestFromZipFile(zf, TEST_FORMAT)

        self.assertEqual(resourceName, 'demo1')
        self.assertEqual(manifestDict, None)

    def test_extract_from_zip_file_manifest_name_override(self):
        zf = zipfile.ZipFile(os.path.join(base_path, 'zipfiles', 'manifest-name-override.zip'))
        resourceName, manifestDict = extractManifestFromZipFile(zf, TEST_FORMAT)

        self.assertEqual(resourceName, 'demo1')
        self.assertEqual(manifestDict, None)

        resourceName, manifestDict = extractManifestFromZipFile(zf, TEST_FORMAT, manifestFilename='other-manifest.cfg')

        self.assertEqual(
                manifestDict,
                {'bar': 'baz', 'description': None, 'title': 'No top level dir'}
            )

    def test_get_all_resources(self):
        app = self.layer['app']

        foo = FilesystemResourceDirectory(os.path.join(test_dir_path, 'demo', 'foo'))
        provideUtility(foo, provides=IResourceDirectory, name=u'++demo++foo')

        manifestTest = FilesystemResourceDirectory(os.path.join(test_dir_path, 'demo', 'manifest-test'))
        provideUtility(manifestTest, provides=IResourceDirectory, name=u'++demo++manifest-test')

        root = BTreeFolder2('portal_resources')
        app._setOb('portal_resources', root)
        root._setOb('demo', BTreeFolder2('demo'))
        root['demo']._setOb('bar', BTreeFolder2('bar'))

        persistentDir = PersistentResourceDirectory(root)
        provideUtility(persistentDir, provides=IResourceDirectory, name=u'persistent')

        resources = getAllResources(TEST_FORMAT)

        self.assertEqual(
                resources,
                {'bar': None,
                 'foo': None,
                 'manifest-test': {'bar': 'baz',
                                   'description': None,
                                   'title': 'Manifest test'}}
            )

    def test_get_all_resources_filter(self):
        app = self.layer['app']

        foo = FilesystemResourceDirectory(os.path.join(test_dir_path, 'demo', 'foo'))
        provideUtility(foo, provides=IResourceDirectory, name=u'++demo++foo')

        manifestTest = FilesystemResourceDirectory(os.path.join(test_dir_path, 'demo', 'manifest-test'))
        provideUtility(manifestTest, provides=IResourceDirectory, name=u'++demo++manifest-test')

        root = BTreeFolder2('portal_resources')
        app._setOb('portal_resources', root)
        root._setOb('demo', BTreeFolder2('demo'))
        root['demo']._setOb('bar', BTreeFolder2('bar'))

        persistentDir = PersistentResourceDirectory(root)
        provideUtility(persistentDir, provides=IResourceDirectory, name=u'persistent')

        resources = getAllResources(TEST_FORMAT, filter=lambda dir: dir.__name__ != 'foo')

        self.assertEqual(
                resources,
                {'bar': None,
                 'manifest-test': {'bar': 'baz',
                                   'description': None,
                                   'title': 'Manifest test'}}
            )

    def test_get_zodb_resources(self):
        app = self.layer['app']

        foo = FilesystemResourceDirectory(os.path.join(test_dir_path, 'demo', 'foo'))
        provideUtility(foo, provides=IResourceDirectory, name=u'++demo++foo')

        manifestTest = FilesystemResourceDirectory(os.path.join(test_dir_path, 'demo', 'manifest-test'))
        provideUtility(manifestTest, provides=IResourceDirectory, name=u'++demo++manifest-test')

        root = BTreeFolder2('portal_resources')
        app._setOb('portal_resources', root)
        root._setOb('demo', BTreeFolder2('demo'))
        root['demo']._setOb('bar', BTreeFolder2('bar'))
        root['demo']._setOb('baz', BTreeFolder2('baz'))

        persistentDir = PersistentResourceDirectory(root)
        provideUtility(persistentDir, provides=IResourceDirectory, name=u'persistent')

        resources = getZODBResources(TEST_FORMAT)

        self.assertEqual(
                resources,
                {'bar': None,
                 'baz': None}
            )

    def test_get_zodb_resources_filter(self):
        app = self.layer['app']

        foo = FilesystemResourceDirectory(os.path.join(test_dir_path, 'demo', 'foo'))
        provideUtility(foo, provides=IResourceDirectory, name=u'++demo++foo')

        manifestTest = FilesystemResourceDirectory(os.path.join(test_dir_path, 'demo', 'manifest-test'))
        provideUtility(manifestTest, provides=IResourceDirectory, name=u'++demo++manifest-test')

        root = BTreeFolder2('portal_resources')
        app._setOb('portal_resources', root)
        root._setOb('demo', BTreeFolder2('demo'))
        root['demo']._setOb('bar', BTreeFolder2('bar'))
        root['demo']._setOb('baz', BTreeFolder2('baz'))

        persistentDir = PersistentResourceDirectory(root)
        provideUtility(persistentDir, provides=IResourceDirectory, name=u'persistent')

        resources = getZODBResources(TEST_FORMAT, filter=lambda dir: dir.__name__ != 'baz')

        self.assertEqual(
                resources,
                {'bar': None}
            )
