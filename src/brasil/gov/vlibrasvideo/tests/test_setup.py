# -*- coding: utf-8 -*-
from brasil.gov.vlibrasvideo.config import PROJECTNAME
from brasil.gov.vlibrasvideo.interfaces import IBrasilGov
from brasil.gov.vlibrasvideo.testing import INTEGRATION_TESTING
from plone import api
from plone.browserlayer.utils import registered_layers

import unittest


CSS = (
    '++resource++brasil.gov.vlibrasvideo/main.css',
)
JS = (
    '++resource++brasil.gov.vlibrasvideo/main.js',
)


class InstallTestCase(unittest.TestCase):

    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        self.assertIn(IBrasilGov, registered_layers())

    def test_cssregistry(self):
        resource_ids = self.portal['portal_css'].getResourceIds()
        for css in CSS:
            self.assertIn(css, resource_ids, '{0} not installed'.format(css))

    def test_jsregistry(self):
        resource_ids = self.portal['portal_javascripts'].getResourceIds()
        for js in JS:
            self.assertIn(js, resource_ids, '{0} not installed'.format(js))

    def test_version(self):
        profile = 'brasil.gov.vlibrasvideo:default'
        setup_tool = self.portal['portal_setup']
        self.assertEqual(
            setup_tool.getLastVersionForProfile(profile), (u'1',))


class UninstallTestCase(unittest.TestCase):

    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        self.assertNotIn(IBrasilGov, registered_layers())

    def test_cssregistry_removed(self):
        resource_ids = self.portal['portal_css'].getResourceIds()
        for css in CSS:
            self.assertNotIn(css, resource_ids, '{0} not installed'.format(css))

    def test_jsregistry_removed(self):
        resource_ids = self.portal['portal_javascripts'].getResourceIds()
        for js in JS:
            self.assertNotIn(js, resource_ids, '{0} not installed'.format(js))
