"""Top level package for crtools.

Expose convenience function names at package level so tests can do
`from crtools import fmedian` and `from crtools import fsigma`.
"""
from .fmedian import fmedian as fmedian
from .fsigma import fsigma as fsigma
from .fmedian3 import fmedian3 as fmedian3
from .fsigma3 import fsigma3 as fsigma3

__version__ = "1.0.0"
__all__ = ["fmedian", "fsigma", "fmedian3", "fsigma3"]
