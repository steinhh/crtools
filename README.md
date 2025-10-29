# CRTools: Cosmic Ray Removal Tools

A high-performance Python library for cosmic ray detection and removal in astronomical images.
This repository provides utility functions for removing cosmic ray hits in single exposures,
implemented as C extensions for optimal speed.

## Overview

CRTools implements two core algorithms for cosmic ray detection and removal:

- **`fmedian`**: Filtered median computation for outlier smoothing
- **`fsigma`**: Local standard deviation calculation for statistical outlier detection

Both functions are implemented in C for maximum performance while maintaining a simple Python interface.

## Features

- **High Performance**: C implementations provide significant speedup over pure Python
- **Robust Cosmic Ray Detection**: Uses local statistics to identify and remove cosmic ray hits
- **Flexible Window Sizes**: Configurable neighborhood sizes for different image characteristics
- **NumPy Integration**: Seamless integration with NumPy arrays
- **Well Tested**: Comprehensive test suite ensures reliability

## Installation

### Prerequisites

- Python 3.7+
- NumPy
- C compiler (gcc, clang, or MSVC)

### Build from Source

Clone the repository:

```bash
git clone <repository-url>
cd crtools
```

Build the C extensions:

```bash
python setup.py build_ext --inplace
```

Install the package:

```bash
pip install .
```

Or install in development mode:

```bash
pip install -e .
```

## Quick Start

```python
import numpy as np
from crtools import fmedian, fsigma

# Create sample astronomical image data
image = np.random.normal(100, 10, (256, 256)).astype(np.float64)
# Add some cosmic ray hits (bright outliers)
image[100, 100] = 5000  # cosmic ray hit

# Method 1: Use filtered median to smooth outliers
smoothed = np.zeros_like(image)
fmedian(image, smoothed, xsize=1, ysize=1, exclude_center=1)

# Method 2: Use sigma-clipping approach
sigma_map = np.zeros_like(image)
fsigma(image, sigma_map, xsize=2, ysize=2, exclude_center=1)

# Calculate z-scores for outlier detection
mean_image = smoothed  # or compute local mean separately
z_scores = (image - mean_image) / (sigma_map + 1e-8)

# Identify cosmic rays (e.g., >5 sigma outliers)
cosmic_ray_mask = np.abs(z_scores) > 5.0

# Replace cosmic rays with smoothed values
cleaned_image = image.copy()
cleaned_image[cosmic_ray_mask] = smoothed[cosmic_ray_mask]
```

## API Reference

### fmedian

Computes a filtered median over a local neighborhood around each pixel.

```python
fmedian(input_array, output_array, xsize, ysize, exclude_center)
```

**Parameters:**

- `input_array` (numpy.ndarray): Input image array (float64)
- `output_array` (numpy.ndarray): Output array for results (float64, same shape as input)
- `xsize` (int): Half-width of window in x-direction
- `ysize` (int): Half-width of window in y-direction  
- `exclude_center` (int): If 1, exclude center pixel from median calculation; if 0, include it

**Window Size:** The actual window size is `(2*xsize+1) × (2*ysize+1)`.

### fsigma

Computes the local standard deviation over a neighborhood around each pixel.

```python
fsigma(input_array, output_array, xsize, ysize, exclude_center)
```

**Parameters:**

- `input_array` (numpy.ndarray): Input image array (float64)
- `output_array` (numpy.ndarray): Output array for standard deviation values (float64, same shape as input)
- `xsize` (int): Half-width of window in x-direction
- `ysize` (int): Half-width of window in y-direction
- `exclude_center` (int): If 1, exclude center pixel from sigma calculation; if 0, include it

## Examples

### Basic Cosmic Ray Removal

```python
import numpy as np
from crtools import fmedian, fsigma

# Load your astronomical image
image = fits.getdata('your_image.fits').astype(np.float64)

# Create output arrays
median_filtered = np.zeros_like(image)
sigma_map = np.zeros_like(image)

# Compute local statistics (3x3 windows)
fmedian(image, median_filtered, 1, 1, 1)  # exclude center
fsigma(image, sigma_map, 1, 1, 1)

# Detect outliers
z_scores = (image - median_filtered) / (sigma_map + 1e-8)
cosmic_rays = np.abs(z_scores) > 5.0

# Clean the image
cleaned = image.copy()
cleaned[cosmic_rays] = median_filtered[cosmic_rays]
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific module tests
python fmedian/test_fmedian.py
python fsigma/test_fsigma.py

# Run smoke test
python scripts/quickstart_smoke.py
```

### Development Dependencies

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

This includes:

- pytest and pytest-cov for testing
- matplotlib for examples and visualization

### Project Structure

```text
crtools/
?   ??? fmedian_ext.c     # C implementation
?   ??? example_fmedian.py
?   ??? test_fmedian.py
??? fsigma/                  # Fsigma module for local standard deviation
?   ??? fsigma_ext.c      # C implementation
?   ??? example_fsigma.py
?   ??? test_fsigma.py
??? scripts/              # Utility scripts
??? tests/                # Additional tests
??? crtools.py           # Main convenience import module
??? cosmic_tools.py      # Alternative import interface
??? setup.py             # Build configuration
```

## Performance

The C implementations provide significant performance improvements over pure Python/NumPy implementations:

- **fmedian**: Optimized median calculation with boundary handling
- **fsigma**: Efficient standard deviation computation
- **Memory efficient**: In-place operations where possible
- **Boundary handling**: Proper edge/corner pixel treatment

## License

[Include your license information here]

## Contributing

[Include contribution guidelines here]

## Citation

If you use CRTools in your research, please cite:

[Include citation information if applicable]

## Acknowledgments

This library was developed for astronomical image processing applications,
particularly for removing cosmic ray artifacts from CCD/CMOS detector images.
