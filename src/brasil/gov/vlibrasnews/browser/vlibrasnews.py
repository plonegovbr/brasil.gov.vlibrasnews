# -*- coding: utf-8 -*-
"""Viewlets used on the package."""
from brasil.gov.vlibrasnews.behaviors import IVLibrasNews
from brasil.gov.vlibrasnews.subscribers import get_video_url
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from time import time


class VLibrasNewsViewlet(ViewletBase):

    """Viewlet with vlibrasnews button."""

    @property
    def enabled(self):
        if not IVLibrasNews.providedBy(self.context):
            return False
        if self.context.video_url is None:
            return False
        is_ready = self.state == 'ready'
        return is_ready or not api.user.is_anonymous()

    @property
    def state(self):
        video_url = self.video_url
        if video_url is None:
            return 'notprocessing'
        elif video_url == '':
            return 'processing'
        return 'ready'

    @ram.cache(lambda method, self, context: (time() // 60, context))
    def _get_video_url(self, context):
        get_video_url(context)
        return getattr(context, 'video_url', None)

    @property
    def video_url(self):
        return self._get_video_url(self.context)
