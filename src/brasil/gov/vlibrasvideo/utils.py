# -*- coding: utf-8 -*-
from brasil.gov.vlibrasvideo.config import POST_URL
from brasil.gov.vlibrasvideo.config import REPOST_URL
from brasil.gov.vlibrasvideo.config import REQUEST_TIMEOUT
from brasil.gov.vlibrasvideo.config import VIDEO_URL
from brasil.gov.vlibrasvideo.interfaces import IVLibrasVideoSettings
from brasil.gov.vlibrasvideo.logger import logger
from plone import api
from plone.app.textfield.interfaces import ITransformer
from zope.component.interfaces import ComponentLookupError

import requests


def _get_content(obj):
    """Return the content of the object.
    :param obj: [required] Content object
    :type obj: content object
    :returns: The object's content text
    :rtype: string
    """
    transformer = ITransformer(obj)
    text = getattr(obj, 'text', '')
    if text:
        text = transformer(obj.text, 'text/plain')
    return text


def _get_state(obj):
    """Return the workflot state of the object.
    :param obj: [required] Content object
    :type obj: content object
    :returns: The object's state
    :rtype: string
    """
    state = 'private'
    try:
        state = api.content.get_state(obj=obj)
    except api.exc.CannotGetPortalError:
        pass
    return state


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
            IVLibrasVideoSettings.__identifier__ + '.{0}'.format(name))
    except api.exc.InvalidParameterError:
        pass
    except ComponentLookupError:
        pass
    return value


def post_news(context, event=None):
    """Create a video in VLibrasVideo.
    :param context: [required] Content object
    :type context: content object
    :param event: Subscriber event
    :type event: subscriber event
    :returns: Status code and description
    :rtype: tuple
    """
    enabled_content_types = _get_registry('enabled_content_types', [])
    if getattr(context, 'portal_type', '') not in enabled_content_types:
        status_code = -3
        reason = u'VLIBRAS VIDEO NOT ENABLED FOR THIS CONTENT TYPE'
        logger.info(u'{0}: {1} - {2}'.format(
            context.absolute_url(), status_code, reason
        ))
        return (status_code, reason)
    token = _get_registry('vlibrasvideo_token')
    if not token:
        status_code = -2
        reason = u'NEED TO INFORM SECRET TOKEN'
        logger.info(u'{0}: {1} - {2}'.format(
            context.absolute_url(), status_code, reason
        ))
        return (status_code, reason)
    headers = {'Authentication-Token': token}
    payload = dict(
        id=context.UID(),
        title=context.Title(),
        description=context.Description(),
        content=_get_content(context)
    )
    params = dict(
        url=POST_URL,
        headers=headers,
        data=payload,
        timeout=REQUEST_TIMEOUT
    )
    logger.info('POST - {0}'.format(params))
    response = requests.post(**params)
    logger.info(u'{0}: {1} - {2}'.format(
        context.absolute_url(), response.status_code, response.reason
    ))
    return (response.status_code, response.reason)


def repost_news(context, event=None):
    """Update a video in VLibrasVideo.
    :param context: [required] Content object
    :type context: content object
    :param event: Subscriber event
    :type event: subscriber event
    :returns: Status code and description
    :rtype: tuple
    """
    enabled_content_types = _get_registry('enabled_content_types', [])
    if getattr(context, 'portal_type', '') not in enabled_content_types:
        status_code = -3
        reason = u'VLIBRAS VIDEO NOT ENABLED FOR THIS CONTENT TYPE'
        logger.info(u'{0}: {1} - {2}'.format(
            context.absolute_url(), status_code, reason
        ))
        return (status_code, reason)
    token = _get_registry('vlibrasvideo_token')
    if not token:
        status_code = -2
        reason = u'NEED TO INFORM SECRET TOKEN'
        logger.info(u'{0}: {1} - {2}'.format(
            context.absolute_url(), status_code, reason
        ))
        return (status_code, reason)
    if _get_state(context) != 'published':
        status_code = -1
        reason = u'UNPUBLISHED CONTENT'
        return (status_code, reason)
    headers = {'Authentication-Token': token}
    payload = dict(
        title=context.Title(),
        description=context.Description(),
        content=_get_content(context)
    )
    params = dict(
        url=REPOST_URL.format(context.UID()),
        headers=headers,
        data=payload,
        timeout=REQUEST_TIMEOUT
    )
    logger.info('PUT - {0}'.format(params))
    response = requests.put(**params)
    logger.info(u'{0}: {1} - {2}'.format(
        context.absolute_url(), response.status_code, response.reason
    ))
    return (response.status_code, response.reason)


