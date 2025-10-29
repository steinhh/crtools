# muse_cosmic

muse_cosmic is a small project that provides a fast C-based median-style filter
implemented as a Python extension. It's intended for image-processing tasks such
as cosmic-ray removal in integral-field spectrograph (MUSE) data, but can be
used for general 2D array median operations.

This repository contains two small C-backed Python extensions and example/test scripts that demonstrate how to use them.

## Layout

- `fmedian/` ? original filtered-median implementation
  - `fmedian/fmedian_ext.c` ? C extension source (package module: `fmedian.fmedian_ext`, function: `fmedian`)
  - `fmedian/example_fmedian.py` ? runnable example
  - `fmedian/test_fmedian.py` ? small test script

- `fsigma/` ? a copy/adaptation with public names changed to *fsigma*
  - `fsigma/fsigma_ext.c` ? C extension source (package module: `fsigma.fsigma_ext`, function: `fsigma`)
  - `fsigma/example_fsigma.py` ? runnable example
  - `fsigma/test_fsigma.py` ? small test script

## Build & run

Both extensions are built by the top-level `setup.py`. To build the extensions in-place, run:

```bash
python3 setup.py build_ext --inplace
```

When built with `--inplace` the compiled extension modules are placed inside
their package directories (for example `fmedian/fmedian_ext.*.so`). After a
successful build you can run the examples and tests from the repository root. For example:

```bash
python3 fmedian/test_fmedian.py
python3 fmedian/example_fmedian.py

python3 fsigma/test_fsigma.py
python3 fsigma/example_fsigma.py
```

## Quickstart

Here is a tiny runnable example showing the preferred package import and the
convenience shim. Run this after building the extensions in-place.

```python
# preferred: import the compiled extension from the package
from fmedian.fmedian_ext import fmedian
import numpy as np

# sample 5x5 input
a = np.arange(25, dtype=np.float64).reshape(5, 5)
out = np.empty_like(a)

# apply the filter: xsize, ysize are window radii, exclude_center is a bool
fmedian(a, out, 3, 3, False)
print(out)
```

Or use the top-level convenience shim that re-exports both filters:

```python
from cosmic_tools import fmedian, fsigma
# fmedian(...) and fsigma(...) have the same call signature as above
```

## Notes


- The top-level `setup.py` builds both `fmedian.fmedian_ext` and `fsigma.fsigma_ext`.
  By default the build places the compiled modules inside their package directories when
  using `--inplace` (so imports like `from fmedian.fmedian_ext import fmedian` work).

- For backwards compatibility this repository also provides small top-level shims
  (`fmedian_ext.py`, `fsigma_ext.py`) and a convenience shim `cosmic_tools.py` so
  external code can still do either:

  - `from fmedian.fmedian_ext import fmedian` (preferred)
  - `import fmedian_ext  # legacy shim`
  - `from cosmic_tools import fmedian, fsigma` (convenience)

- API summary:
  - `fmedian(input_array, output_array, xsize, ysize, exclude_center)`
  - `fsigma(input_array, output_array, xsize, ysize, exclude_center)`

  Both functions accept 2-D `np.float64` input/output arrays and write results into `output_array`.

- If you prefer the compiled modules arranged differently for packaging (wheels, site-packages, etc.), I can update `setup.py` or provide packaging instructions.

## Contributing / CI

If you want CI (GitHub Actions) to build and run tests automatically on push/PR I can add a workflow that runs the in-place build and executes both test scripts.

If you spot any mismatches between the examples/tests and the C code, tell me and I'll fix them.
