# -*- coding: utf-8 -*-
"""Setup testing fixture.

For Plone 5 we need to install plone.app.contenttypes.
"""
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import pkg_resources


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import brasil.gov.vlibrasvideo
        self.loadZCML(package=brasil.gov.vlibrasvideo)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'brasil.gov.vlibrasvideo:default')
        portal.portal_workflow.setDefaultChain('one_state_workflow')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='brasil.gov.vlibrasvideo:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='brasil.gov.vlibrasvideo:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='brasil.gov.vlibrasvideo:Robot',
)
