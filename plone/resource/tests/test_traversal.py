from plone.resource.directory import FilesystemResourceDirectory
from plone.resource.directory import PersistentResourceDirectory
from plone.resource.file import FilesystemFile
from plone.resource.interfaces import IResourceDirectory
from plone.resource.interfaces import IUniqueResourceRequest
from plone.resource.testing import DEMO_TRAVERSER_FUNCTIONAL_TESTING
from plone.testing import zca
from plone.testing import zope
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from zExceptions import Forbidden
from zExceptions import NotFound
from zope.component import provideUtility

import os.path
import unittest


base_path = os.path.dirname(__file__)
test_dir_path = os.path.join(base_path, "resources")


class TraversalTestCase(unittest.TestCase):
    layer = DEMO_TRAVERSER_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer.get("app")
        zca.pushGlobalRegistry()

    def tearDown(self):
        zca.popGlobalRegistry()

    def test_traverse_packaged_type_specific_directory(self):
        dire = FilesystemResourceDirectory(test_dir_path)
        provideUtility(dire, provides=IResourceDirectory, name="++demo++foo")

        res = self.app.restrictedTraverse("++demo++foo")
        self.assertTrue(res.directory.endswith("resources"))

        self.assertRaises(
            NotFound,
            self.app.restrictedTraverse,
            "++demo++asdf",
        )

    def test_traverse_packaged_type_specific_file(self):
        dire = FilesystemResourceDirectory(os.path.join(test_dir_path, "demo", "foo"))
        provideUtility(dire, provides=IResourceDirectory, name="++demo++foo")

        res = self.app.restrictedTraverse("++demo++foo/test.html")
        self.assertTrue(isinstance(res, FilesystemFile))

    def test_traverse_global_directory(self):
        dire = FilesystemResourceDirectory(test_dir_path)
        provideUtility(dire, provides=IResourceDirectory, name="")

        res = self.app.restrictedTraverse("++demo++foo")
        self.assertTrue(res.directory.endswith("resources/demo/foo"))

        self.assertRaises(NotFound, self.app.restrictedTraverse, "++demo++bar")

    def test_traverse_persistent_directory(self):
        root = BTreeFolder2("portal_resources")
        self.app._setOb("portal_resources", root)
        root._setOb("demo", BTreeFolder2("demo"))
        root.demo._setOb("foo", BTreeFolder2("foo"))

        dire = PersistentResourceDirectory(root)
        provideUtility(dire, provides=IResourceDirectory, name="persistent")

        res = self.app.restrictedTraverse("++demo++foo")
        self.assertEqual(
            "portal_resources/demo/foo",
            "/".join(
                res.context.getPhysicalPath(),
            ),
        )

        self.assertRaises(NotFound, self.app.restrictedTraverse, "++demo++bar")

    def test_publish_resource(self):
        dire = FilesystemResourceDirectory(test_dir_path)
        provideUtility(dire, provides=IResourceDirectory, name="")

        browser = zope.Browser(self.app)
        browser.handleErrors = False

        browser.open(self.app.absolute_url() + "/++demo++foo/test.html")
        self.assertEqual("asdf", browser.contents)

    def test_traverse_unique_resource_marks_request(self):
        dire = FilesystemResourceDirectory(test_dir_path)
        provideUtility(dire, provides=IResourceDirectory, name="")

        self.app.restrictedTraverse("++demo++foo/++unique++bar/test.html")
        self.assertTrue(IUniqueResourceRequest.providedBy(self.app.REQUEST))

    def test_publish_unique_resource(self):
        dire = FilesystemResourceDirectory(test_dir_path)
        provideUtility(dire, provides=IResourceDirectory, name="")

        browser = zope.Browser(self.app)
        browser.handleErrors = False

        browser.open(self.app.absolute_url() + "/++demo++foo/++unique++bar/test.html")
        self.assertEqual("asdf", browser.contents)

    def test_forbidden_resource_path_traversal(self):
        resource_directory = FilesystemResourceDirectory(test_dir_path)
        self.assertRaises(
            Forbidden, resource_directory._resolveSubpath, "../../../../setup.py"
        )
