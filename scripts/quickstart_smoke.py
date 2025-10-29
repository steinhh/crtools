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

print("Running quickstart smoke test...")

# Preferred package import
try:
    from fmedian.fmedian_ext import fmedian as fmedian_pkg
    print("Imported fmedian from fmedian.fmedian_ext")
except Exception as e:
    print("Failed to import fmedian.fmedian_ext:", e)
    raise

# Convenience shim import
try:
    from cosmic_tools import fmedian as fmedian_shim, fsigma as fsigma_shim
    print("Imported fmedian/fsigma from cosmic_tools")
except Exception as e:
    print("Failed to import from cosmic_tools:", e)
    raise

# create a small test array
a = np.arange(25.0, dtype=np.float64).reshape(5, 5)
out = np.empty_like(a)

# Call the package-imported function
try:
    fmedian_pkg(a, out, 1, 1, 0)
    print("fmedian_pkg call succeeded. sample output[2,2] =", out[2,2])
except Exception:
    print("fmedian_pkg call raised an exception")
    raise

# Call the shim-imported function (sanity; same signature)
try:
    fmedian_shim(a, out, 1, 1, 0)
    print("fmedian_shim call succeeded. sample output[2,2] =", out[2,2])
except Exception:
    print("fmedian_shim call raised an exception")
    raise

print("quickstart smoke test completed successfully")
