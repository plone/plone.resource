# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.resource.traversal import ResourceTraverser
from plone.testing import Layer
from plone.testing import publisher
from plone.testing import zca
from plone.testing.z2 import FunctionalTesting
from plone.testing.z2 import STARTUP
from zope.configuration import xmlconfig


class DemoTraverser(Layer):
    defaultBases = (STARTUP, publisher.PUBLISHER_DIRECTIVES)

    def setUp(self):
        # Stack a new configuration context
        self['configurationContext'] = context = zca.stackConfigurationContext(
            self.get('configurationContext')
        )

        import plone.resource
        xmlconfig.file('testing.zcml', plone.resource, context=context)

    def tearDown(self):
        # Zap the stacked configuration context
        del self['configurationContext']


DEMO_TRAVERSER_FIXTURE = DemoTraverser()
DEMO_TRAVERSER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DEMO_TRAVERSER_FIXTURE,),
    name="plone.resource:DemoTraverserFunctional"
)


class PloneResource(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.resource
        xmlconfig.file(
            'configure.zcml',
            plone.resource,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'plone.resource:default')


PLONE_RESOURCE_FIXTURE = PloneResource()
PLONE_RESOURCE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_RESOURCE_FIXTURE,),
    name="plone.resource:Integration"
)


class DemoTraverser(ResourceTraverser):
    name = 'demo'
