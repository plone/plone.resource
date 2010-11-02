from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class PloneResource(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.resource
        xmlconfig.file('configure.zcml', plone.resource, context=configurationContext)
    
    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'plone.resource:default')

        from transaction import commit
        commit()
    
PLONE_RESOURCE_FIXTURE = PloneResource()
PLONE_RESOURCE_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(PLONE_RESOURCE_FIXTURE,), name="plone.resource:Integration")
