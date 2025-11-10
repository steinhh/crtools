# ftools

## C-based local image filters for cosmic ray detection and removal

`ftools` provides fast local neighborhood filters `fmedian` and `fsigma` that automatically handle both 2D and 3D arrays, implemented as C extensions with optimized sorting networks for small window sizes up to 27 elements.

## Features

- **`fmedian`**: Filtered median computation - automatically works with 2D and 3D arrays
- **`fsigma`**: Local population standard deviation - automatically works with 2D and 3D arrays
- Optional center pixel/voxel exclusion for better outlier detection (default: include center)
- Robust NaN handling
- Correct edge handling (edge pixels/voxels use smaller neighborhoods)
- Full test coverage with unit, edge case, and integration tests

## Requirements

- Python 3.8+
- NumPy >= 1.20
- C compiler toolchain (gcc, clang, or MSVC)

## Standard installation

```bash
pip install .
```

## Building extensions in-place (for development)

If you want to build the C extensions without installing:

```bash
python setup.py build_ext --inplace
```

## Quick Start

```python
import numpy as np
from ftools import fmedian, fsigma

# Works with both 2D and 3D data automatically!

xsize, ysize, zsize = 3, 3, 3  # Example window sizes

# Generate random input data
data_2d = np.random.normal(0.0, 1.0, (100, 200)).astype(np.float64)
data_3d = np.random.normal(0.0, 1.0, (100, 200, 100)).astype(np.float64)

# 2D example
median_filtered_2d = fmedian(data_2d, (xsize, ysize), exclude_center=1)
sigma_map_2d = fsigma(data_2d, (xsize, ysize), exclude_center=1)

# 3D example
median_filtered_3d = fmedian(data_3d, (xsize, ysize, zsize))
sigma_map_3d = fsigma(data_3d, (xsize, ysize, zsize))
```

## Parameters

- `input_data`: Input NumPy array (2D or 3D, will be converted to float64)
- `window_size`: tuple with window sizes. Must be odd positive integers.
- `exclude_center`: Optional, if 1, exclude center pixel/voxel from median calculation; if 0, include it (default: 0)

## Returns

- NumPy array of same shape as input, containing filtered median values (float64)

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

```
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

- Both functions convert input to `float64` for computation
- C implementations provide significant speedup over pure Python/NumPy equivalents
- Edge handling uses appropriate boundary conditions

## Credits

- Blazingly fast sorting networks adapted from [Sorting Networks](https://bertdobbelaere.github.io/sorting_networks.html)
- Many thanks to Claude!
