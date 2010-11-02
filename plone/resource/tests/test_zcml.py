import unittest2 as unittest
from zope.component.tests import clearZCML
from zope.component.testing import tearDown

import os.path
from StringIO import StringIO
from zope.configuration.xmlconfig import xmlconfig, XMLConfig
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory


def runSnippet(snippet, package='plone.resource.tests'):
    template = """\
    <configure xmlns="http://namespaces.zope.org/zope"
               xmlns:plone="http://namespaces.plone.org/plone"
               i18n_domain="plone"
               package="%s">
    %s
    </configure>"""
    xmlconfig(StringIO(template % (package, snippet)))


class ZCMLTestCase(unittest.TestCase):
    
    def setUp(self):
        clearZCML()
        import plone.resource
        XMLConfig('meta.zcml', plone.resource)()
    
    def tearDown(self):
        tearDown()
    
    def test_everything_specified(self):
        runSnippet("""
        <plone:resourceDirectory
          name="foo"
          type="theme"
          directory="resources"
          />
        """)
        
        res = getUtility(IResourceDirectory, name='++theme++foo')
        self.assertEqual('theme', res.type)
        self.assertEqual('foo', res.name)
        self.assertTrue(res.directory.endswith(os.path.join('plone', 'resource', 'tests', 'resources')))
