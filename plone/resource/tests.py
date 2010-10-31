import unittest2 as unittest
from plone.app.uuid.testing import PLONE_RESOURCE_INTEGRATION_TESTING

class IntegrationTestCase(unittest.TestCase):
    layer = PLONE_RESOURCE_INTEGRATION_TESTING
    
    def test_foo(self):
        pass
