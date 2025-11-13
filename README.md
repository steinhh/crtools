# ftools

## C-based local image filters for cosmic ray detection and removal

`ftools` provides fast implementations of miscellaneous routines using C extensions.

## Features

- **`fmedian`**: Local median computation - automatically works with 2D and 3D arrays
- **`fsigma`**: Local population standard deviation - automatically works with 2D and 3D arrays
- **`fgaussian`** / **`fgaussian_f64`**: Fast Gaussian profile computation
  - `fgaussian`: Float32 version, ~7-10x faster than NumPy for small arrays, ~5x for large
  - `fgaussian_f64`: Float64 version for compatibility, ~2-3x faster than NumPy
  - Uses Apple Accelerate framework for vectorized computation
- **`fmedian` and `fsigma`**:
  - Optional center pixel/voxel exclusion for better outlier detection (default: include center)
  - Robust NaN handling
  - Correct edge handling (edge pixels/voxels use smaller neighborhoods)
  - Full test coverage with unit, edge case, and integration tests

## Requirements

- Python 3.8+
- NumPy >= 1.20
- C compiler toolchain (gcc, clang, or MSVC)
- macOS with Accelerate framework (for `fgaussian` optimal performance)

## Standard installation

```bash
pip install .
```

## Building extensions in-place (for development)

If you want to build the C extensions without installing:

```bash
python setup.py build_ext --inplace
```

## Git Hooks (Optional)

The repository includes a pre-commit hook in `hooks/pre-commit` that automatically increments the patch version number and appends the branch name on each commit.

To enable it, create a symlink:

```bash
ln -sf ../../hooks/pre-commit .git/hooks/pre-commit
```

This will automatically update the version in `setup.py` (e.g., `3.2.1-main` → `3.2.2-main`).

## Quick Start

```python
import numpy as np
from ftools import fmedian, fsigma
# Direct extension import for minimal overhead:
from ftools.fgaussian.fgaussian_ext import fgaussian

# Generate random input data
data_2d = np.random.normal(0.0, 1.0, (100, 200)).astype(np.float64)
data_3d = np.random.normal(0.0, 1.0, (100, 200, 100)).astype(np.float64)

xsize = ysize = zsize = 3
# 2D example
median_filtered_2d = fmedian(data_2d, (xsize, ysize), exclude_center=1)
sigma_map_2d = fsigma(data_2d, (xsize, ysize), exclude_center=1)

# 3D example
median_filtered_3d = fmedian(data_3d, (xsize, ysize, zsize))
sigma_map_3d = fsigma(data_3d, (xsize, ysize, zsize))

# Gaussian profile computation (float32 - fastest)
x_f32 = np.linspace(-10, 10, 1000, dtype=np.float32)
profile_f32 = fgaussian(x_f32, 1.0, 0.0, 1.5)

# Or use float64 version for compatibility
from ftools import fgaussian_f64
x_f64 = np.linspace(-10, 10, 1000, dtype=np.float64)
profile_f64 = fgaussian_f64(x_f64, 1.0, 0.0, 1.5)
```

## Parameters

### fmedian / fsigma

- `input_data`: Input NumPy array (2D or 3D, will be converted to float64)
- `window_size`: tuple with window sizes. Must be odd positive integers.
- `exclude_center`: Optional, if 1, exclude center pixel/voxel from filter calculation; if 0, include it (default: 0)

### fgaussian / fgaussian_f64

Both functions compute: `i0 * exp(-((x - mu)^2) / (2 * sigma^2))`

**fgaussian** (float32 - recommended for performance):

- `x`: Input array, dtype=float32 (no validation or conversion performed)
- `i0`: Peak intensity (scalar, float)
- `mu`: Center position (scalar, float)
- `sigma`: Width parameter (scalar, float, must be > 0)
- Returns: NumPy array of same shape as input, dtype=float32

**fgaussian_f64** (float64 - for compatibility):

- `x`: Input array, dtype=float64 (automatically converted if needed)
- `i0`: Peak intensity (scalar, float)
- `mu`: Center position (scalar, float)
- `sigma`: Width parameter (scalar, float, must be > 0)
- Returns: NumPy array of same shape as input, dtype=float64

## Returns

- **fmedian/fsigma**: NumPy array of same shape as input, dtype=float64
- **fgaussian**: NumPy array of same shape as input, dtype=float32
- **fgaussian_f64**: NumPy array of same shape as input, dtype=float64

## Examples

See the `examples` directory.

## Testing

Comprehensive tests covering unit tests, edge cases, parameter validation, and integration scenarios. Run tests using `pytest`:

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov=ftools --cov-report=html
```

## Project Structure

```bash
tree --gitignore
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

- **fmedian/fsigma**: Use float64, optimized sorting networks for small windows
- **fgaussian (float32)**: Uses Apple Accelerate framework
  - ~7-9x faster than NumPy for small arrays (N < 100)
  - ~5-7x faster than NumPy for large arrays (N ? 1000)
  - Vectorized exp() via Apple's vForce library (vvexpf)
  - Zero-copy in-place computation
  - Minimal overhead (~0.23 ?s) - direct C extension call
  - Accuracy: <1e-7 difference vs float64
- **fgaussian_f64 (float64)**: Also uses Apple Accelerate framework
  - ~2-3x faster than NumPy (slower than float32 due to memory bandwidth)
  - Vectorized exp() via Apple's vForce library (vvexp)
  - Full float64 precision maintained

## Credits

- Blazingly fast sorting networks adapted from [Sorting Networks](https://bertdobbelaere.github.io/sorting_networks.html)
- Many thanks to Claude!
