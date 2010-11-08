import unittest2 as unittest
from plone.testing import zca, z2
from plone.resource.testing import DEMO_TRAVERSER_INTEGRATION_TESTING

import os.path
from zExceptions import NotFound
from zope.component import provideUtility, provideAdapter
from zope.interface import Interface
from zope.publisher.interfaces import IRequest
from zope.traversing.interfaces import ITraversable
from plone.resource.interfaces import IResourceDirectory
from plone.resource.directory import PersistentResourceDirectory
from plone.resource.directory import FilesystemResourceDirectory

base_path = os.path.dirname(__file__)
test_dir_path = os.path.join(base_path, 'resources')


class TraversalTestCase(unittest.TestCase):
    layer = DEMO_TRAVERSER_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer.get('app')
        zca.pushGlobalRegistry()
    
    def tearDown(self):
        zca.popGlobalRegistry()

    def test_traverse_packaged_type_generic_directory(self):
        dir = FilesystemResourceDirectory(test_dir_path)
        provideUtility(dir, provides=IResourceDirectory, name=u'foo')
        
        res = self.app.restrictedTraverse('++theme++foo')
        self.failUnless(res.directory.endswith('resources/theme'))
        
        from plone.resource.traversal import ResourceTraverser
        class ThingyTraverser(ResourceTraverser):
            name = 'thingy'
        provideAdapter(factory=ThingyTraverser, provides=ITraversable, adapts=(Interface, IRequest), name=u'thingy')
        self.assertRaises(NotFound, self.app.restrictedTraverse, '++thingy++foo')

    def test_traverse_packaged_type_specific_directory(self):
        dir = FilesystemResourceDirectory(test_dir_path)
        provideUtility(dir, provides=IResourceDirectory, name=u'++theme++foo')
        
        res = self.app.restrictedTraverse('++theme++foo')
        self.failUnless(res.directory.endswith('resources'))
    
    def test_traverse_global_directory(self):
        dir = FilesystemResourceDirectory(test_dir_path)
        provideUtility(dir, provides=IResourceDirectory, name=u'')
        
        res = self.app.restrictedTraverse('++theme++foo')
        self.failUnless(res.directory.endswith('resources/theme/foo'))
        
        self.assertRaises(NotFound, self.app.restrictedTraverse, '++theme++bar')
    
    def test_traverse_persistent_directory(self):
        dir = PersistentResourceDirectory('portal_resources')
        self.app._setOb('portal_resources', dir)
        dir._setOb('theme', PersistentResourceDirectory('theme'))
        dir.theme._setOb('foo', PersistentResourceDirectory('foo'))
        provideUtility(dir, provides=IResourceDirectory, name=u'persistent')
        
        res = self.app.restrictedTraverse('++theme++foo')
        self.failUnless(res.absolute_url().endswith('portal_resources/theme/foo'))

        self.assertRaises(NotFound, self.app.restrictedTraverse, '++theme++bar')

    def test_publish_resource(self):
        dir = FilesystemResourceDirectory(test_dir_path)
        provideUtility(dir, provides=IResourceDirectory, name=u'')
        
        browser = z2.Browser(self.app)
        browser.open(self.app.absolute_url() + '/++theme++foo/test.html')
        self.assertEqual('asdf', browser.contents)
