# 3D Extensions for crtools

This document describes the new 3D extensions (fmedian3 and fsigma3) that have been added to the crtools package.

## Overview

Two new C extensions have been added to provide 3D versions of the existing 2D image filtering operations:

- **fmedian3**: 3D median filtering for volumetric data
- **fsigma3**: 3D standard deviation (sigma) filtering for volumetric data

## Features

### fmedian3

- Computes the median value within a 3D neighborhood around each voxel
- Handles NaN values gracefully (ignores them in calculations)
- Supports excluding the center voxel from the calculation
- Window sizes can be different in x, y, and z dimensions (but must be odd)
- Robust outlier detection and removal in 3D volumes

### fsigma3

- Computes the population standard deviation within a 3D neighborhood
- Useful for detecting areas of high local variation in 3D data
- Handles NaN values gracefully (ignores them in calculations)  
- Supports excluding the center voxel from the calculation
- Window sizes can be different in x, y, and z dimensions (but must be odd)

## File Structure

New directories and files added:

```text
src/crtools/
??? fmedian3/
?   ??? __init__.py              # Python interface for fmedian3
?   ??? fmedian3_ext.c           # C extension implementation
?   ??? example_fmedian3.py      # Usage example
?   ??? test_fmedian3.py         # Test suite
??? fsigma3/
?   ??? __init__.py              # Python interface for fsigma3
?   ??? fsigma3_ext.c            # C extension implementation
?   ??? example_fsigma3.py       # Usage example
?   ??? test_fsigma3.py          # Test suite
??? __init__.py                  # Updated to export 3D functions
```

Modified files:

- `setup.py`: Added the new extensions to the build configuration
- `src/crtools/__init__.py`: Added imports for fmedian3 and fsigma3

## Usage

### Basic Usage

```python
import numpy as np
from crtools import fmedian3, fsigma3

# Create a 3D array
data = np.random.random((10, 10, 10)).astype(np.float64)

# Apply 3D median filter with 3x3x3 window
filtered = fmedian3(data, 3, 3, 3, exclude_center=1)

# Compute local standard deviation with 3x3x3 window  
sigma = fsigma3(data, 3, 3, 3, exclude_center=1)
```

### Function Signatures

```python
def fmedian3(input_array, xsize: int, ysize: int, zsize: int, exclude_center: int) -> np.ndarray:
    """
    Compute 3D filtered median.
    
    Parameters:
    - input_array: 3D numpy array (will be converted to float64)
    - xsize: Window width (must be odd, positive integer)
    - ysize: Window height (must be odd, positive integer) 
    - zsize: Window depth (must be odd, positive integer)
    - exclude_center: If 1, exclude center voxel; if 0, include it
    
    Returns:
    - 3D numpy array of same shape as input, dtype=float64
    """

def fsigma3(input_array, xsize: int, ysize: int, zsize: int, exclude_center: int) -> np.ndarray:
    """
    Compute 3D filtered standard deviation.
    
    Parameters:
    - input_array: 3D numpy array (will be converted to float64)
    - xsize: Window width (must be odd, positive integer)
    - ysize: Window height (must be odd, positive integer)
    - zsize: Window depth (must be odd, positive integer)  
    - exclude_center: If 1, exclude center voxel; if 0, include it
    
    Returns:
    - 3D numpy array of same shape as input, dtype=float64
    """
```

### Parameter Validation

Both functions include comprehensive parameter validation:

- Window sizes must be positive odd integers
- Input must be a 3D array
- All parameters are required

### NaN Handling

Both functions handle NaN values robustly:

- NaN values in the input are ignored during calculations
- If all values in a neighborhood are NaN, the result is NaN (fsigma3) or the center value (fmedian3)
- Edge cases are handled gracefully

## Examples

Run the provided examples to see the functions in action:

```bash
# Run fmedian3 example
python -m src.crtools.fmedian3.example_fmedian3

# Run fsigma3 example  
python -m src.crtools.fsigma3.example_fsigma3
```

## Testing

Comprehensive test suites are provided for both functions:

```bash
# Test fmedian3
python -m pytest src/crtools/fmedian3/test_fmedian3.py -v

# Test fsigma3
python -m pytest src/crtools/fsigma3/test_fsigma3.py -v

# Test all extensions
python -m pytest tests/ src/crtools/*/test_*.py -v
```

## Building

To build the new extensions:

```bash
python setup.py build_ext --inplace
```

## Performance Characteristics

- Both functions are implemented in C for high performance
- Memory usage scales with window size: O(xsize × ysize × zsize) per voxel
- Time complexity: O(N × W × log W) where N is the number of voxels and W is the window size
- Efficient handling of boundary conditions using array bounds checking

## Use Cases

### fmedian3 Use Cases

- 3D noise reduction in volumetric datasets
- Outlier removal in medical imaging (CT, MRI)
- Edge-preserving smoothing of 3D point clouds
- Preprocessing for 3D computer vision applications

### fsigma3 Use Cases

- Feature detection in volumetric data
- Texture analysis in 3D datasets
- Quality control in manufacturing (3D scanning)
- Identifying regions of interest in scientific volumes
- Edge detection in 3D images
