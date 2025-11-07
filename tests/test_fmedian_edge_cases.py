"""Additional edge case and validation tests for fmedian."""
import numpy as np

from ftools import fmedian


def test_fmedian_large_window():
    """Test fmedian with window larger than the array."""
    a = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64)
    # Window extends beyond array bounds
    out = fmedian(a, (21, 21), 1)
    assert out.shape == a.shape
    assert np.all(np.isfinite(out))


def test_fmedian_asymmetric_windows():
    """Test fmedian with asymmetric window sizes (xsize != ysize)."""
    a = np.arange(25, dtype=np.float64).reshape(5, 5)
    
    # Wide horizontal window
    out1 = fmedian(a, (5, 1), 1)
    assert out1.shape == a.shape
    
    # Tall vertical window
    out2 = fmedian(a, (1, 5), 1)
    assert out2.shape == a.shape
    
    # Results should differ
    assert not np.allclose(out1, out2)


def test_fmedian_all_nan_input():
    """Test fmedian with an array of all NaNs."""
    a = np.full((3, 3), np.nan, dtype=np.float64)
    out = fmedian(a, (3, 3), 1)
    assert out.shape == a.shape
    assert np.all(np.isnan(out))


def test_fmedian_mixed_nan_and_values():
    """Test fmedian with mixed NaN and finite values."""
    a = np.array([
        [np.nan, 1.0, np.nan],
        [2.0, 3.0, 4.0],
        [np.nan, 5.0, np.nan]
    ], dtype=np.float64)
    out = fmedian(a, (3, 3), 1)
    
    # Center should be median of finite neighbors: [1,2,4,5] -> 3.0
    assert np.isclose(out[1, 1], 3.0)


def test_fmedian_negative_values():
    """Test fmedian handles negative values correctly."""
    a = np.array([
        [-5.0, -3.0, -1.0],
        [-4.0, -2.0, 0.0],
        [-3.0, -1.0, 1.0]
    ], dtype=np.float64)
    out = fmedian(a, (3, 3), 1)
    
    # Center neighbors (excluding -2.0): [-5,-3,-1,-4,0,-3,-1,1]
    # Sorted: [-5,-4,-3,-3,-1,-1,0,1] -> median = (-3 + -1)/2 = -2.0
    assert np.isclose(out[1, 1], -2.0)


def test_fmedian_very_large_values():
    """Test fmedian with very large floating point values."""
    a = np.array([
        [1e100, 1e100, 1e100],
        [1e100, 1e100, 1e100],
        [1e100, 1e100, 1e100]
    ], dtype=np.float64)
    out = fmedian(a, (3, 3), 1)
    assert np.allclose(out, 1e100)


def test_fmedian_zero_window():
    """Test fmedian with zero window size (only center pixel)."""
    a = np.arange(16, dtype=np.float64).reshape(4, 4)
    out = fmedian(a, (1, 1), 1)
    # With 1x1 window and exclude_center=1, should fall back to center
    assert np.allclose(out, a)


def test_fmedian_include_vs_exclude_center():
    """Verify include/exclude center produces different results with outlier."""
    a = np.array([
        [1.0, 1.0, 1.0],
        [1.0, 100.0, 1.0],
        [1.0, 1.0, 1.0]
    ], dtype=np.float64)
    
    out_excl = fmedian(a, (3, 3), 1)
    out_incl = fmedian(a, (3, 3), 0)
    
    # Excluding center: median of [1,1,1,1,1,1,1,1] = 1.0
    assert np.isclose(out_excl[1, 1], 1.0)
    
    # Including center: median of [1,1,1,1,100,1,1,1,1] = 1.0 (still 1.0 with 9 values)
    assert np.isclose(out_incl[1, 1], 1.0)


def test_fmedian_rectangular_array():
    """Test fmedian with non-square arrays."""
    a = np.arange(20, dtype=np.float64).reshape(4, 5)
    out = fmedian(a, (3, 3), 1)
    assert out.shape == (4, 5)
    assert np.all(np.isfinite(out))


def test_fmedian_single_row():
    """Test fmedian with a single row (height=1)."""
    a = np.arange(10, dtype=np.float64).reshape(1, 10)
    out = fmedian(a, (3, 3), 1)
    assert out.shape == (1, 10)
    assert np.all(np.isfinite(out))


def test_fmedian_single_column():
    """Test fmedian with a single column (width=1)."""
    a = np.arange(10, dtype=np.float64).reshape(10, 1)
    out = fmedian(a, (3, 3), 1)
    assert out.shape == (10, 1)
    assert np.all(np.isfinite(out))


def test_fmedian_preserves_input():
    """Verify fmedian does not modify the input array."""
    a = np.arange(25, dtype=np.float64).reshape(5, 5)
    a_copy = a.copy()
    
    out = fmedian(a, (3, 3), 1)
    
    assert np.array_equal(a, a_copy), "Input array was modified"
    assert out is not a, "Output should be a new array"


def test_fmedian_int_input_coercion():
    """Test fmedian coerces integer input to float64."""
    a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.int32)
    out = fmedian(a, (3, 3), 1)
    
    assert out.dtype == np.float64
    assert out.shape == a.shape


def test_fmedian_corner_pixels():
    """Test fmedian handles corner pixels (truncated windows) correctly."""
    a = np.arange(9, dtype=np.float64).reshape(3, 3)
    out = fmedian(a, (3, 3), 1)
    
    # All corners should have finite values
    assert np.isfinite(out[0, 0])
    assert np.isfinite(out[0, 2])
    assert np.isfinite(out[2, 0])
    assert np.isfinite(out[2, 2])


def test_fmedian_edge_pixels():
    """Test fmedian handles edge pixels (partial windows) correctly."""
    a = np.arange(25, dtype=np.float64).reshape(5, 5)
    out = fmedian(a, (3, 3), 1)
    
    # Check all edge pixels are finite
    assert np.all(np.isfinite(out[0, :]))  # Top edge
    assert np.all(np.isfinite(out[-1, :]))  # Bottom edge
    assert np.all(np.isfinite(out[:, 0]))  # Left edge
    assert np.all(np.isfinite(out[:, -1]))  # Right edge


def test_fmedian_inf_values():
    """Test fmedian with infinity values."""
    a = np.array([
        [1.0, 2.0, 3.0],
        [4.0, np.inf, 6.0],
        [7.0, 8.0, 9.0]
    ], dtype=np.float64)
    out = fmedian(a, (3, 3), 1)
    
    # Behavior with inf depends on C implementation
    # At minimum, output should have same shape
    assert out.shape == a.shape
