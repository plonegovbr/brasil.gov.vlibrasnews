# -*- coding: utf-8 -*-
"""Viewlets used on the package."""
from brasil.gov.vlibrasvideo.utils import get_video_url
from plone import api
from plone.app.layout.viewlets.common import ViewletBase


class VLibrasVideoViewlet(ViewletBase):

    """Viewlet with VLibrasVideo button."""

    youtube_url = ''
    is_ready = False
    enabled = False
    klass = 'processing'

    def update(self):
        super(VLibrasVideoViewlet, self).update()
        self.youtube_url = get_video_url(self.context)
        self.is_ready = self.youtube_url is not None
        self.enabled = self.is_ready and not api.user.is_anonymous()
        if self.is_ready:
            self.klass = 'ready'
