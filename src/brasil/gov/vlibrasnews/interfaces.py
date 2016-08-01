# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews import _
from brasil.gov.vlibrasnews.config import DEFAULT_ENABLED_CONTENT_TYPES
from plone.directives import form
from zope import schema
from zope.interface import Interface


class IVLibrasNewsLayer(Interface):

    """A layer specific for this add-on product."""


class IVLibrasNewsSettings(form.Schema):

    """Schema for the control panel form."""

    access_token = schema.ASCIILine(
        title=_(u'Access Token'),
        description=_(u'Token to access the VLibras News API service.'),
        default='',
        required=True,
    )

    enabled_content_types = schema.List(
        title=_(u'Enabled Content Types'),
        description=_(u'Only objects of these content types will display vlibras icon.'),
        required=False,
        default=DEFAULT_ENABLED_CONTENT_TYPES,
        # we are going to list only the main content types in the widget
        value_type=schema.Choice(
            vocabulary=u'plone.app.vocabularies.ReallyUserFriendlyTypes'),
    )
