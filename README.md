# crtools

## C-based local image filters for cosmic ray detection and removal

`crtools` provides fast, local neighborhood filters `fmedian` and `fsigma` that automatically handle both 2D and 3D arrays, implemented as C extensions with NumPy integration.

## Features

- **`fmedian`**: Filtered median computation - automatically works with 2D and 3D arrays
- **`fsigma`**: Local population standard deviation - automatically works with 2D and 3D arrays
- Optional center pixel/voxel exclusion for better outlier detection (default: include center)
- Robust NaN handling
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

# Works with both 2D and 3D data automatically!

# 2D example
data_2d = np.random.normal(0.0, 1.0, (128, 128)).astype(np.float64)
xsize = ysize = 3
median_filtered_2d = fmedian(data_2d, xsize, ysize)
sigma_map_2d = fsigma(data_2d, xsize, ysize)

# 3D example  
data_3d = np.random.normal(0.0, 1.0, (64, 64, 64)).astype(np.float64)
xsize = ysize = zsize = 3
median_filtered_3d = fmedian(data_3d, xsize, ysize, zsize)
sigma_map_3d = fsigma(data_3d, xsize, ysize, zsize)
```

## Usage

#### `fmedian` - Filtered Median (2D/3D)

Computes the median of pixels/voxels in a local neighborhood around each pixel/voxel.

```python
from crtools import fmedian

# For 2D arrays
output_2d = fmedian(input_array_2d, xsize, ysize, exclude_center=0)

# For 3D arrays  
output_3d = fmedian(input_array_3d, xsize, ysize, zsize, exclude_center=0)
```

**Parameters:**

- `input_array`: Input NumPy array (2D or 3D, will be converted to float64)
- `xsize`: Full window width (must be an odd number ? 1)
- `ysize`: Full window height (must be an odd number ? 1)  
- `zsize`: Full window depth (required for 3D arrays, ignored for 2D arrays)
- `exclude_center`: Optional, if 1, exclude center pixel/voxel from median calculation; if 0, include it (default: 0)

**Returns:**

- NumPy array of same shape as input, containing filtered median values (float64)

**Examples:**

```python
import numpy as np
from crtools import fmedian

# 2D example
data_2d = np.ones((5, 5)) * 10.0
data_2d[2, 2] = 100.0  # Outlier

# Filter with 3x3 window (center included by default)
filtered_2d = fmedian(data_2d, xsize=3, ysize=3)

# Exclude center pixel for outlier detection
filtered_2d_no_center = fmedian(data_2d, xsize=3, ysize=3, exclude_center=1)

# 3D example
data_3d = np.ones((5, 5, 5)) * 10.0
data_3d[2, 2, 2] = 100.0  # Outlier

# Filter with 3x3x3 window (center included by default)
filtered_3d = fmedian(data_3d, xsize=3, ysize=3, zsize=3)

# Exclude center voxel for outlier detection
filtered_3d_no_center = fmedian(data_3d, xsize=3, ysize=3, zsize=3, exclude_center=1)
```

#### `fsigma` - Local Standard Deviation (2D/3D)

Computes the population standard deviation in a local neighborhood around each pixel/voxel.

```python
from crtools import fsigma

# For 2D arrays
output_2d = fsigma(input_array_2d, xsize, ysize, exclude_center=0)

# For 3D arrays
output_3d = fsigma(input_array_3d, xsize, ysize, zsize, exclude_center=0)
```

**Parameters:**

- `input_array`: Input NumPy array (2D or 3D, will be converted to float64)
- `xsize`: Full window width (must be an odd number ? 1)
- `ysize`: Full window height (must be an odd number ? 1)
- `zsize`: Full window depth (required for 3D arrays, ignored for 2D arrays)
- `exclude_center`: Optional, if 1, exclude center pixel/voxel from sigma calculation; if 0, include it (default: 0)

**Returns:**

- NumPy array of same shape as input, containing local sigma values (float64)

**Examples:**

```python
import numpy as np
from crtools import fsigma

# 2D example
data_2d = np.ones((5, 5)) * 10.0
data_2d[2, 2] = 100.0  # Outlier

# Calculate local sigma with 3x3 window (center included by default)
sigma_2d = fsigma(data_2d, xsize=3, ysize=3)

# Exclude center for outlier detection  
sigma_2d_no_center = fsigma(data_2d, xsize=3, ysize=3, exclude_center=1)

# 3D example
data_3d = np.random.normal(0.0, 1.0, (64, 64, 64)).astype(np.float64)
data_3d[32, 32, 32] = 100.0  # Outlier

# Calculate local 3D sigma with 3x3x3 window (center included by default)
sigma_3d = fsigma(data_3d, xsize=3, ysize=3, zsize=3)

# Exclude center voxel for outlier detection
sigma_3d_no_center = fsigma(data_3d, xsize=3, ysize=3, zsize=3, exclude_center=1)
```

## Examples

Complete example scripts are provided in the package:

```bash
# Run the 2D examples
python src/crtools/fmedian/example_fmedian.py
python src/crtools/fsigma/example_fsigma.py

# Run the 3D examples  
python src/crtools/fmedian3/example_fmedian3.py
python src/crtools/fsigma3/example_fsigma3.py
```


## Testing

The project includes comprehensive tests covering unit tests, edge cases, parameter validation, and integration scenarios. Run tests using `pytest`:

```bash
pytest
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
- Edge handling uses appropriate boundary conditions
