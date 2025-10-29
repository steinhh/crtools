"""Small smoke test for the Quickstart snippets.

This script assumes you've built the extensions in-place with:

    python3 setup.py build_ext --inplace

It tries two imports:
 - preferred: from fmedian.fmedian_ext import fmedian
 - convenience: from cosmic_tools import fmedian, fsigma

and runs a tiny call to `fmedian` to ensure the extension is callable.
"""

import sys
import numpy as np

print("Running quickstart smoke test (using cosmic_tools imports)...")

# Import only via the supported convenience shim
from cosmic_tools import fmedian as fmedian_shim, fsigma as fsigma_shim
print("Imported fmedian/fsigma from cosmic_tools")

# create a small test array
a = np.arange(25.0, dtype=np.float64).reshape(5, 5)
out = np.empty_like(a)

fmedian_shim(a, out, 1, 1, 0)
print("fmedian (via cosmic_tools) call succeeded. sample output[2,2] =", out[2,2])

print("quickstart smoke test completed successfully")
