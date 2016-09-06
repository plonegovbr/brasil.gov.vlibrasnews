# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews import _
from brasil.gov.vlibrasnews.behaviors import IVLibrasNews
from brasil.gov.vlibrasnews.config import POST_URL
from brasil.gov.vlibrasnews.config import REPOST_URL
from brasil.gov.vlibrasnews.config import REQUEST_TIMEOUT
from brasil.gov.vlibrasnews.config import VIDEO_URL
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsSettings
from brasil.gov.vlibrasnews.logger import logger
from plone import api
from plone.app.textfield.interfaces import ITransformer
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import safe_unicode
from requests.exceptions import RequestException
from zope.component.interfaces import ComponentLookupError
from zope.globalrequest import getRequest

import requests

SUCCESS = _(u'The request was successfully processed.')
CREATE_ERROR = _(u'There was an error while creating the LIBRAS translation.')
UPDATE_ERROR = _(u'There was an error while updating the LIBRAS translation.')
DELETE_ERROR = _(u'There was an error while deleting the LIBRAS translation.')


class VLibrasNewsError(Exception):

    """Exception raised for errors accessing VLibras News API."""

    def __init__(self, msg, log):
        self.msg = msg  # a message to show to end users
        self.log = log  # a message to log as an error


def error_handler(func):
    """Decorator to deal with errors accessing VLibras News API."""

    def func_wrapper(context, event):
        try:
            return func(context, event)
        except VLibrasNewsError as e:
            api.portal.show_message(e.msg, request=getRequest(), type='error')
            logger.error(e.log)
            return False

    return func_wrapper


def _get_registry_record(name):
    """Return the record and treat exceptions.
    :param name: [required] Record name
    :type name: string
    :returns: Registry record value
    :rtype: any
    """
    record = dict(interface=IVLibrasNewsSettings, name=name)
    try:
        value = api.portal.get_registry_record(**record)
    except (api.exc.InvalidParameterError, ComponentLookupError):
        return

    msg = 'Using "{0}" as Access Token for VLibras News API'
    logger.info(msg.format(value))
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
    # check if context has VLibras News behavior
    if not IVLibrasNews.providedBy(context):
        logger.info('IVLibrasNews not enabled on context')
        return False

    # check if has token
    has_token = bool(token)
    if not has_token:
        logger.error('VLibras News API Access Token must be informed in the control panel')
    return has_token


def _is_published(context):
    """Check if object is published.
    :param context: [required] Content object
    :type context: content object
    :returns: True if object is published
    :rtype: bool
    """
    # check if object is published
    state = 'private'
    try:
        state = api.content.get_state(obj=context)
    except WorkflowException, api.exc.CannotGetPortalError:
        pass
    if state != 'published':
        logger.info('Context state is not "published"')
        return False
    return True


def _deletion_confirmed():
    """Check if we are in the context of a delete confirmation event.
    We need to be sure we're in the righ event to process it, as
    `IObjectRemovedEvent` is raised up to three times: the first one
    when the delete confirmation window is shown; the second when we
    select the 'Delete' button; and the last, as part of the
    redirection request to the parent container. Why? I have absolutely
    no idea. If we select 'Cancel' after the first event, then no more
    events are fired.
    :returns: True if delete event is fired after confirmation
    :rtype: bool
    """
    request = getRequest()
    is_delete_confirmation = 'delete_confirmation' in request.URL
    is_post = request.REQUEST_METHOD == 'POST'
    form_being_submitted = 'form.submitted' in request.form
    return is_delete_confirmation and is_post and form_being_submitted


def get_data(context, include_id=False):
    """Return the payload to be used in VLibras News API calls."""
    try:
        transformer = ITransformer(context)
        text = transformer(context.text, 'text/plain')
    except AttributeError:
        text = u''

    data = dict(
        title=safe_unicode(context.Title()),
        description=safe_unicode(context.Description()),
        content=safe_unicode(text),
    )

    if include_id:
        data['id'] = context.UID()

    return data


