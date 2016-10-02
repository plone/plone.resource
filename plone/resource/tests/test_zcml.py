# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component.testing import tearDown
from zope.configuration.exceptions import ConfigurationError

import os.path
from StringIO import StringIO
from zope.configuration.xmlconfig import xmlconfig, XMLConfig
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory


def clearZCML(test=None):
    # Copy from ``zope.component.tests.examples``
    from zope.configuration.xmlconfig import XMLConfig
    import zope.component
    from zope.component.testing import setUp
    from zope.component.testing import tearDown
    tearDown()
    setUp()
    XMLConfig('meta.zcml', zope.component)()


def runSnippet(snippet, dist='plone.resource.tests'):
    template = """\
    <configure xmlns="http://namespaces.zope.org/zope"
               xmlns:plone="http://namespaces.plone.org/plone"
               i18n_domain="plone"
               %s>
    %s
    </configure>"""
    dist = 'package="%s"' % dist if dist else ''
    xmlconfig(StringIO(template % (dist, snippet)))


class ZCMLTestCase(unittest.TestCase):

    def setUp(self):
        clearZCML()
        import plone.resource
        XMLConfig('meta.zcml', plone.resource)()

    def tearDown(self):
        tearDown()

    def test_dist_with_name_and_type(self):
        runSnippet("""
        <plone:static
          name="foo"
          type="theme"
          directory="resources"
          />
        """)

        res = getUtility(IResourceDirectory, name='++theme++foo')
        self.assertTrue(res.directory.endswith(os.path.join('plone', 'resource', 'tests', 'resources')))

    def test_dist_rejects_with_missing_type(self):
        # resource directories in distributions must be registered with a type
        self.assertRaises(ConfigurationError,
            runSnippet,
            """<plone:static
              name="foo"
              directory="resources"
              />"""
            )

    def test_dist_with_type_only(self):
        runSnippet("""
        <plone:static
          type="theme"
          directory="resources"
          />
        """)

        getUtility(IResourceDirectory, name='++theme++plone.resource.tests')

    def test_dist_rejects_absolute_directory(self):
        self.assertRaises(ConfigurationError,
            runSnippet,
            """<plone:static directory="/" />"""
            )

    def test_global(self):
        runSnippet("""
        <plone:static
          directory="/"
          />
        """, dist=None)

        res = getUtility(IResourceDirectory)
        self.assertEqual('/', res.directory)

    def test_global_rejects_relative_directory(self):
        self.assertRaises(ConfigurationError,
            runSnippet,
            """<plone:static directory="foobar" />""",
            dist=None
            )

    def test_missing_directory(self):
        self.assertRaises(ConfigurationError,
            runSnippet,
            """<plone:static directory="foobar" />"""
            )

    def test_rejects_parent_directory_traversal(self):
        self.assertRaises(ConfigurationError,
            runSnippet,
            """<plone:static directory="../tests" />"""
            )