def get_video_url(context):
    """Get a video url from VLibrasVideo.
    :param context: [required] Content object
    :type context: content object
    :returns: Status code and youtube url or error description
    :rtype: tuple
    """
    enabled_content_types = _get_registry('enabled_content_types', [])
    if getattr(context, 'portal_type', '') not in enabled_content_types:
        status_code = -3
        reason = u'VLIBRAS VIDEO NOT ENABLED FOR THIS CONTENT TYPE'
        logger.info(u'{0}: {1} - {2}'.format(
            context.absolute_url(), status_code, reason
        ))
        return (status_code, reason)
    token = _get_registry('vlibrasvideo_token')
    if not token:
        status_code = -2
        reason = u'NEED TO INFORM SECRET TOKEN'
        logger.info(u'{0}: {1} - {2}'.format(
            context.absolute_url(), status_code, reason
        ))
        return (status_code, reason)
    if _get_state(context) != 'published':
        status_code = -1
        reason = u'UNPUBLISHED CONTENT'
        return (status_code, reason)
    headers = {'Authentication-Token': token}
    params = dict(
        url=VIDEO_URL.format(context.UID()),
        headers=headers,
        timeout=REQUEST_TIMEOUT
    )
    logger.info('GET - {0}'.format(params))
    response = requests.get(**params)
    if response.status_code != 200:
        logger.info(u'{0}: {1} - {2}'.format(
            context.absolute_url(), response.status_code, response.reason
        ))
        return (response.status_code, response.reason)
    data = response.json()
    logger.info(u'{0}: {1} - {2}'.format(
        context.absolute_url(), response.status_code, data['url_youtube']
    ))
    return (response.status_code, data['url_youtube'])


def delete_video(context, event=None):
    """Delete a video in VLibrasVideo.
    :param context: [required] Content object
    :type context: content object
    :param event: Subscriber event
    :type event: subscriber event
    :returns: Status code and description
    :rtype: tuple
    """
    enabled_content_types = _get_registry('enabled_content_types', [])
    if getattr(context, 'portal_type', '') not in enabled_content_types:
        status_code = -3
        reason = u'VLIBRAS VIDEO NOT ENABLED FOR THIS CONTENT TYPE'
        logger.info(u'{0}: {1} - {2}'.format(
            context.absolute_url(), status_code, reason
        ))
        return (status_code, reason)
    token = _get_registry('vlibrasvideo_token')
    if not token:
        status_code = -2
        reason = u'NEED TO INFORM SECRET TOKEN'
        logger.info(u'{0}: {1} - {2}'.format(
            context.absolute_url(), status_code, reason
        ))
        return (status_code, reason)
    if _get_state(context) != 'published':
        status_code = -1
        reason = u'UNPUBLISHED CONTENT'
        return (status_code, reason)
    headers = {'Authentication-Token': token}
    params = dict(
        url=VIDEO_URL.format(context.UID()),
        headers=headers,
        timeout=REQUEST_TIMEOUT
    )
    logger.info('DELETE - {0}'.format(params))
    response = requests.delete(**params)
    logger.info(u'{0}: {1} - {2}'.format(
        context.absolute_url(), response.status_code, response.reason
    ))
    return (response.status_code, response.reason)
