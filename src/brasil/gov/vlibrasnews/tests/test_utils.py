# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews import utils
from brasil.gov.vlibrasnews.config import DEFAULT_ENABLED_CONTENT_TYPES
from brasil.gov.vlibrasnews.exc import NotProcessingError
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsSettings
from brasil.gov.vlibrasnews.testing import INTEGRATION_TESTING
from brasil.gov.vlibrasnews.tests.api_hacks import set_text_field
from brasil.gov.vlibrasnews.tests.vlibras_mock import request_exception
from brasil.gov.vlibrasnews.tests.vlibras_mock import vlibras_error
from brasil.gov.vlibrasnews.tests.vlibras_mock import vlibras_ok
from brasil.gov.vlibrasnews.tests.vlibras_mock import vlibras_processing
from httmock import HTTMock
from plone import api

import unittest2 as unittest


class UtilsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        api.portal.set_registry_record(
            IVLibrasNewsSettings.__identifier__ + '.vlibrasnews_token',
            u'no key')
        with HTTMock(vlibras_ok):
            with api.env.adopt_roles(['Manager']):
                self.document = api.content.create(
                    type='Document',
                    title='My Content',
                    description='Description',
                    container=self.portal)
                set_text_field(
                    self.document, '<p>Content</p>')

    def test_get_registry(self):
        self.assertEqual(utils._get_registry('vlibrasnews_token'), u'no key')
        self.assertEqual(
            utils._get_registry('enabled_content_types', []),
            DEFAULT_ENABLED_CONTENT_TYPES)

    def test_validate(self):
        self.assertTrue(utils._validate(self.document, u'no key'))

    def test_post_news_ok(self):
        with HTTMock(vlibras_ok):
            self.assertTrue(utils.post_news(self.document))

    def test_post_news_error(self):
        with HTTMock(vlibras_error):
            self.assertFalse(utils.post_news(self.document))
        with HTTMock(request_exception):
            self.assertFalse(utils.post_news(self.document))

    def test_repost_news_ok(self):
        with HTTMock(vlibras_ok):
            self.assertTrue(utils.repost_news(self.document))

    def test_repost_news_error(self):
        with HTTMock(vlibras_error):
            self.assertFalse(utils.repost_news(self.document))
        with HTTMock(request_exception):
            self.assertFalse(utils.repost_news(self.document))

    def test_get_video_url_ok(self):
        with HTTMock(vlibras_ok):
            video_url = utils.get_video_url(self.document)
            self.assertEqual(video_url, 'https://www.youtube.com/embed/ds2gGAbPJz8')

    def test_get_video_url_error(self):
        with HTTMock(vlibras_error):
            with self.assertRaises(NotProcessingError):
                utils.get_video_url(self.document)
        with HTTMock(vlibras_processing):
            self.assertIsNone(utils.get_video_url(self.document))
        with HTTMock(request_exception):
            self.assertIsNone(utils.get_video_url(self.document))

    def test_delete_video_ok(self):
        with HTTMock(vlibras_ok):
            self.assertTrue(utils.delete_video(self.document))

    def test_delete_video_error(self):
        with HTTMock(vlibras_error):
            self.assertFalse(utils.delete_video(self.document))
        with HTTMock(request_exception):
            self.assertFalse(utils.delete_video(self.document))
