# -*- coding: utf-8 -*-
"""Viewlets used on the package."""
from brasil.gov.vlibrasvideo.config import TTL
from brasil.gov.vlibrasvideo.interfaces import IVLibrasVideoSettings
from brasil.gov.vlibrasvideo.utils import _get_state
from brasil.gov.vlibrasvideo.utils import get_video_url
from brasil.gov.vlibrasvideo.utils import post_news
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from time import time


class VLibrasVideoViewlet(ViewletBase):

    """Viewlet with VLibrasVideo button."""

    def _is_ready(self):
        """Return True if content is ready.
        :param self: [required] Instance object
        :type self: instance object
        :returns: True if content is ready
        :rtype: boolean
        """
        self.status, self.video_url = get_video_url(self.context)
        if self.status == 200:
            return True
        elif self.status != 102 and _get_state(self.context) == 'published':
            post_news(self.context)
        return False

    @ram.cache(lambda *args: (time() // TTL))
    def is_ready(self):
        """Return True if content is ready (cached).
        :param self: [required] Instance object
        :type self: instance object
        :returns: True if content is ready
        :rtype: boolean
        """
        return self._is_ready()

    def youtube_url(self):
        """Return The video URL.
        :param self: [required] Instance object
        :type self: instance object
        :returns: The video URL
        :rtype: string
        """
        return getattr(self, 'video_url', '')

    def enabled(self):
        """Return True if viewlet is enabled.
        :param self: [required] Instance object
        :type self: instance object
        :returns: True if viewlet is enabled
        :rtype: boolean
        """
        enabled_content_types = api.portal.get_registry_record(
            IVLibrasVideoSettings.__identifier__ + '.enabled_content_types')
        if self.context.portal_type not in enabled_content_types:
            return False
        if not api.user.is_anonymous():
            return True
        return self.is_ready()

    def klass(self):
        """Return The viewlet css class.
        :param self: [required] Instance object
        :type self: instance object
        :returns: The viewlet css class
        :rtype: string
        """
        if self.is_ready():
            return 'ready'
