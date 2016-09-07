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
        self.assertEqual(subscribers._get_token_from_registry(), 'no key')

    def test_deletion_confirmed(self):
        self.assertFalse(subscribers._deletion_confirmed())
        self.request.URL += 'delete_confirmation'
        self.request.REQUEST_METHOD = 'POST'
        self.request.form['form.submitted'] = 1
        self.assertTrue(subscribers._deletion_confirmed())

    def test_workflow_change_handler_ok(self):
        with HTTMock(vlibras_ok):
            self.assertTrue(subscribers.workflow_change_handler(self.document, Mock(action='publish')))

    def test_workflow_change_handler_error(self):
        with HTTMock(vlibras_error):
            self.assertFalse(subscribers.workflow_change_handler(self.document, Mock(action='publish')))
        with HTTMock(request_exception):
            self.assertFalse(subscribers.workflow_change_handler(self.document, Mock(action='publish')))

    def test_update_content_handler_ok(self):
        with HTTMock(vlibras_ok):
            self.assertTrue(subscribers.update_content_handler(self.document, None))

    def test_update_content_handler_error(self):
        with HTTMock(vlibras_error):
            self.assertFalse(subscribers.update_content_handler(self.document, None))
        with HTTMock(request_exception):
            self.assertFalse(subscribers.update_content_handler(self.document, None))

    def test_get_translation_url_ok(self):
        with HTTMock(vlibras_ok):
            subscribers.get_translation_url(self.document)
            self.assertEqual(self.document.translation_url, 'https://www.youtube.com/embed/ds2gGAbPJz8')

    def test_get_translation_url_processing(self):
        with HTTMock(vlibras_processing):
            subscribers.get_translation_url(self.document)
            self.assertEqual(self.document.translation_url, '')

    def test_get_translation_url_on_error(self):
        with HTTMock(vlibras_error):
            subscribers.get_translation_url(self.document)
            self.assertEqual(self.document.translation_url, '')  # no change
        with HTTMock(request_exception):
            subscribers.get_translation_url(self.document)
            self.assertEqual(self.document.translation_url, '')  # no change

    def test_delete_content_handler_ok(self):
        with HTTMock(vlibras_ok):
            self.request.URL += 'delete_confirmation'
            self.request.REQUEST_METHOD = 'POST'
            self.request.form['form.submitted'] = 1
            self.assertTrue(subscribers.delete_content_handler(self.document, Mock(action='publish')))

    def test_delete_on_unpublish(self):
        with HTTMock(vlibras_ok):
            self.assertTrue(subscribers.workflow_change_handler(self.document, Mock(action='reject')))

    def test_delete_content_handler_error(self):
        with HTTMock(vlibras_error):
            self.assertFalse(subscribers.delete_content_handler(self.document, Mock(action='publish')))
        with HTTMock(request_exception):
            self.assertFalse(subscribers.delete_content_handler(self.document, Mock(action='publish')))
