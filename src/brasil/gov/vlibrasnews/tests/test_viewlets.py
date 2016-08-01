# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews.browser.vlibrasnews import VLibrasNewsViewlet
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsLayer
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsSettings
from brasil.gov.vlibrasnews.testing import INTEGRATION_TESTING
from brasil.gov.vlibrasnews.tests.vlibras_mock import vlibras_ok
from brasil.gov.vlibrasnews.tests.vlibras_mock import vlibras_processing
from httmock import HTTMock
from plone import api
from zope.interface import alsoProvides

import unittest


class ViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.portal.REQUEST, IVLibrasNewsLayer)
        api.portal.set_registry_record(
            IVLibrasNewsSettings.__identifier__ + '.vlibrasnews_token',
            u'no key')
        with HTTMock(vlibras_ok):
            with api.env.adopt_roles(['Manager']):
                self.document = api.content.create(
                    type='Document',
                    title='My Content',
                    container=self.portal)

    def viewlet(self, context=None):
        context = context or self.portal
        viewlet = VLibrasNewsViewlet(context, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_enabled_on_document(self):
        with HTTMock(vlibras_ok):
            viewlet = self.viewlet(self.document)
            self.assertTrue(viewlet.enabled)

    def test_processing(self):
        with HTTMock(vlibras_processing):
            viewlet = self.viewlet(self.document)
            self.assertFalse(viewlet.is_ready)
            self.assertEqual(viewlet.state, 'processing')

    def test_is_ready(self):
        with HTTMock(vlibras_ok):
            viewlet = self.viewlet(self.document)
            self.assertTrue(viewlet.is_ready)
            self.assertEqual(
                viewlet.youtube_url, 'https://www.youtube.com/embed/ds2gGAbPJz8')
            self.assertEqual(viewlet.state, 'ready')
