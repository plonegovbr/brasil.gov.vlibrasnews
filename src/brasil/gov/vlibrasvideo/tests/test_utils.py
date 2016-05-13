# -*- coding: utf-8 -*-
from brasil.gov.vlibrasvideo import utils
from brasil.gov.vlibrasvideo.config import DEFAULT_ENABLED_CONTENT_TYPES
from brasil.gov.vlibrasvideo.interfaces import IVLibrasVideoSettings
from brasil.gov.vlibrasvideo.testing import INTEGRATION_TESTING
from brasil.gov.vlibrasvideo.tests.vlibras_mock import vlibras_error
from brasil.gov.vlibrasvideo.tests.vlibras_mock import vlibras_ok
from httmock import HTTMock
from plone import api

import unittest2 as unittest


class UtilsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        api.portal.set_registry_record(
            IVLibrasVideoSettings.__identifier__ + '.vlibrasvideo_token',
            u'no key')
        with HTTMock(vlibras_ok):
            with api.env.adopt_roles(['Manager']):
                self.document = api.content.create(
                    type='Document',
                    title='My Content',
                    description='Description',
                    text='<p>Content</p>',
                    container=self.portal)

    def test_get_content(self):
        self.assertEqual(utils._get_content(self.document), 'Content')

    def test_get_state(self):
        self.assertEqual(utils._get_state(self.document), 'published')

    def test_get_registry(self):
        self.assertEqual(utils._get_registry('vlibrasvideo_token'), u'no key')
        self.assertEqual(
            utils._get_registry('enabled_content_types', []),
            DEFAULT_ENABLED_CONTENT_TYPES)

    def test_post_news_ok(self):
        with HTTMock(vlibras_ok):
            status, description = utils.post_news(self.document)
            self.assertEqual(status, 200)
            self.assertEqual(description, 'OK')

    def test_post_news_error(self):
        with HTTMock(vlibras_error):
            status, description = utils.post_news(self.document)
            self.assertEqual(status, 401)
            self.assertEqual(description, 'UNAUTHORIZED')

    def test_repost_news_ok(self):
        with HTTMock(vlibras_ok):
            status, description = utils.repost_news(self.document)
            self.assertEqual(status, 200)
            self.assertEqual(description, 'OK')

    def test_repost_news_error(self):
        with HTTMock(vlibras_error):
            status, description = utils.repost_news(self.document)
            self.assertEqual(status, 401)
            self.assertEqual(description, 'UNAUTHORIZED')

    def test_get_video_url_ok(self):
        with HTTMock(vlibras_ok):
            status, video_url = utils.get_video_url(self.document)
            self.assertEqual(status, 200)
            self.assertEqual(video_url, 'https://www.youtube.com/embed/ds2gGAbPJz8')

    def test_get_video_url_error(self):
        with HTTMock(vlibras_error):
            status, description = utils.get_video_url(self.document)
            self.assertEqual(status, 401)
            self.assertEqual(description, 'UNAUTHORIZED')

    def test_delete_video_ok(self):
        with HTTMock(vlibras_ok):
            status, description = utils.delete_video(self.document)
            self.assertEqual(status, 200)
            self.assertEqual(description, 'OK')

    def test_delete_video_error(self):
        with HTTMock(vlibras_error):
            status, description = utils.delete_video(self.document)
            self.assertEqual(status, 401)
            self.assertEqual(description, 'UNAUTHORIZED')
