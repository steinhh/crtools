"""crtools package public API.

Import the optimized C extensions for median and sigma filters.

Usage:
    from crtools import fmedian, fsigma
"""
from __future__ import annotations

__all__ = ["fmedian", "fsigma"]

try:
    from fmedian.fmedian_ext import fmedian  # type: ignore
except ImportError as e:
    raise ImportError(
        "Could not import 'fmedian' from package 'fmedian'.\n"
        "Build the extension with: python3 setup.py build_ext --inplace"
    ) from e

try:
    from fsigma.fsigma_ext import fsigma  # type: ignore
except ImportError as e:
    raise ImportError(
        "Could not import 'fsigma' from package 'fsigma'.\n"
        "Build the extension with: python3 setup.py build_ext --inplace"
    ) from e
