import unittest2 as unittest
from plone.resource.testing import PLONE_RESOURCE_INTEGRATION_TESTING
from plone.resource.interfaces import IResourceDirectory


class IntegrationTestCase(unittest.TestCase):
    layer = PLONE_RESOURCE_INTEGRATION_TESTING
    
    def setUp(self):
        self.portal = self.layer.get('portal')
    
    def test_persistent_directory_installed(self):
        # should be available as an IResourceDirectory utility named 'persistent'
        from zope.component import getUtility
        utility = getUtility(IResourceDirectory, name='persistent')
        
        # should be available as the portal_resources tool
        from Products.CMFCore.utils import getToolByName
        tool = getToolByName(self.portal, 'portal_resources')
        self.assertEqual('portal_resources', tool.getId())

        # the tool and utility are identical except for their acquisition wrappers
        from Acquisition import aq_base
        self.assertTrue(aq_base(tool) is aq_base(utility))
