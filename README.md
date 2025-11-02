# CRTools: Cosmic Ray Removal Tools

A high-performance Python library for cosmic ray detection and removal in astronomical images.
This repository provides utility functions for removing cosmic ray hits in single exposures,
# CRTools: Cosmic Ray Removal Tools

High-performance C-backed utilities for local image filtering used in cosmic-ray
detection and removal workflows.

This repository provides two small C extensions exposed to Python:

- crtools.fmedian ? filtered median over a local neighborhood
- crtools.fsigma  ? local (population) standard deviation over a neighborhood

Key change: native C sources live under `src/crtools/<module>/` (e.g.
`src/crtools/fmedian/fmedian_ext.c`). Legacy prebuilt `.so` files and top-level
C sources were removed; build the package to produce extension modules.

## Requirements

- Python 3.8+
- NumPy
- C compiler toolchain (clang, gcc, or MSVC)

## Build & Install

Prefer using an editable install during development so Python imports the
package from `src/`:

```bash
# from repository root
python3 -m pip install -e .
```

To build extension modules in-place (no install):

```bash
python3 setup.py build_ext --inplace
```

To install normally:

```bash
python3 -m pip install .
```

Note: for isolated PEP 517 builds it's recommended to add a `pyproject.toml`
with build-system requirements (setuptools, wheel, numpy). If you'd like I can
add a minimal `pyproject.toml` for reproducible builds.

## Quick usage

```py
import numpy as np
from crtools import fmedian, fsigma

arr = np.random.normal(0.0, 1.0, (128, 128)).astype(np.float64)
out = np.zeros_like(arr)
fmedian(arr, out, 1, 1, 1)
```

## Running tests

Run tests against the locally built package (recommended to install/editable):

```bash
# ensure src/ is on PYTHONPATH (pip editable install handles this for you)
PYTHONPATH=src pytest -q
```

Or run individual scripts:

```bash
PYTHONPATH=src python3 fmedian/test_fmedian.py
PYTHONPATH=src python3 fsigma/test_fsigma.py
```

## Project layout

Relevant locations after these changes:

- `src/crtools/fmedian/` ? python + C source for fmedian
- `src/crtools/fsigma/`  ? python + C source for fsigma
- `setup.py`              ? setuptools configuration to build extensions

## Further improvements (optional)

- Add `pyproject.toml` with build-system requirements for PEP 517/518 builds
- Add CI workflow to build wheels and run tests on push/PR
- Add MANIFEST.in/package_data if you need to include non-Python files in sdist

If you want, I can add any of the above improvements.
