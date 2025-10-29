"""Convenience shim exposing core functions at top-level.

Usage:
    from cosmic_tools import fmedian, fsigma

This module prefers the package-qualified compiled extensions (e.g.
``from fmedian.fmedian_ext import fmedian``). If those are not available it
falls back to legacy top-level shims (``fmedian_ext`` / ``fsigma_ext``) if
present. If neither is available an ImportError will be raised.
"""
from __future__ import annotations

__all__ = ["fmedian", "fsigma"]

# fmedian
try:
    from fmedian.fmedian_ext import fmedian  # type: ignore
except Exception:
    try:
        # Legacy top-level shim
        from fmedian_ext import fmedian  # type: ignore
    except Exception as e:  # noqa: BLE001 - explicit import fallback
        raise ImportError(
            "Could not import 'fmedian'. Build the extension with: python setup.py build_ext --inplace"
        ) from e

# fsigma
try:
    from fsigma.fsigma_ext import fsigma  # type: ignore
except Exception:
    try:
        # Legacy top-level shim
        from fsigma_ext import fsigma  # type: ignore
    except Exception as e:  # noqa: BLE001 - explicit import fallback
        raise ImportError(
            "Could not import 'fsigma'. Build the extension with: python setup.py build_ext --inplace"
        ) from e
