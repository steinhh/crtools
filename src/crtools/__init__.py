"""Top level package for crtools.

Expose convenience function names at package level so tests can do
`from crtools import fmedian` and `from crtools import fsigma`.
"""
from .fmedian import fmedian as fmedian
from .fsigma import fsigma as fsigma

__all__ = ["fmedian", "fsigma"]
