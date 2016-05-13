# -*- coding: utf-8 -*-
from brasil.gov.vlibrasvideo.config import DEFAULT_ENABLED_CONTENT_TYPES
from brasil.gov.vlibrasvideo.config import PROJECTNAME
from brasil.gov.vlibrasvideo.controlpanel import IVLibrasVideoSettings
from brasil.gov.vlibrasvideo.interfaces import IBrasilGov
from brasil.gov.vlibrasvideo.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import alsoProvides

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrasilGov)
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        view = api.content.get_view(u'vlibrasvideo-settings', self.portal, self.request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@vlibrasvideo-settings')

    def test_controlpanel_installed(self):
        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertIn('vlibrasvideo', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertNotIn('vlibrasvideo', actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IVLibrasVideoSettings)

    def test_vlibrasvideo_token_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'vlibrasvideo_token'))
        self.assertEqual(self.settings.vlibrasvideo_token, '')

    def test_enabled_content_types_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'enabled_content_types'))
        self.assertEqual(self.settings.enabled_content_types, DEFAULT_ENABLED_CONTENT_TYPES)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        records = [
            IVLibrasVideoSettings.__identifier__ + '.vlibrasvideo_token',
            IVLibrasVideoSettings.__identifier__ + '.enabled_content_types'
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
