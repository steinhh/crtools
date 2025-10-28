# fmedian_ext - Filtered Median Python Extension

A Python C extension for computing filtered median values on 2D arrays. This extension is optimized for cosmic ray removal in astronomical imaging (MUSE).

## Features

- Fast C implementation for median filtering
- Threshold-based filtering to exclude outliers
- Configurable window size
- NumPy integration with int16 input and float64 output

## Building

To build the extension:

```bash
pip install numpy
python setup.py build_ext --inplace
```

This will create `fmedian_ext.cpython-*.so` in the current directory.

## Usage

```python
import numpy as np
import fmedian_ext

# Create input array (must be int16)
input_array = np.array([...], dtype=np.int16)

# Create output array (must be float64, same shape as input)
output_array = np.zeros_like(input_array, dtype=np.float64)

# Define parameters
xsize = np.int16(1)      # Window half-width in x direction
ysize = np.int16(1)      # Window half-width in y direction  
threshold = 50.0         # Threshold for including neighbors

# Apply filtered median
fmedian_ext.fmedian(input_array, output_array, xsize, ysize, threshold)
```

## Function Signature

```python
fmedian(input_array, output_array, xsize, ysize, threshold)
```

### Parameters

- `input_array` (numpy.ndarray): Input 2D array with dtype=np.int16
- `output_array` (numpy.ndarray): Output 2D array with dtype=np.float64 (same size as input)
- `xsize` (int16): Half-width of the filter window in x direction
- `ysize` (int16): Half-width of the filter window in y direction
- `threshold` (float64): Threshold for including values in median calculation. Only values where `|value - center_value| < threshold` are included.

### Returns

None (modifies `output_array` in place)

## Examples

Run the example program:

```bash
python example_fmedian.py
```

Run the test suite:

```bash
python test_fmedian.py
```

## How It Works

For each pixel in the input array:
1. Consider all pixels in a window of size `(2*xsize+1) × (2*ysize+1)` centered on the pixel
2. Only include neighbor pixels where `|neighbor_value - center_value| < threshold`
3. Compute the median of the included values
4. Store the result in the output array

This approach effectively filters out cosmic rays and other outliers while preserving the structure of the image.

## Installation

To install the package:

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

## Requirements

- Python 3.8+
- NumPy

## License

MIT License (or specify your license)
