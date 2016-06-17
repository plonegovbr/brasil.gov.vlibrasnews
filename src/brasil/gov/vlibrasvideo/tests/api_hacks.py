# -*- coding: utf-8 -*-
"""Hacks to work around API inconsistencies between Archetypes and Dexterity."""


def set_text_field(obj, text):
    """Set text field in object on both, Archetypes and Dexterity."""
    try:
        obj.setText(text)  # Archetypes
    except AttributeError:
        from plone.app.textfield.value import RichTextValue
        obj.text = RichTextValue(text, 'text/html', 'text/html')  # Dexterity
    finally:
        obj.reindexObject()


def get_text_field(obj):
    """Get text field in object on both, Archetypes and Dexterity."""
    text = ''
    try:
        raw = obj.getText()  # Archetypes
        if raw != '':
            from lxml import html
            el = html.fromstring(raw)
            text = el.text_content()
    except AttributeError:
        from plone.app.textfield.value import IRichTextValue
        if IRichTextValue.providedBy(obj.text):  # Dexterity
            from plone.app.textfield.interfaces import ITransformer
            transformer = ITransformer(obj)
            text = transformer(obj.text, 'text/plain')
    return text
