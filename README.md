# CRTools: Cosmic Ray Removal Tools

Small, fast C-backed utilities for local image filtering used in cosmic-ray detection and removal workflows. The project exposes two extension modules:

- `crtools.fmedian` ? filtered median over a local neighborhood
- `crtools.fsigma`  ? local (population) standard deviation over a neighborhood

## Requirements

- Python 3.8+
- NumPy
- A C compiler toolchain (clang, gcc, or MSVC)

## Build & install

During development prefer an editable install so imports resolve to the
`src/` tree:

```bash
# from repository root
python3 -m pip install -e .
```

Build extension modules in-place (no install):

```bash
python3 setup.py build_ext --inplace
```

Install normally:

```bash
python3 -m pip install .
```

## Quick usage

```py
import numpy as np
from crtools import fmedian, fsigma

arr = np.random.normal(0.0, 1.0, (128, 128)).astype(np.float64)
# fmedian returns a new float64 array
out = fmedian(arr, 1, 1, 1)
# fsigma is the C extension that still expects an output array (in-place)
out2 = np.zeros_like(arr)
fsigma(arr, out2, 1, 1, 1)
```

## Running tests

Run the test-suite against the local package (editable install or PYTHONPATH):

```bash
# ensure src/ is on PYTHONPATH (pip editable install handles this for you)
PYTHONPATH=src pytest -q
```

Or run individual module tests:

```bash
PYTHONPATH=src python3 fmedian/test_fmedian.py
PYTHONPATH=src python3 fsigma/test_fsigma.py
```
