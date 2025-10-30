"""fsigma package.

Exports:
    fsigma: the compiled extension entry point
"""
from __future__ import annotations

from .fsigma_ext import fsigma  # type: ignore

__all__ = ["fsigma"]
