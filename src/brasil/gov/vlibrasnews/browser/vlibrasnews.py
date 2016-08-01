# -*- coding: utf-8 -*-
"""Viewlets used on the package."""
from brasil.gov.vlibrasnews.exc import NotProcessingError
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsSettings
from brasil.gov.vlibrasnews.subscribers import get_video_url
from plone import api
from plone.app.layout.viewlets.common import ViewletBase


class VLibrasNewsViewlet(ViewletBase):

    """Viewlet with vlibrasnews button."""

    youtube_url = None
    is_ready = False
    enabled = False
    state = 'processing'

    def update(self):
        super(VLibrasNewsViewlet, self).update()
        try:
            self.youtube_url = get_video_url(self.context)
            self.is_ready = self.youtube_url is not None
            if self.is_ready:
                self.state = 'ready'
        except NotProcessingError:
            self.state = 'notprocessing'
        finally:
            record = '{0}.enabled_content_types'.format(
                IVLibrasNewsSettings.__identifier__)
            enabled_content_types = api.portal.get_registry_record(record)
            if self.context.portal_type in enabled_content_types:
                self.enabled = self.is_ready or not api.user.is_anonymous()
