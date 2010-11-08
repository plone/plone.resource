import unittest2 as unittest
from zope.component.tests import clearZCML
from zope.component.testing import tearDown
from zope.configuration.exceptions import ConfigurationError

import os.path
from StringIO import StringIO
from zope.configuration.xmlconfig import xmlconfig, XMLConfig
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory


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
        <plone:resourceDirectory
          name="foo"
          type="theme"
          directory="resources"
          />
        """)
        
        res = getUtility(IResourceDirectory, name='++theme++foo')
        self.assertTrue(res.directory.endswith(os.path.join('plone', 'resource', 'tests', 'resources')))
    
    def test_dist_with_name_only(self):
        runSnippet("""
        <plone:resourceDirectory
          name="foo"
          directory="resources"
          />
        """)

        getUtility(IResourceDirectory, name='foo')
    
    def test_dist_with_type_only(self):
        runSnippet("""
        <plone:resourceDirectory
          type="theme"
          directory="resources"
          />
        """)

        getUtility(IResourceDirectory, name='++theme++plone.resource.tests')

    def test_dist_without_name_or_type(self):
        runSnippet("""
        <plone:resourceDirectory
          directory="resources"
          />
        """)

        getUtility(IResourceDirectory, name='plone.resource.tests')

    def test_dist_rejects_absolute_directory(self):
        self.assertRaises(ConfigurationError,
            runSnippet,
            """<plone:resourceDirectory directory="/" />"""
            )

    def test_global(self):
        runSnippet("""
        <plone:resourceDirectory
          directory="/"
          />
        """, dist=None)
        
        res = getUtility(IResourceDirectory)
        self.assertEqual('/', res.directory)

    def test_global_rejects_relative_directory(self):
        self.assertRaises(ConfigurationError,
            runSnippet,
            """<plone:resourceDirectory directory="foobar" />""",
            dist=None
            )

    def test_missing_directory(self):
        self.assertRaises(ConfigurationError,
            runSnippet,
            """<plone:resourceDirectory directory="foobar" />"""
            )

    def test_rejects_parent_directory_traversal(self):
        self.assertRaises(ConfigurationError,
            runSnippet,
            """<plone:resourceDirectory directory="../tests" />"""
            )
