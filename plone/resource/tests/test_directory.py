# -*- coding: utf-8 -*-
import os.path
import unittest2 as unittest
from Acquisition import aq_base
from plone.resource.events import PloneResourceCreatedEvent
from plone.resource.events import PloneResourceModifiedEvent
from plone.resource.interfaces import IPloneResourceCreatedEvent
from plone.resource.interfaces import IPloneResourceModifiedEvent
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from zope.component import adapter
from zope.component import provideHandler

class TestPersistentResourceDirectory(unittest.TestCase):

    def _makeOne(self):
        root = BTreeFolder2('portal_resources')
        root._setOb('demo', BTreeFolder2('demo'))
        root.demo._setOb('foo', BTreeFolder2('foo'))

        from StringIO import StringIO
        from OFS.Image import File
        file = File('test.html', 'test.html', StringIO('asdf'))
        root.demo.foo._setOb('test.html', file)

        from plone.resource.directory import PersistentResourceDirectory
        return PersistentResourceDirectory(root)

    def _assertSameUnwrapped(self, a, b):
        self.assertTrue(aq_base(a) is aq_base(b))

    def test_ctor_implicit_context(self):
        from zope.site.testing import siteSetUp, createSiteManager, siteTearDown
        siteSetUp()

        site = BTreeFolder2('site')
        createSiteManager(site, setsite=True)
        root = self._makeOne().context
        site._setOb('portal_resources', root)

        from plone.resource.directory import PersistentResourceDirectory
        try:
            dir = PersistentResourceDirectory()
            # context should be stored unwrapped
            self.assertTrue(aq_base(root) is dir.context)

            # but re-wrapped during traversal
            traversed = dir['demo']
            self.assertTrue(site in traversed.context.aq_chain)
        finally:
            siteTearDown()

    def test_repr(self):
        dir = self._makeOne()
        s = '<PersistentResourceDirectory object at portal_resources>'
        self.assertEqual(s, repr(dir))

    def test_publishTraverse_directory(self):
        dir = self._makeOne()
        subdir = dir.publishTraverse(None, 'demo')
        self._assertSameUnwrapped(subdir.context, dir.context.demo)

    def test_publishTraverse_file(self):
        dir = self._makeOne()
        file = dir.publishTraverse(None, 'demo/foo/test.html')
        self._assertSameUnwrapped(file, dir.context.demo.foo['test.html'])

    def test_publishTraverse_not_found(self):
        dir = self._makeOne()
        from zExceptions import NotFound
        self.assertRaises(NotFound, dir.publishTraverse, None, 'baz')

    def test_getitem(self):
        dir = self._makeOne()
        self._assertSameUnwrapped(dir['demo'].context, dir.context.demo)

    def test_openFile(self):
        dir = self._makeOne()
        file = dir.openFile('demo/foo/test.html')
        self.assertEqual('asdf', file.read())

    def test_readFile(self):
        dir = self._makeOne()
        self.assertEqual('asdf', dir.readFile('demo/foo/test.html'))

    def test_readFile_not_found(self):
        dir = self._makeOne()
        self.assertRaises(IOError, dir.readFile, 'baz')

    def test_listDirectory(self):
        dir = self._makeOne()
        self.assertEqual(['demo'], dir.listDirectory())

    def test_listDirectory_filters_by_name(self):
        dir = self._makeOne()
        dir.context._setOb('.svn', BTreeFolder2('filtered'))
        self.assertEqual(['demo'], dir.listDirectory())

    def test_makeDirectory(self):
        dir = self._makeOne()
        dir.makeDirectory('demo/bar')
        newdir = dir['demo']['bar']
        self.assertTrue(isinstance(newdir.context, BTreeFolder2))

    def test_makeDirectory_extra_slashes(self):
        dir = self._makeOne()
        dir.makeDirectory('/demo/bar/')
        newdir = dir['demo']['bar']
        self.assertTrue(isinstance(newdir.context, BTreeFolder2))

    def test_writeFile(self):
        dir = self._makeOne()
        dir.writeFile('qux', 'qux')
        self.assertEqual('qux', dir.readFile('qux'))

    def test_writeFile_does_not_create_empty_directory(self):
        dir = self._makeOne()
        dir.writeFile('qux', 'qux')
        self.assertFalse('' in dir)
        self.assertTrue('qux' in dir)

    def test_writeFile_directory_missing(self):
        dir = self._makeOne()
        dir.writeFile('baz/qux', 'qux')
        self.assertEqual('qux', dir.readFile('baz/qux'))

    def test_writeFile_file_already_exists(self):
        dir = self._makeOne()
        dir.writeFile('demo/foo/test.html', 'changed')
        self.assertEqual('changed', dir.readFile('demo/foo/test.html'))

    def test_importZip(self):
        dir = self._makeOne()
        f = open(os.path.join(os.path.dirname(__file__), 'resources.zip'))
        dir.importZip(f)
        self.assertEqual('from zip', dir.readFile('demo/foo/test.html'))

    def test_importZip_takes_ZipFile(self):
        dir = self._makeOne()
        from zipfile import ZipFile
        f = ZipFile(os.path.join(os.path.dirname(__file__), 'resources.zip'))
        dir.importZip(f)
        self.assertEqual('from zip', dir.readFile('demo/foo/test.html'))

    def test_importZip_filters_resource_forks(self):
        dir = self._makeOne()
        f = open(os.path.join(os.path.dirname(__file__), 'resources.zip'))
        dir.importZip(f)
        self.assertFalse('__MACOSX' in dir.context.objectIds())

    def test_importZip_filters_hidden_directories(self):
        dir = self._makeOne()
        f = open(os.path.join(os.path.dirname(__file__), 'resources.zip'))
        dir.importZip(f)
        self.assertFalse('.svn' in dir)

    def test_delitem(self):
        dir = self._makeOne()
        dir.makeDirectory('demo')
        self.assertTrue('demo' in dir)
        del dir['demo']
        self.assertFalse('demo' in dir)

    def test_rename(self):
        dir = self._makeOne()
        dir.rename('demo', 'demo1')
        self.assertEqual(['demo1'], dir.listDirectory())

    def test_setitem_file(self):
        dir = self._makeOne()
        f = dir['demo']['foo']['test.html']
        dir['demo'].makeDirectory('bar')

        dir['demo']['bar']['test.html'] = f
        self.assertEqual(dir['demo']['foo'].readFile('test.html'),
                         dir['demo']['bar'].readFile('test.html'),)

    def test_setitem_file_unicode(self):
        dir = self._makeOne()
        f = dir['demo']['foo']['test.html']
        dir['demo'].makeDirectory('bar')

        dir['demo']['bar'][u'test.html'] = f
        self.assertEqual(dir['demo']['foo'].readFile('test.html'),
                         dir['demo']['bar'].readFile('test.html'),)

    def test_setitem_directory(self):
        dir = self._makeOne()
        dir['demo']['foo'].makeDirectory('d1')

        d1 = dir['demo']['foo']['d1']
        del dir['demo']['foo']['d1']

        dir['demo']['foo']['d2'] = d1

        self.assertEqual(dir['demo']['foo']['d2'].__name__, 'd2')

    def test_events(self):
        events = []

        @adapter(IPloneResourceCreatedEvent)
        def _handleFileCreated(event):
            events.append(event)
        provideHandler(_handleFileCreated)

        @adapter(IPloneResourceModifiedEvent)
        def _handleFileModified(event):
            events.append(event)
        provideHandler(_handleFileModified)

        dir = self._makeOne()
        dir.writeFile('test', 'my test')
        dir.writeFile('test', 'my test is modified')
        self.assertTrue(isinstance(events[0], PloneResourceCreatedEvent))
        self.assertEqual(
            str(events[0].object), 
            'my test'
        )
        self.assertTrue(isinstance(events[1], PloneResourceModifiedEvent))
        self.assertEqual(
            str(events[1].object), 
            'my test is modified'
        )


