# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews import _
from brasil.gov.vlibrasnews.logger import logger
from plone import api
from requests.exceptions import RequestException
from zope.globalrequest import getRequest

import requests

CREATE_URL = 'http://150.165.204.81:3000/publish'
UPDATE_URL = 'http://150.165.204.81:3000/publish/{0}'
DELETE_URL = GET_URL = 'http://150.165.204.81:3000/videos/{0}'

CREATE_ERROR = _(u'There was an error while creating the LIBRAS translation.')
UPDATE_ERROR = _(u'There was an error while updating the LIBRAS translation.')
DELETE_ERROR = _(u'There was an error while deleting the LIBRAS translation.')
GET_ERROR = _(u'There was an error while getting the LIBRAS translation.')


class VLibrasNewsError(Exception):

    """Exception raised for errors accessing VLibras News API."""

    def __init__(self, msg, log):
        self.msg = msg  # a message to show to end users
        self.log = log  # a message to log as an error


def api_error_handler(func):
    """Decorator to deal with errors accessing VLibras News API."""

    def func_wrapper(context, event):
        try:
            return func(context, event)
        except VLibrasNewsError as e:
            api.portal.show_message(e.msg, request=getRequest(), type='error')
            logger.error(e.log)
            return False

    return func_wrapper


class VLibrasNews:

    """Make calls against the VLibras News API."""

    def __init__(self, token='', timeout=5):
        """Set token and timeout."""
        self.headers = {'Authentication-Token': token}
        self.timeout = timeout

    def _is_valid_data(self, data):
        """Check if the payload is valid for API consumption."""
        # all keys must be present
        keys = ['content', 'description', 'title'] == sorted(data.keys())
        # no values are empty
        values = all(data.values())
        return keys and values

    def create(self, id_, data):
        """Create a LIBRAS translation using VLibras News API.

        :param id_: id of the object being processed
        :type id_: str
        :param data: content payload
        :type data: dict
        :raises VLibrasNewsError: on error
        """
        assert self._is_valid_data(data)
        url, error_msg, data['id'] = CREATE_URL, CREATE_ERROR, id_
        params = dict(
            url=url, headers=self.headers, data=data, timeout=self.timeout)

        logger.debug('POST: {0}'.format(params))
        try:
            response = requests.post(**params)
        except RequestException as e:  # skip on timeouts and other errors
            raise VLibrasNewsError(error_msg, e.message)

        if response.status_code != 200:
            log = u'Status code {0} ({1})'.format(response.status_code, response.reason)
            raise VLibrasNewsError(error_msg, log)

    def update(self, id_, data):
        """Update a LIBRAS translation using VLibras News API.

        :param id_: id of the object being processed
        :type id_: str
        :param data: content payload
        :type data: dict
        :raises VLibrasNewsError: on error
        """
        assert self._is_valid_data(data)
        url, error_msg = UPDATE_URL.format(id_), UPDATE_ERROR
        params = dict(
            url=url, headers=self.headers, data=data, timeout=self.timeout)

        logger.debug('PUT: {0}'.format(params))
        try:
            response = requests.put(**params)
        except RequestException as e:  # skip on timeouts and other errors
            raise VLibrasNewsError(error_msg, e.message)

        if response.status_code != 200:  # not OK
            log = u'Status code {0} ({1})'.format(response.status_code, response.reason)
            raise VLibrasNewsError(error_msg, log)

    def delete(self, id_):
        """Delete a LIBRAS translation using VLibras News API.

        :param id_: id of the object being processed
        :type id_: str
        :raises VLibrasNewsError: on error
        """
        url, error_msg = DELETE_URL.format(id_), DELETE_ERROR
        params = dict(url=url, headers=self.headers, timeout=self.timeout)

        try:
            logger.debug('DELETE: {0}'.format(params))
            response = requests.delete(**params)
        except RequestException as e:  # skip on timeouts and other errors
            raise VLibrasNewsError(error_msg, e.message)

        if response.status_code != 200:
            log = u'Status code {0} ({1})'.format(response.status_code, response.reason)
            raise VLibrasNewsError(error_msg, log)

    def get(self, id_):
        """Get the URL of a LIBRAS translation using VLibras News API.

        :param id_: id of the object being processed
        :type id_: str
        :returns: URL of the translation, if available
        :rtype: str or None
        :raises VLibrasNewsError: on error
        """
        url, error_msg = GET_URL.format(id_), GET_ERROR
        params = dict(url=url, headers=self.headers, timeout=self.timeout)

        try:
            logger.debug('GET: {0}'.format(params))
            response = requests.get(**params)
        except RequestException as e:  # skip on timeouts and other errors
            raise VLibrasNewsError(error_msg, e.message)

        if response.status_code == 200:  # OK
            data = response.json()
            return data['url_youtube']

        if response.status_code == 102:  # Processing
            return ''

        if response.status_code == 404:  # Not Found
            return None

        log = u'Status code {0} ({1})'.format(response.status_code, response.reason)
        raise VLibrasNewsError(error_msg, log)
