# crtools

## C-based local image filters for cosmic ray detection and removal

`crtools` provides fast, local neighborhood filters commonly used for cosmic ray detection and removal. The package currently includes two core filtering functions `fmedian` and `fsigma`, both implemented as C extensions with NumPy integration.

## Features

- **`fmedian`**: Filtered median computation over local neighborhoods
- **`fsigma`**: Local population standard deviation (sigma) calculation
- Optional center pixel exclusion for better outlier detection
- Full test coverage with unit, edge case, and integration tests

## Requirements

- Python 3.8+
- NumPy >= 1.20
- C compiler toolchain (gcc, clang, or MSVC)

## Installation

### From source (editable install for development)

```bash
# Clone the repository
git clone <repository-url>
cd crtools

# Install in editable mode
pip install -e .
```

### Standard installation

```bash
pip install .
```

### Building extensions in-place

If you want to build the C extensions without installing:

```bash
python setup.py build_ext --inplace
```

## Quick Start

```python
import numpy as np
from crtools import fmedian, fsigma

# Create sample data
data = np.random.normal(0.0, 1.0, (128, 128)).astype(np.float64)

# Apply filtered median (3x3 window, excluding center pixel)
median_filtered = fmedian(data, xsize=3, ysize=3, exclude_center=1)

# Calculate local sigma (3x3 window, excluding center pixel)
sigma_map = fsigma(data, xsize=3, ysize=3, exclude_center=1)
```

## Usage

### `fmedian` - Filtered Median

Computes the median of pixels in a local neighborhood around each pixel.

```python
from crtools import fmedian

output = fmedian(input_array, xsize, ysize, exclude_center)
```

**Parameters:**

- `input_array`: Input 2D NumPy array (will be converted to float64)
- `xsize`: Full window width (must be an odd number ? 1)
- `ysize`: Full window height (must be an odd number ? 1)
- `exclude_center`: If 1, exclude center pixel from median calculation; if 0, include it

**Returns:**

- NumPy array of same shape as input, containing filtered median values (float64)

**Example:**

```python
import numpy as np
from crtools import fmedian

# Create data with an outlier
data = np.ones((5, 5)) * 10.0
data[2, 2] = 100.0  # Cosmic ray hit

# Filter with 3x3 window, excluding center
filtered = fmedian(data, xsize=3, ysize=3, exclude_center=1)
# The outlier at [2,2] will be replaced with median of surrounding pixels
```

### `fsigma` - Local Standard Deviation

Computes the population standard deviation in a local neighborhood around each pixel.

```python
from crtools import fsigma

output = fsigma(input_array, xsize, ysize, exclude_center)
```

**Parameters:**

- `input_array`: Input 2D NumPy array (will be converted to float64)
- `xsize`: Full window width (must be an odd number ? 1)
- `ysize`: Full window height (must be an odd number ? 1)
- `exclude_center`: If 1, exclude center pixel from sigma calculation; if 0, include it

**Returns:**

- NumPy array of same shape as input, containing local sigma values (float64)

**Example:**

```python
import numpy as np
from crtools import fsigma

# Create uniform data with one outlier
data = np.ones((5, 5)) * 10.0
data[2, 2] = 100.0

# Calculate local sigma with 3x3 window
sigma = fsigma(data, xsize=3, ysize=3, exclude_center=1)
# High sigma value at [2,2] indicates an outlier
```

## Examples

Complete example scripts are provided in the package:

```bash
# Run the fmedian example
python src/crtools/fmedian/example_fmedian.py

# Run the fsigma example
python src/crtools/fsigma/example_fsigma.py
```

## Testing

The project includes comprehensive tests covering unit tests, edge cases, parameter validation, and integration scenarios.

### Run all tests

```bash
pytest
```

### Run specific test modules

```bash
# Unit tests
pytest tests/test_fmedian_unit.py
pytest tests/test_fsigma_unit.py

# Edge case tests
pytest tests/test_fmedian_edge_cases.py
pytest tests/test_fsigma_edge_cases.py

# Parameter validation tests
pytest tests/test_parameter_validation.py

# Integration tests
pytest tests/test_smoke_integration.py
```

### Run tests with coverage

```bash
pytest --cov=crtools --cov-report=html
```

## Project Structure

```text
crtools/
??? setup.py                          # Package configuration and build
??? pytest.ini                        # Pytest configuration
??? src/
?   ??? crtools/
?       ??? __init__.py              # Package entry point
?       ??? fmedian/
?       ?   ??? __init__.py          # fmedian module loader
?       ?   ??? fmedian_ext.c        # C implementation
?       ?   ??? example_fmedian.py   # Usage example
?       ?   ??? test_fmedian.py      # Module tests
?       ??? fsigma/
?           ??? __init__.py          # fsigma module loader
?           ??? fsigma_ext.c         # C implementation
?           ??? example_fsigma.py    # Usage example
?           ??? test_fsigma.py       # Module tests
??? tests/
?   ??? test_fmedian_unit.py         # fmedian unit tests
?   ??? test_fmedian_edge_cases.py   # fmedian edge cases
?   ??? test_fsigma_unit.py          # fsigma unit tests
?   ??? test_fsigma_edge_cases.py    # fsigma edge cases
?   ??? test_parameter_validation.py # Parameter validation tests
?   ??? test_smoke_integration.py    # Integration tests
??? scripts/
    ??? quickstart_smoke.py          # Quick smoke test
    ??? set_utf8_locale.sh           # Locale setup script
```

## Use Cases

### Cosmic Ray Detection

```python
import numpy as np
from crtools import fmedian, fsigma

# Read your astronomical image
image = np.load('science_image.npy')

# Calculate local statistics
local_median = fmedian(image, xsize=5, ysize=5, exclude_center=1)
local_sigma = fsigma(image, xsize=5, ysize=5, exclude_center=1)

# Detect cosmic rays (simple sigma-clipping approach)
deviation = np.abs(image - local_median)
threshold = 5.0  # 5-sigma threshold
cosmic_ray_mask = deviation > (threshold * local_sigma)

# Clean the image
cleaned_image = image.copy()
cleaned_image[cosmic_ray_mask] = local_median[cosmic_ray_mask]
```

### Image Quality Assessment

```python
# Calculate noise map across image
noise_map = fsigma(image, xsize=7, ysize=7, exclude_center=0)

# Identify regions with high local variation
high_noise_regions = noise_map > np.percentile(noise_map, 90)
```

## Development

### Building the extensions

The C extensions are built automatically during installation. For development:

```bash
# Build in-place
python setup.py build_ext --inplace

# Run tests
pytest

# Clean build artifacts
python setup.py clean --all
```

### Code Style

The project follows standard Python conventions:

- PEP 8 for Python code
- Type hints where applicable
- Comprehensive docstrings

## License

MIT License

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass (`pytest`)
2. New features include tests
3. Code follows project style conventions
4. Documentation is updated as needed

## Performance Notes

- Both functions convert input to `float64` for computation
- C implementations provide significant speedup over pure Python/NumPy equivalents
- Memory allocation is efficient with pre-allocated output arrays
- Edge handling uses appropriate boundary conditions

## Acknowledgments

These tools are designed for astronomical image processing workflows, particularly for removing cosmic ray
artifacts from CCD images.
