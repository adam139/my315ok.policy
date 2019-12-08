from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting,FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig

class Base(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import my315ok.policy
#         import plone.app.contenttypes
        xmlconfig.file('configure.zcml', my315ok.policy, context=configurationContext)
#         xmlconfig.file('configure.zcml', plone.app.contenttypes, context=configurationContext)
        
        # Install products that use an old-style initialize() function

    
    def tearDownZope(self, app):
        # Uninstall products installed above
        pass

        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'my315ok.policy:default')
#         applyProfile(portal, 'plone.app.contenttypes:default')

FIXTURE = Base()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="Base:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name="Base:Functional")
