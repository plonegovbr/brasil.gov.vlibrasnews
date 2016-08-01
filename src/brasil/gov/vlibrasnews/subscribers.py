# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews.config import POST_URL
from brasil.gov.vlibrasnews.config import REPOST_URL
from brasil.gov.vlibrasnews.config import REQUEST_TIMEOUT
from brasil.gov.vlibrasnews.config import VIDEO_URL
from brasil.gov.vlibrasnews.exc import NotProcessingError
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsSettings
from brasil.gov.vlibrasnews.logger import logger
from brasil.gov.vlibrasnews.tests.api_hacks import get_text_field
from plone import api
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import safe_unicode
from requests.exceptions import RequestException
from zope.component.interfaces import ComponentLookupError

import requests


def _get_registry(name, default=''):
    """Return the record of the registry and treat exceptions.
    :param name: [required] Record name
    :type name: string
    :param default: Default value
    :type default: any
    :returns: Registry record value
    :rtype: any
    """
    value = default
    try:
        value = api.portal.get_registry_record(
            IVLibrasNewsSettings.__identifier__ + '.{0}'.format(name))
    except api.exc.InvalidParameterError:
        pass
    except ComponentLookupError:
        pass
    return value


def _validate(context, token):
    """Validate if object is ready to communicate with VLibras API.
    :param context: [required] Content object
    :type context: content object
    :param token: [required] Token used to access API
    :type token: string
    :returns: true if object is ready
    :rtype: bool
    """
    # check if content type is enabled
    enabled_content_types = _get_registry('enabled_content_types', [])
    if getattr(context, 'portal_type', '') not in enabled_content_types:
        return False

    # check if object is published
    state = 'private'
    try:
        state = api.content.get_state(obj=context)
    except WorkflowException, api.exc.CannotGetPortalError:
        pass
    if state != 'published':
        return False

    # check if has token
    has_token = bool(token)
    if not has_token:
        logger.error('VLibras TOKEN must be informed in the control panel')
    return has_token


def post_news(context, event=None):
    """Create a video in vlibrasnews.
    :param context: [required] Content object
    :type context: content object
    :param event: Subscriber event
    :type event: subscriber event
    :returns: true if request is 200
    :rtype: bool
    """
    token = _get_registry('access_token')
    if not _validate(context, token):
        return False
    headers = {'Authentication-Token': token}
    payload = dict(
        id=context.UID(),
        title=safe_unicode(context.Title()),
        description=safe_unicode(context.Description()),
        content=safe_unicode(get_text_field(context)))
    params = dict(
        url=POST_URL,
        headers=headers,
        data=payload,
        timeout=REQUEST_TIMEOUT)
    logger.info('POST - {0}'.format(params))
    try:
        response = requests.post(**params)
    except RequestException as e:  # skip on timeouts and other errors
        logger.error(u'POST - {0}: {1}'.format(
            context.absolute_url(), e.message))
        return False
    if response.status_code != 200:
        logger.error(u'POST - {0}: {1} - {2}'.format(
            context.absolute_url(), response.status_code, response.reason))
        return False
    return True


def repost_news(context, event=None):
    """Update a video in vlibrasnews.
    :param context: [required] Content object
    :type context: content object
    :param event: Subscriber event
    :type event: subscriber event
    :returns: true if request is 200
    :rtype: bool
    """
    token = _get_registry('access_token')
    if not _validate(context, token):
        return False
    headers = {'Authentication-Token': token}
    payload = dict(
        title=safe_unicode(context.Title()),
        description=safe_unicode(context.Description()),
        content=safe_unicode(get_text_field(context)))
    params = dict(
        url=REPOST_URL.format(context.UID()),
        headers=headers,
        data=payload,
        timeout=REQUEST_TIMEOUT)
    logger.info('PUT - {0}'.format(params))
    try:
        response = requests.put(**params)
    except RequestException as e:  # skip on timeouts and other errors
        logger.error(u'PUT - {0}: {1}'.format(
            context.absolute_url(), e.message))
        return False
    if response.status_code != 200:
        logger.error(u'PUT - {0}: {1} - {2}'.format(
            context.absolute_url(), response.status_code, response.reason))
        return False
    return True


def get_video_url(context):
    """Get a video url from vlibrasnews.
    :param context: [required] Content object
    :type context: content object
    :returns: youtube url if available
    :rtype: string or None
    :raises:
        :class:`~brasil.gov.vlibras.exc.NotProcessingErrorError`,
    """
    token = _get_registry('access_token')
    if not _validate(context, token):
        return
    headers = {'Authentication-Token': token}
    params = dict(
        url=VIDEO_URL.format(context.UID()),
        headers=headers,
        timeout=REQUEST_TIMEOUT)
    logger.info('GET - {0}'.format(params))
    try:
        response = requests.get(**params)
    except RequestException as e:  # skip on timeouts and other errors
        logger.error(u'GET - {0}: {1}'.format(
            context.absolute_url(), e.message))
        return
    if response.status_code != 200:
        logger.error(u'GET - {0}: {1} - {2}'.format(
            context.absolute_url(), response.status_code, response.reason))
        if response.status_code != 102:
            raise NotProcessingError('Video not ready and not being processed.')
        return
    data = response.json()
    return data['url_youtube']


def delete_video(context, event=None):
    """Delete a video in vlibrasnews.
    :param context: [required] Content object
    :type context: content object
    :param event: Subscriber event
    :type event: subscriber event
    :returns: true if request is 200
    :rtype: bool
    """
    token = _get_registry('access_token')
    if not _validate(context, token):
        return False
    headers = {'Authentication-Token': token}
    params = dict(
        url=VIDEO_URL.format(context.UID()),
        headers=headers,
        timeout=REQUEST_TIMEOUT)
    logger.info('DELETE - {0}'.format(params))

    try:
        response = requests.delete(**params)
    except RequestException as e:  # skip on timeouts and other errors
        logger.error(u'DELETE - {0}: {1}'.format(
            context.absolute_url(), e.message))
        return False
    if response.status_code != 200:
        logger.error(u'DELETE - {0}: {1} - {2}'.format(
            context.absolute_url(), response.status_code, response.reason))
        return False
    return True
