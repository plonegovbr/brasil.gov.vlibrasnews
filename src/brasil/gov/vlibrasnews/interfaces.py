# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews import _
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class IVLibrasNewsLayer(Interface):

    """A layer specific for this add-on product."""


class IVLibrasNewsSettings(model.Schema):

    """Schema for the control panel form."""

    access_token = schema.ASCIILine(
        title=_(u'Access Token'),
        description=_(u'Token to access the VLibras News API service.'),
        default='',
        required=True,
    )
