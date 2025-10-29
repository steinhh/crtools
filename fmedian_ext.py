"""Backward-compatibility shim for importing the compiled extension as
``import fmedian_ext``.

Prefer using the package-qualified import ``from fmedian import fmedian_ext``.
This shim will attempt to import the package submodule first and fall back to
an older top-level compiled extension if present.
"""
try:
    # Preferred: extension built as package submodule
    from fmedian import fmedian_ext as _real
except Exception:
    # Fallback: try to import a top-level compiled extension (legacy)
    try:
        import importlib

        _real = importlib.import_module('fmedian_ext')
    except Exception as e:  # re-raise as ImportError to show helpful message
        raise ImportError(
            "Could not import 'fmedian_ext'. Build the extension with: python setup.py build_ext --inplace"
        ) from e

# Re-export public names
for _name in dir(_real):
    if not _name.startswith('_'):
        globals()[_name] = getattr(_real, _name)

__all__ = [n for n in globals() if not n.startswith('_')]