class TestFilesystemResourceDirectory(unittest.TestCase):

    def _makeOne(self):
        from plone.resource.directory import FilesystemResourceDirectory
        path = os.path.join(os.path.dirname(__file__), 'resources')
        return FilesystemResourceDirectory(path)

    def test_repr(self):
        dir = self._makeOne()
        subpath = dir.directory[dir.directory.index(dir.__name__):]
        s = '<FilesystemResourceDirectory object at %s>' % subpath
        self.assertEqual(s, repr(dir))

    def test_publishTraverse_directory(self):
        dir = self._makeOne()
        subdir = dir.publishTraverse(None, 'demo')
        self.assertEqual(subdir.directory, os.path.join(dir.directory, 'demo'))

    def test_publishTraverse_file(self):
        dir = self._makeOne()
        file = dir.publishTraverse(None, 'demo/foo/test.html')
        subpath = os.path.join(dir.directory, 'demo', 'foo', 'test.html')
        self.assertEqual(file.path, subpath)

    def test_publishTraverse_not_found(self):
        dir = self._makeOne()
        from zExceptions import NotFound
        self.assertRaises(NotFound, dir.publishTraverse, None, 'baz')

    def test_getitem(self):
        dir = self._makeOne()
        subpath = os.path.join(dir.directory, 'demo')
        self.assertEqual(dir['demo'].directory, subpath)

    def test_contains(self):
        dir = self._makeOne()
        self.assertTrue('demo' in dir)

    def test_openFile(self):
        dir = self._makeOne()
        file = dir.openFile('demo/foo/test.html')
        self.assertEqual('asdf', file.read())

    def test_readFile(self):
        dir = self._makeOne()
        self.assertEqual('asdf', dir.readFile('demo/foo/test.html'))

    def test_readFile_not_found(self):
        dir = self._makeOne()
        self.assertRaises(IOError, dir.readFile, 'baz')

    def test_listDirectory(self):
        dir = self._makeOne()
        self.assertEqual(['demo'], dir.listDirectory())

    def test_listDirectory_filters_by_name(self):
        dir = self._makeOne()
        name = '.dummy'
        file_path = os.path.join(dir.directory, name)
        if name not in os.listdir(dir.directory):
            f = open(file_path, 'w')
            f.write("")
            f.close()
        self.assertTrue(name in os.listdir(dir.directory))
        self.assertEqual(['demo'], dir.listDirectory())
        # Cleanup created file.
        os.remove(file_path)
