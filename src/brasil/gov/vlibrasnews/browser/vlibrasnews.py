# -*- coding: utf-8 -*-
"""Viewlets used on the package."""
from brasil.gov.vlibrasnews.exc import NotProcessingError
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsSettings
from brasil.gov.vlibrasnews.subscribers import get_video_url
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from time import time


class VLibrasNewsViewlet(ViewletBase):

    """Viewlet with vlibrasnews button."""

    @property
    def enabled(self):
        record = IVLibrasNewsSettings.__identifier__ + '.enabled_content_types'
        enabled_content_types = api.portal.get_registry_record(record)
        if self.context.portal_type not in enabled_content_types:
            return False

        is_ready = self.state == 'ready'
        return is_ready or not api.user.is_anonymous()

    @property
    def state(self):
        try:
            video_url = self.video_url
        except NotProcessingError:
            return 'notprocessing'

        if video_url is None:
            return 'processing'

        return 'ready'

    @ram.cache(lambda method, self, context: (time() // 60, context))
    def _get_video_url(self, context):
        return get_video_url(context)

    @property
    def video_url(self):
        return self._get_video_url(self.context)
