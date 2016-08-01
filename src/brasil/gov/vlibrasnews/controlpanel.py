# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews import _
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsSettings
from plone.app.registry.browser import controlpanel


class VLibrasNewsSettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = IVLibrasNewsSettings
    label = _(u'VLibras News')
    description = _(u'Settings for the VLibras News API integration.')


class VLibrasNewsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = VLibrasNewsSettingsEditForm
