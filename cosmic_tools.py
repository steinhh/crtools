"""Convenience shim exposing core functions at top-level.

Usage:
    from cosmic_tools import fmedian, fsigma

This module is the supported, canonical import surface for the project.
Use:

    from cosmic_tools import fmedian, fsigma

The module imports the compiled extension implementations from their package
locations (``fmedian.fmedian_ext`` and ``fsigma.fsigma_ext``). If those
compiled extensions are not available the import will fail with an
ImportError that instructs the user to build the extensions.
"""
from __future__ import annotations

__all__ = ["fmedian", "fsigma"]

# fmedian
try:
    from fmedian.fmedian_ext import fmedian  # type: ignore
except ImportError as e:
    # Fail fast: require users to import via `cosmic_tools` and ensure the
    # compiled extension is available (built in-place or installed).
    raise ImportError(
        "Could not import 'fmedian' from package 'fmedian'.\n"
        "Build the extension with: python3 setup.py build_ext --inplace"
    ) from e

# fsigma
try:
    from fsigma.fsigma_ext import fsigma  # type: ignore
except ImportError as e:
    raise ImportError(
        "Could not import 'fsigma' from package 'fsigma'.\n"
        "Build the extension with: python3 setup.py build_ext --inplace"
    ) from e
