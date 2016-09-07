# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews import _
from brasil.gov.vlibrasnews.api import api_error_handler
from brasil.gov.vlibrasnews.api import VLibrasNews
from brasil.gov.vlibrasnews.api import VLibrasNewsError
from brasil.gov.vlibrasnews.behaviors import IVLibrasNews
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsSettings
from brasil.gov.vlibrasnews.logger import logger
from plone import api
from plone.app.textfield.interfaces import ITransformer
from Products.CMFPlone.utils import safe_unicode
from zope.component.interfaces import ComponentLookupError
from zope.globalrequest import getRequest

EMPTY = _(u'None')


# TODO: move exception handling to api_api_error_handler to get rid of this
def _get_token_from_registry():
    """Return the token from the registry and treat exceptions."""
    record = dict(interface=IVLibrasNewsSettings, name='access_token')
    try:
        value = api.portal.get_registry_record(**record)
    except api.exc.InvalidParameterError:  # error?
        logger.error(u'Missing VLibras News API authentication token record')
        return
    except ComponentLookupError:  # package not installed?
        return

    if not value:
        logger.error(u'VLibras News API authentication token is not defined')
        return

    return value


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


def get_content(context, default=EMPTY):
    """Return the content to be used in VLibras News API calls. As the
    API doesn't accept empty payload, we need to be sure all keys have
    a default value.
    """
    title = safe_unicode(context.Title()) or default
    description = safe_unicode(context.Description()) or default

    try:
        transformer = ITransformer(context)
        text = transformer(context.text, 'text/plain')
    except AttributeError:
        text = u''
    content = safe_unicode(text) or default

    return dict(title=title, description=description, content=content)


@api_error_handler
def workflow_change_handler(context, event):
    """Deal with creation or deletion of translations based on changes
    on the workflow state: if an item is published, we need to create
    a translation; if it's being removed, we need to delete the
    translation.

    :param context: the item being processsed
    :type context: Dexterity-based content type
    :param event: event rised
    :type event: subscriber event
    :returns: True on success
    :rtype: bool
    :raises brasil.gov.vlibrasnews.api.VLibrasNewsError: on error
    """
    if not IVLibrasNews.providedBy(context):
        return  # nothing to do

    token = _get_token_from_registry()
    if not token:  # package not installed, token not defined or error
        return

    vlibrasnews = VLibrasNews(token=token)

    if event.action == 'publish':
        # the object is being published, create a translation
        payload = get_content(context)
        logger.debug('Creating translation for ' + context.absolute_url())
        vlibrasnews.create(context.UID(), payload)
        context.translation_url = ''
    elif event.action in ('reject', 'retract'):
        # other actions could be an indication of unpublishing
        # check if the translation exists and delete it
        if vlibrasnews.get(context.UID()):
            logger.debug('Deleting translation for ' + context.absolute_url())
            vlibrasnews.delete(context.UID())
    else:
        return  # nothing to do

    return True


@api_error_handler
def update_content_handler(context, event):
    """Deal with updates of translations based on changes on content.

    :param context: the item being processsed
    :type context: Dexterity-based content type
    :param event: event fired
    :type event: subscriber event
    :returns: True on success
    :rtype: bool
    :raises brasil.gov.vlibrasnews.api.VLibrasNewsError: on error
    """
    if not IVLibrasNews.providedBy(context):
        return  # nothing to do

    if api.content.get_state(context) != 'published':
        return  # nothing to do; translaton doesn't exist

    token = _get_token_from_registry()
    if not token:  # package not installed, token not defined or error
        return

    vlibrasnews = VLibrasNews(token=token)
    payload = get_content(context)
    logger.debug('Updating LIBRAS translation for ' + context.absolute_url())
    vlibrasnews.update(context.UID(), payload)

    return True


# XXX: this doesn't belong here
def get_translation_url(context):
    """Get the URL of a LIBRAS translation using VLibras News API.

    :param context: the item being processsed
    :type context: Dexterity-based content type
    :raises brasil.gov.vlibrasnews.api.VLibrasNewsError: on error
    """
    if not IVLibrasNews.providedBy(context):
        return  # nothing to do

    if api.content.get_state(context) != 'published':
        return  # nothing to do; translaton doesn't exist

    token = _get_token_from_registry()
    if not token:  # package not installed, token not defined or error
        return

    vlibrasnews = VLibrasNews(token=token)
    logger.debug('Getting LIBRAS translation for ' + context.absolute_url())
    try:
        context.translation_url = vlibrasnews.get(context.UID())
    except VLibrasNewsError as e:
        api.portal.show_message(e.msg, request=getRequest(), type='error')
        logger.error(e.log)


@api_error_handler
def delete_content_handler(context, event):
    """Delete a LIBRAS translation using VLibras News API.

    :param context: item being deleted
    :type context: Dexterity-based content type
    :param event: event fired
    :type event: subscriber event
    :returns: True on success
    :rtype: bool
    :raises brasil.gov.vlibrasnews.api.VLibrasNewsError: on error
    """
    if not IVLibrasNews.providedBy(context):
        return  # nothing to do

    if not _deletion_confirmed():
        return  # don't process this event

    if api.content.get_state(context) != 'published':
        return  # nothing to do; translaton doesn't exist

    token = _get_token_from_registry()
    if not token:  # package not installed, token not defined or error
        return

    vlibrasnews = VLibrasNews(token=token)
    logger.debug('Deleting translation for ' + context.absolute_url())
    vlibrasnews.delete(context.UID())

    return True
