"""crtools.fsigma package loader.

Locate the pre-built `fsigma` extension in the repository and load it.
Expose `fsigma` at package level for `from crtools import fsigma` imports.
"""
from __future__ import annotations

import glob
import importlib.machinery
import importlib.util
import os

try:
    from . import _fsigma_ext as _ext  # type: ignore
except Exception:
    _HERE = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))

    candidates = glob.glob(os.path.join(_HERE, "fsigma_ext*.so"))
    if not candidates:
        candidates = glob.glob(os.path.join(repo_root, "fsigma", "fsigma_ext*.so"))
        if not candidates:
            candidates = glob.glob(os.path.join(repo_root, "fsigma", "fsigma_ext*.*.so"))

    if not candidates:
        raise ImportError(
            "Could not locate the compiled fsigma extension (expected src/crtools/fsigma/fsigma_ext*.so or fsigma/fsigma_ext*.so). "
            "Build it first or install the package so the extension is available."
        )

    so_path = candidates[0]
    # Ensure loader name matches the compiled module name (so the PyInit symbol matches)
    base = os.path.basename(so_path)
    base_mod = os.path.splitext(base)[0].split(".")[0]
    loader = importlib.machinery.ExtensionFileLoader(base_mod, so_path)
    spec = importlib.util.spec_from_loader(base_mod, loader)
    _ext = importlib.util.module_from_spec(spec)
    loader.exec_module(_ext)  # type: ignore[arg-type]

try:
    fsigma = _ext.fsigma  # type: ignore[attr-defined]
except Exception as exc:  # pragma: no cover - defensive
    raise ImportError("Loaded fsigma extension but could not find 'fsigma' symbol") from exc

__all__ = ["fsigma"]
