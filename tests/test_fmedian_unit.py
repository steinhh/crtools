import numpy as np
import math

import fmedian_ext


def test_median_excludes_nan_neighbors():
    """Neighbors that are NaN should be ignored when computing the median."""
    arr = np.array([
        [1.0, 2.0, 3.0],
        [4.0, np.nan, 6.0],
        [7.0, 8.0, 9.0]
    ], dtype=np.float64)

    out = np.zeros_like(arr)
    # 3x3 window excluding the center from neighbors
    fmedian_ext.fmedian(arr, out, 1, 1, 1)

    # For the center pixel, neighbors excluding center are [1,2,3,4,6,7,8,9]
    # median = (4 + 6) / 2 = 5.0
    assert out[1, 1] == 5.0


def test_median_with_all_nan_window_writes_nan():
    """If the whole neighborhood (and center) are NaN, output should be NaN."""
    arr = np.array([[np.nan]], dtype=np.float64)
    out = np.zeros_like(arr)

    # Window 1x1, exclude center -> no neighbors; center is NaN -> output should be NaN
    fmedian_ext.fmedian(arr, out, 0, 0, 1)
    assert math.isnan(out[0, 0])
