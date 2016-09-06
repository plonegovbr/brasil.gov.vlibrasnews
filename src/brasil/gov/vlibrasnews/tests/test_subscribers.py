# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews import subscribers
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsSettings
from brasil.gov.vlibrasnews.testing import INTEGRATION_TESTING
from brasil.gov.vlibrasnews.tests.vlibras_mock import request_exception
from brasil.gov.vlibrasnews.tests.vlibras_mock import vlibras_error
from brasil.gov.vlibrasnews.tests.vlibras_mock import vlibras_ok
from brasil.gov.vlibrasnews.tests.vlibras_mock import vlibras_processing
from httmock import HTTMock
from mock import Mock
from plone import api
from plone.app.textfield.value import RichTextValue

import unittest


class SubscribersTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        record = IVLibrasNewsSettings.__identifier__ + '.access_token'
        api.portal.set_registry_record(record, 'no key')
        text = RichTextValue('<p>Content</p>', 'text/html', 'text/html')
        with HTTMock(vlibras_ok):
            with api.env.adopt_roles(['Manager']):
                self.document = api.content.create(
                    container=self.portal,
                    type='News Item',
                    title='My Content',
                    description='Description',
                    text=text,
                )

    def test_get_registry_record(self):
        self.assertEqual(subscribers._get_registry_record('access_token'), 'no key')

    def test_validate(self):
        self.assertTrue(subscribers._validate(self.document, 'no key'))

    def test_is_published(self):
        self.assertTrue(subscribers._is_published(self.document))

    def test_deletion_confirmed(self):
        self.assertFalse(subscribers._deletion_confirmed())
        self.request.URL += 'delete_confirmation'
        self.request.REQUEST_METHOD = 'POST'
        self.request.form['form.submitted'] = 1
        self.assertTrue(subscribers._deletion_confirmed())

    def test_create_translation_ok(self):
        with HTTMock(vlibras_ok):
            self.assertTrue(subscribers.create_translation(self.document, Mock(action='publish')))

    def test_create_translation_error(self):
        with HTTMock(vlibras_error):
            self.assertFalse(subscribers.create_translation(self.document, Mock(action='publish')))
        with HTTMock(request_exception):
            self.assertFalse(subscribers.create_translation(self.document, Mock(action='publish')))

    def test_update_translation_ok(self):
        with HTTMock(vlibras_ok):
            self.assertTrue(subscribers.update_translation(self.document, None))

    def test_update_translation_error(self):
        with HTTMock(vlibras_error):
            self.assertFalse(subscribers.update_translation(self.document, None))
        with HTTMock(request_exception):
            self.assertFalse(subscribers.update_translation(self.document, None))

    def test_get_video_url_ok(self):
        with HTTMock(vlibras_ok):
            subscribers.get_video_url(self.document)
            self.assertEqual(self.document.video_url, 'https://www.youtube.com/embed/ds2gGAbPJz8')

    def test_get_video_url_processing(self):
        with HTTMock(vlibras_processing):
            subscribers.get_video_url(self.document)
            self.assertEqual(self.document.video_url, '')

    def test_get_video_url_error(self):
        with HTTMock(vlibras_error):
            subscribers.get_video_url(self.document)
            self.assertIsNone(self.document.video_url)
        with HTTMock(request_exception):
            subscribers.get_video_url(self.document)
            self.assertIsNone(self.document.video_url)

    def test_delete_translation_ok(self):
        with HTTMock(vlibras_ok):
            self.request.URL += 'delete_confirmation'
            self.request.REQUEST_METHOD = 'POST'
            self.request.form['form.submitted'] = 1
            self.assertTrue(subscribers.delete_translation(self.document, Mock(action='publish')))

    def test_delete_on_unpublish(self):
        with HTTMock(vlibras_ok):
            self.assertTrue(subscribers.create_translation(self.document, Mock(action='reject')))

    def test_delete_translation_error(self):
        with HTTMock(vlibras_error):
            self.assertFalse(subscribers.delete_translation(self.document, Mock(action='publish')))
        with HTTMock(request_exception):
            self.assertFalse(subscribers.delete_translation(self.document, Mock(action='publish')))
