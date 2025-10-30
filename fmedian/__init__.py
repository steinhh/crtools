"""fmedian package.

Exports:
    fmedian: the compiled extension entry point
"""
from __future__ import annotations

from .fmedian_ext import fmedian  # type: ignore

__all__ = ["fmedian"]
