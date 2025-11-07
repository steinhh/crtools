"""Top level package for crtools.

Expose unified function names at package level so users can call
`fmedian` and `fsigma` with either 2D or 3D arrays.
"""
from .fmedian import fmedian as _fmedian2d
from .fsigma import fsigma as _fsigma2d
from .fmedian3 import fmedian3 as _fmedian3d
from .fsigma3 import fsigma3 as _fsigma3d


def fmedian(input_array, xsize: int, ysize: int, zsize: int | None = None, exclude_center: int = 0):
    """Compute filtered median for 2D or 3D arrays.

    Automatically dispatches to the appropriate implementation based on input dimensionality.

    Parameters:
    - input_array: 2D or 3D numpy array
    - xsize: Full window width (must be odd)
    - ysize: Full window height (must be odd)
    - zsize: Full window depth (must be odd, required for 3D arrays)
    - exclude_center: Whether to exclude center pixel/voxel (default: 0)

    Returns:
    - Filtered array of same shape as input
    """
    import numpy as np

    arr = np.asarray(input_array)

    if arr.ndim == 2:
        # For 2D arrays, zsize should not be provided
        # However, for backward compatibility, check if zsize was passed as exclude_center
        if zsize is not None:
            # Backward compatibility: if we got zsize for 2D array, treat it as exclude_center
            if isinstance(zsize, int) and zsize in [0, 1]:
                exclude_center = zsize
                zsize = None
            else:
                raise ValueError("zsize parameter not allowed for 2D arrays")
        
        from .fmedian import fmedian as fmedian2d
        return fmedian2d(arr, xsize, ysize, exclude_center)
    
    elif arr.ndim == 3:
        if zsize is None:
            raise ValueError("zsize parameter required for 3D arrays")
        
        from .fmedian3 import fmedian3
        return fmedian3(arr, xsize, ysize, zsize, exclude_center)
    
    else:
        raise ValueError(f"Input array must be 2D or 3D, got {arr.ndim}D")
def fsigma(input_array, xsize: int, ysize: int, zsize: int | None = None, exclude_center: int = 0):
    """Compute local population standard deviation for 2D or 3D arrays.

    Automatically dispatches to the appropriate implementation based on input dimensionality.

    Parameters:
    - input_array: 2D or 3D numpy array
    - xsize: Full window width (must be odd)
    - ysize: Full window height (must be odd)
    - zsize: Full window depth (must be odd, required for 3D arrays)
    - exclude_center: Whether to exclude center pixel/voxel (default: 0)

    Returns:
    - Array of local standard deviations, same shape as input
    """
    import numpy as np

    arr = np.asarray(input_array)

    if arr.ndim == 2:
        # For 2D arrays, zsize should not be provided
        # However, for backward compatibility, check if zsize was passed as exclude_center
        if zsize is not None:
            # Backward compatibility: if we got zsize for 2D array, treat it as exclude_center
            if isinstance(zsize, int) and zsize in [0, 1]:
                exclude_center = zsize
                zsize = None
            else:
                raise ValueError("zsize parameter not allowed for 2D arrays")
        
        from .fsigma import fsigma as fsigma2d
        return fsigma2d(arr, xsize, ysize, exclude_center)
    
    elif arr.ndim == 3:
        if zsize is None:
            raise ValueError("zsize parameter required for 3D arrays")
        
        from .fsigma3 import fsigma3
        return fsigma3(arr, xsize, ysize, zsize, exclude_center)
    
    else:
        raise ValueError(f"Input array must be 2D or 3D, got {arr.ndim}D")
# Keep the specific implementations available for direct access if needed
fmedian2d = _fmedian2d
fsigma2d = _fsigma2d
fmedian3d = _fmedian3d
fsigma3d = _fsigma3d

__version__ = "1.0.0"
__all__ = ["fmedian", "fsigma", "fmedian2d", "fsigma2d", "fmedian3d", "fsigma3d"]
