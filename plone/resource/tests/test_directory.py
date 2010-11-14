import os.path
import unittest2 as unittest
from Acquisition import aq_base
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2


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
        from plone.resource.directory import FILTERED_NAMES
        dir.context._setOb(FILTERED_NAMES[0], BTreeFolder2('filtered'))
        self.assertEqual(['demo'], dir.listDirectory())


class TestFilesystemResourceDirectory(unittest.TestCase):
    
    def _makeOne(self):
        from plone.resource.directory import FilesystemResourceDirectory
        path = os.path.join(os.path.dirname(__file__), 'resources')
        return FilesystemResourceDirectory(path)
    
    def test_repr(self):
        dir = self._makeOne()
        s = '<FilesystemResourceDirectory object at %s>' % dir.directory
        self.assertEqual(s, repr(dir))

    def test_publishTraverse_directory(self):
        dir = self._makeOne()
        subdir = dir.publishTraverse(None, 'demo')
        self.assertEqual(subdir.directory, os.path.join(dir.directory, 'demo'))
    
    def test_publishTraverse_file(self):
        dir = self._makeOne()
        file = dir.publishTraverse(None, 'demo/foo/test.html')
        subpath = os.path.join(dir.directory, 'demo', 'foo', 'test.html')
        self.assertEqual(file.context.path, subpath)
    
    def test_publishTraverse_not_found(self):
        dir = self._makeOne()
        from zExceptions import NotFound
        self.assertRaises(NotFound, dir.publishTraverse, None, 'baz')

    def test_getitem(self):
        dir = self._makeOne()
        subpath = os.path.join(dir.directory, 'demo')
        self.assertEqual(dir['demo'].directory, subpath)

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
        from plone.resource.directory import FILTERED_NAMES
        name = FILTERED_NAMES[0]
        if name not in os.listdir(dir.directory): # pragma: no cover
            f = open(os.path.join(dir.directory, name), 'w')
            f.write()
            f.close()
        self.assertTrue(name in os.listdir(dir.directory))
        self.assertEqual(['demo'], dir.listDirectory())