@error_handler
def create_translation(context, event):
    """Create a LIBRAS translation using VLibras News API.
    :param context: [required] Content object
    :type context: Dexterity-based content type
    :param event: event rised
    :type event: subscriber event
    :returns: True on success
    :rtype: bool
    :raises: VLibrasNewsError
    """
    # Unpublish item
    if event.action != 'publish':
        return delete_translation(context, event)

    token = _get_registry_record('access_token')
    if not _validate(context, token):
        return False

    params = dict(
        url=POST_URL,
        headers={'Authentication-Token': token},
        data=get_data(context, include_id=True),
        timeout=REQUEST_TIMEOUT,
    )

    logger.info('Creating translation for ' + context.absolute_url())
    logger.info('POST - {0}'.format(params))

    try:
        response = requests.post(**params)
    except RequestException as e:  # skip on timeouts and other errors
        raise VLibrasNewsError(CREATE_ERROR, e.message)

    if response.status_code != 200:
        log = u'Status code {0} ({1})'.format(response.status_code, response.reason)
        raise VLibrasNewsError(CREATE_ERROR, log)

    context.video_url = ''
    logger.info(SUCCESS)
    return True


@error_handler
def update_translation(context, event):
    """Update a LIBRAS translation using VLibras News API.
    :param context: item being updated
    :type context: Dexterity-based content type
    :param event: event fired
    :type event: subscriber event
    :returns: True on success
    :rtype: bool
    :raises: VLibrasNewsError
    """
    token = _get_registry_record('access_token')
    if not _validate(context, token):
        return False
    if not _is_published(context):
        return False

    params = dict(
        url=REPOST_URL.format(context.UID()),
        headers={'Authentication-Token': token},
        data=get_data(context),
        timeout=REQUEST_TIMEOUT,
    )

    logger.info('Updating translation for ' + context.absolute_url())
    logger.info('PUT - {0}'.format(params))

    try:
        response = requests.put(**params)
    except RequestException as e:  # skip on timeouts and other errors
        raise VLibrasNewsError(UPDATE_ERROR, e.message)

    if response.status_code != 200:
        log = u'Status code {0} ({1})'.format(response.status_code, response.reason)
        raise VLibrasNewsError(UPDATE_ERROR, log)

    logger.info(SUCCESS)
    return True


def get_video_url(context):
    """Get the URL of a LIBRAS translation using VLibras News API.

    :param context: item being processed
    :type context: Dexterity-based content type
    :returns: URL of the translation if available
    :rtype: string or None
    """
    token = _get_registry_record('access_token')
    if not _validate(context, token):
        return
    if not _is_published(context):
        return

    # skip old contents
    if context.video_url is None:
        return

    params = dict(
        url=VIDEO_URL.format(context.UID()),
        headers={'Authentication-Token': token},
        timeout=REQUEST_TIMEOUT,
    )
    logger.info('GET - {0}'.format(params))
    try:
        response = requests.get(**params)
    except RequestException as e:  # skip on timeouts and other errors
        logger.error(u'GET - {0}: {1}'.format(
            context.absolute_url(), e.message))
        context.video_url = None
        return
    if response.status_code == 200:
        data = response.json()
        context.video_url = data['url_youtube']
        return
    if response.status_code != 102:
        logger.error(u'GET - {0}: {1} - {2}'.format(
            context.absolute_url(), response.status_code, response.reason))
        context.video_url = None
        return
    logger.info(u'GET - {0}: {1} - {2}'.format(
        context.absolute_url(), response.status_code, response.reason))
    context.video_url = ''


@error_handler
def delete_translation(context, event):
    """Delete a LIBRAS translation using VLibras News API.

    :param context: item being deleted
    :type context: Dexterity-based content type
    :param event: event fired
    :type event: subscriber event
    :returns: True on success
    :rtype: bool
    :raises: VLibrasNewsError
    """
    token = _get_registry_record('access_token')
    if not _validate(context, token):
        return False
    is_unpublish_event = getattr(event, 'action', 'publish') != 'publish'
    if not is_unpublish_event and not _is_published(context):
        return False
    if not is_unpublish_event and not _deletion_confirmed():
        return False

    params = dict(
        url=VIDEO_URL.format(context.UID()),
        headers={'Authentication-Token': token},
        timeout=REQUEST_TIMEOUT,
    )

    logger.info('Deleting translation for ' + context.absolute_url())
    logger.info('DELETE - {0}'.format(params))

    try:
        response = requests.delete(**params)
    except RequestException as e:  # skip on timeouts and other errors
        raise VLibrasNewsError(DELETE_ERROR, e.message)

    if response.status_code != 200:
        log = u'Status code {0} ({1})'.format(response.status_code, response.reason)
        raise VLibrasNewsError(DELETE_ERROR, log)

    logger.info(SUCCESS)
    return True
