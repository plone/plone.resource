# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone.resource.testing import PLONE_RESOURCE_INTEGRATION_TESTING
from plone.resource.interfaces import IResourceDirectory


class IntegrationTestCase(unittest.TestCase):
    layer = PLONE_RESOURCE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer.get('portal')

    def test_persistent_directory_installed(self):
        # directory should be available as the portal_resources tool
        from Products.CMFCore.utils import getToolByName
        tool = getToolByName(self.portal, 'portal_resources')
        self.assertEqual('portal_resources', tool.getId())

        # wrapper should be available as an IResourceDirectory utility named 'persistent'
        from zope.component import getUtility
        utility = getUtility(IResourceDirectory, name='persistent')

        # the utility's context attribute is the (unwrapped) tool
        from Acquisition import aq_base
        self.assertTrue(aq_base(tool) is utility.context)
