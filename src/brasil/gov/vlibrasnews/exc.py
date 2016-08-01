# -*- coding: utf-8 -*-
"""Exceptions raised by brasil.gov.vlibrasnews methods."""


class BrasilGovVLibrasNewsError(Exception):
    """Base exception class for brasil.gov.vlibrasnews errors."""


class NotProcessingError(BrasilGovVLibrasNewsError):
    """Raised when the video is not ready and not being processed."""
