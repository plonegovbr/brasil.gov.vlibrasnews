# -*- coding: utf-8 -*-
"""Exceptions raised by brasil.gov.vlibras methods."""


class BrasilGovVlibrasError(Exception):
    """Base exception class for brasil.gov.vlibras errors."""


class NotProcessingError(BrasilGovVlibrasError):
    """Raised when the video is not ready and not being processed."""
