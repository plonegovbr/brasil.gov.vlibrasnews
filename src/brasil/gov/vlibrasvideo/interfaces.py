# -*- coding: utf-8 -*-
from brasil.gov.vlibrasvideo import _
from brasil.gov.vlibrasvideo.config import DEFAULT_ENABLED_CONTENT_TYPES
from plone.directives import form
from zope import schema
from zope.interface import Interface


class IBrasilGov(Interface):

    """A layer specific for this add-on product."""


class IVLibrasVideoSettings(form.Schema):

    """Schema for the control panel form."""

    vlibrasvideo_token = schema.TextLine(
        title=_(u'VLibras Video Token'),
        description=_(
            u'Add the secret token to call VLibras API.'),
        default=u'',
        required=True,
    )

    enabled_content_types = schema.List(
        title=_(u'Enabled Content Types'),
        description=_(u'Only objects of these content types will display glossary terms.'),
        required=False,
        default=DEFAULT_ENABLED_CONTENT_TYPES,
        # we are going to list only the main content types in the widget
        value_type=schema.Choice(
            vocabulary=u'brasil.gov.vlibrasvideo.PortalTypes'),
    )
