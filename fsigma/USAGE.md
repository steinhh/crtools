# fsigma_ext - Filtered Sigma-style Python extension

Lightweight C extension (copied/adapted from fmedian) that computes a neighborhood-based operation on 2D NumPy arrays.
The implementation in this directory has the public API renamed to `fsigma` and the module is `fsigma_ext`.

This document describes the current, minimal API and how to build and run the example/tests.

## Features

- Fast C implementation for local standard-deviation (sigma) computation
- Configurable window size
- NumPy integration with float64 input/output
- Center pixel exclusion from sigma calculation
  
## Current status

- `exclude_center == 0` => include the center pixel in the sigma calculation (default behavior)
- `exclude_center != 0` => exclude the center pixel when computing sigma

## Building

See README.md for build instructions.

## Function signature

```python
fsigma(input_array, output_array, xsize, ysize, exclude_center)
```

Parameters

- `input_array` (numpy.ndarray): 2-D array, dtype `np.float64`.
- `output_array` (numpy.ndarray): 2-D array, dtype `np.float64`, same shape as `input_array`.
- `xsize` (int): half-width of the window along X (window width = 2*xsize+1).
- `ysize` (int): half-width of the window along Y (window height = 2*ysize+1).
- `exclude_center` (int): if non-zero, the center pixel is excluded from the sigma computation.

## Minimal usage example

```python
import numpy as np
from fsigma.fsigma_ext import fsigma

input_array = np.array([[1.0, 2.0, 3.0], [4.0, 999.0, 6.0], [7.0, 8.0, 9.0]], dtype=np.float64)
output_array = np.zeros_like(input_array, dtype=np.float64)

# 3x3 neighborhood, exclude center from computation
fsigma(input_array, output_array, 1, 1, 1)

print(output_array)
```

## Example program

Run the provided example:

```bash
python3 fsigma/example_fsigma.py
```

## Tests

Run the test suite (a small script `test_fsigma.py` is included):

```bash
python3 fsigma/test_fsigma.py
# or run the full pytest suite from the repository root:
python3 -m pytest -q
```

## Notes

Older versions used a `threshold` parameter and/or an `include_center` boolean with the
opposite meaning. Update old calls by inverting the last boolean: `new_exclude = 0 if old_include else 1`.
