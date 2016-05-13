# -*- coding: utf-8 -*-
from brasil.gov.vlibrasvideo import _
from brasil.gov.vlibrasvideo.interfaces import IVLibrasVideoSettings
from plone.app.registry.browser import controlpanel


class VLibrasVideoSettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = IVLibrasVideoSettings
    label = _(u'VLibrasVideo')
    description = _(u'Settings for the brasil.gov.vlibrasvideo package')


class VLibrasVideoSettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = VLibrasVideoSettingsEditForm
