# fmedian_ext - Filtered Median Python extension

Lightweight C extension that computes a median-filter-like operation on 2D NumPy arrays. The
implementation is intended for image-processing tasks such as cosmic-ray removal where a median of
neighboring pixels is used to replace outliers.

This document describes the current, minimal API and how to build and run the example/tests.

## Features

- Fast C implementation for median filtering
- Configurable window size
- NumPy integration with int16 input and float64 output
- Center pixel exclusion from median calculation
  
## Current status

- `exclude_center == 0` => include the center pixel in the median calculation (default behavior)
- `exclude_center != 0` => exclude the center pixel when computing the median

## Building
See README.md for build instructions.

## Function signature

```python
fmedian(input_array, output_array, xsize, ysize, exclude_center)
```

Parameters

- `input_array` (numpy.ndarray): 2-D array, dtype `np.float64`.
- `output_array` (numpy.ndarray): 2-D array, dtype `np.float64`, same shape as `input_array`.
- `xsize` (int): half-width of the window along X (window width = 2*xsize+1).
- `ysize` (int): half-width of the window along Y (window height = 2*ysize+1).
- `exclude_center` (int): if non-zero, the center pixel is excluded from the median computation.

Return value: None (the result is written into `output_array`).

## Minimal usage example

```python
import numpy as np
import fmedian_ext

input_array = np.array([[1.0, 2.0, 3.0], [4.0, 999.0, 6.0], [7.0, 8.0, 9.0]], dtype=np.float64)
output_array = np.zeros_like(input_array, dtype=np.float64)

# 3x3 neighborhood, exclude center from median
fmedian_ext.fmedian(input_array, output_array, 1, 1, 1)

print(output_array)
```

## Example program

Run the provided example:

```bash
python fmedian/example_fmedian.py
```

## Tests

Run the test suite (a small script `test_fmedian.py` is included):

```bash
python fmedian/test_fmedian.py
```

## Notes

Older versions used a `threshold` parameter and/or an `include_center` boolean with the
opposite meaning. Update old calls by inverting the last boolean: `new_exclude = 0 if old_include else 1`.
