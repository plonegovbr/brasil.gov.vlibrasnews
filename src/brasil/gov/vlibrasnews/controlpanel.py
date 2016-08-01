# -*- coding: utf-8 -*-
from brasil.gov.vlibrasnews import _
from brasil.gov.vlibrasnews.interfaces import IVLibrasNewsSettings
from plone.app.registry.browser import controlpanel


class VLibrasNewsSettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = IVLibrasNewsSettings
    label = _(u'VLibrasNews')
    description = _(u'Settings for the brasil.gov.vlibrasnews package')


class VLibrasNewsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = VLibrasNewsSettingsEditForm
