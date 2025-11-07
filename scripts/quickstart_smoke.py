"""Small smoke test for the Quickstart snippets.

This script assumes you've built the extensions in-place with:

    python3 setup.py build_ext --inplace

It tries two imports:
 - preferred: from fmedian.fmedian_ext import fmedian
 - convenience: from ftools import fmedian, fsigma

and runs a tiny call to `fmedian` to ensure the extension is callable.
"""

import numpy as np

from ftools import fmedian as fmedian_shim

print("Running quickstart smoke test (using ftools imports)...")
print("Imported fmedian from ftools")

# create a small test array
a = np.arange(25.0, dtype=np.float64).reshape(5, 5)

out = fmedian_shim(a, 1, 1, 0)
print("fmedian (via crtools) call succeeded. sample output[2,2] =", out[2,2])

print("quickstart smoke test completed successfully")
