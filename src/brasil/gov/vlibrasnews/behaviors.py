# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IVLibrasNews(model.Schema):

    """VLibras News behavior. Read-only field to store the address of
    the video containing the LIBRAS translation of an item. A `None`
    value indicates content that was present before the installation
    of the feature; this content has no translation available. An empty
    string indicates content being processed.
    """

    translation_url = schema.ASCIILine(
        title=_(u'Video URL'),
        description=_(u'The URL of the video containing the LIBRAS translation for this item.'),
        required=False,
        readonly=True,
        default='',  # translation being processed
        missing_value=None,  # no translation available
    )
