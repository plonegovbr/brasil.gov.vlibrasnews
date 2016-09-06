# -*- coding: utf-8 -*-
"""Setup testing fixture.

For Plone 5 we need to install plone.app.contenttypes.
"""
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing import z2
from zope.component import queryUtility


IS_PLONE_5 = api.env.plone_version().startswith('5')


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import brasil.gov.vlibrasnews
        self.loadZCML(package=brasil.gov.vlibrasnews)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'brasil.gov.vlibrasnews:default')
        self._enable_vlibras_behavior('News Item')
        portal.portal_workflow.setDefaultChain('one_state_workflow')

    def _enable_vlibras_behavior(self, portal_type):
        """Enable Vlibras Behavior for News Item."""
        fti = queryUtility(IDexterityFTI, name=portal_type)
        behavior = 'brasil.gov.vlibrasnews.behaviors.IVLibrasNews'
        if behavior in fti.behaviors:
            return
        behaviors = list(fti.behaviors)
        behaviors.append(behavior)
        fti.behaviors = tuple(behaviors)


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='brasil.gov.vlibrasnews:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='brasil.gov.vlibrasnews:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='brasil.gov.vlibrasnews:Robot',
)
