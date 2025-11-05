"""Additional edge case and validation tests for fsigma."""
import numpy as np

from crtools import fsigma


def test_fsigma_large_window():
    """Test fsigma with window larger than the array."""
    a = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64)
    # Window extends beyond array bounds
    out = fsigma(a, 10, 10, 1)
    assert out.shape == a.shape
    assert np.all(np.isfinite(out))
    assert np.all(out >= 0.0)


def test_fsigma_asymmetric_windows():
    """Test fsigma with asymmetric window sizes (xsize != ysize)."""
    a = np.arange(25, dtype=np.float64).reshape(5, 5)
    
    # Wide horizontal window
    out1 = fsigma(a, 2, 0, 1)
    assert out1.shape == a.shape
    
    # Tall vertical window
    out2 = fsigma(a, 0, 2, 1)
    assert out2.shape == a.shape
    
    # Results should differ
    assert not np.allclose(out1, out2)


def test_fsigma_all_nan_input():
    """Test fsigma with an array of all NaNs."""
    a = np.full((3, 3), np.nan, dtype=np.float64)
    out = fsigma(a, 1, 1, 1)
    assert out.shape == a.shape
    # All NaN neighborhood should produce NaN or 0.0 depending on implementation
    # At minimum, output should have consistent behavior


def test_fsigma_mixed_nan_and_values():
    """Test fsigma with mixed NaN and finite values."""
    a = np.array([
        [np.nan, 1.0, np.nan],
        [2.0, 3.0, 4.0],
        [np.nan, 5.0, np.nan]
    ], dtype=np.float64)
    out = fsigma(a, 1, 1, 1)
    
    # Center sigma computed from finite neighbors only
    assert np.isfinite(out[1, 1])
    assert out[1, 1] >= 0.0


def test_fsigma_negative_values():
    """Test fsigma handles negative values correctly (sigma always positive)."""
    a = np.array([
        [-5.0, -3.0, -1.0],
        [-4.0, -2.0, 0.0],
        [-3.0, -1.0, 1.0]
    ], dtype=np.float64)
    out = fsigma(a, 1, 1, 1)
    
    # Sigma must be non-negative
    assert np.all(out >= 0.0)
    assert np.all(np.isfinite(out))


def test_fsigma_very_large_values():
    """Test fsigma with very large floating point values."""
    a = np.array([
        [1e100, 1e100, 1e100],
        [1e100, 1e100, 1e100],
        [1e100, 1e100, 1e100]
    ], dtype=np.float64)
    out = fsigma(a, 1, 1, 1)
    # All same values -> sigma should be 0
    assert np.allclose(out, 0.0)


def test_fsigma_zero_window():
    """Test fsigma with zero window size (only center pixel)."""
    a = np.arange(16, dtype=np.float64).reshape(4, 4)
    out = fsigma(a, 0, 0, 1)
    # With 1x1 window and exclude_center=1, no values -> sigma = 0
    assert np.allclose(out, 0.0)


def test_fsigma_include_vs_exclude_center():
    """Verify include/exclude center produces different results with outlier."""
    a = np.array([
        [1.0, 1.0, 1.0],
        [1.0, 100.0, 1.0],
        [1.0, 1.0, 1.0]
    ], dtype=np.float64)
    
    out_excl = fsigma(a, 1, 1, 1)
    out_incl = fsigma(a, 1, 1, 0)
    
    # Excluding center: sigma of [1,1,1,1,1,1,1,1] = 0.0
    assert np.isclose(out_excl[1, 1], 0.0)
    
    # Including center: sigma of [1,1,1,1,100,1,1,1,1] > 0
    assert out_incl[1, 1] > 0.0


def test_fsigma_rectangular_array():
    """Test fsigma with non-square arrays."""
    a = np.arange(20, dtype=np.float64).reshape(4, 5)
    out = fsigma(a, 1, 1, 1)
    assert out.shape == (4, 5)
    assert np.all(np.isfinite(out))
    assert np.all(out >= 0.0)


def test_fsigma_single_row():
    """Test fsigma with a single row (height=1)."""
    a = np.arange(10, dtype=np.float64).reshape(1, 10)
    out = fsigma(a, 1, 1, 1)
    assert out.shape == (1, 10)
    assert np.all(np.isfinite(out))


def test_fsigma_single_column():
    """Test fsigma with a single column (width=1)."""
    a = np.arange(10, dtype=np.float64).reshape(10, 1)
    out = fsigma(a, 1, 1, 1)
    assert out.shape == (10, 1)
    assert np.all(np.isfinite(out))


def test_fsigma_preserves_input():
    """Verify fsigma does not modify the input array."""
    a = np.arange(25, dtype=np.float64).reshape(5, 5)
    a_copy = a.copy()
    
    out = fsigma(a, 1, 1, 1)
    
    assert np.array_equal(a, a_copy), "Input array was modified"
    assert out is not a, "Output should be a new array"


def test_fsigma_int_input_coercion():
    """Test fsigma coerces integer input to float64."""
    a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.int32)
    out = fsigma(a, 1, 1, 1)
    
    assert out.dtype == np.float64
    assert out.shape == a.shape


def test_fsigma_corner_pixels():
    """Test fsigma handles corner pixels (truncated windows) correctly."""
    a = np.arange(9, dtype=np.float64).reshape(3, 3)
    out = fsigma(a, 1, 1, 1)
    
    # All corners should have finite, non-negative values
    assert np.isfinite(out[0, 0]) and out[0, 0] >= 0.0
    assert np.isfinite(out[0, 2]) and out[0, 2] >= 0.0
    assert np.isfinite(out[2, 0]) and out[2, 0] >= 0.0
    assert np.isfinite(out[2, 2]) and out[2, 2] >= 0.0


def test_fsigma_edge_pixels():
    """Test fsigma handles edge pixels (partial windows) correctly."""
    a = np.arange(25, dtype=np.float64).reshape(5, 5)
    out = fsigma(a, 1, 1, 1)
    
    # Check all edge pixels are finite and non-negative
    assert np.all(np.isfinite(out[0, :])) and np.all(out[0, :] >= 0.0)  # Top
    assert np.all(np.isfinite(out[-1, :])) and np.all(out[-1, :] >= 0.0)  # Bottom
    assert np.all(np.isfinite(out[:, 0])) and np.all(out[:, 0] >= 0.0)  # Left
    assert np.all(np.isfinite(out[:, -1])) and np.all(out[:, -1] >= 0.0)  # Right


def test_fsigma_uniform_array():
    """Test fsigma with uniform values returns zero sigma."""
    a = np.full((5, 5), 42.0, dtype=np.float64)
    out = fsigma(a, 1, 1, 1)
    assert np.allclose(out, 0.0)


def test_fsigma_two_values():
    """Test fsigma with exactly two distinct values."""
    a = np.array([
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0]
    ], dtype=np.float64)
    out = fsigma(a, 1, 1, 1)
    
    # Center neighbors (excluding 0.0): [0,1,0,1,1,0,1,0]
    # Population std of alternating 0/1 should be 0.5
    assert out[1, 1] > 0.0


def test_fsigma_numerical_precision():
    """Test fsigma maintains numerical precision with small differences."""
    a = np.array([
        [1.0, 1.0001, 1.0],
        [1.0001, 1.0, 1.0001],
        [1.0, 1.0001, 1.0]
    ], dtype=np.float64)
    out = fsigma(a, 1, 1, 1)
    
    # Should detect small variance
    assert out[1, 1] > 0.0
    assert out[1, 1] < 0.001  # But should be small


def test_fsigma_inf_values():
    """Test fsigma with infinity values."""
    a = np.array([
        [1.0, 2.0, 3.0],
        [4.0, np.inf, 6.0],
        [7.0, 8.0, 9.0]
    ], dtype=np.float64)
    out = fsigma(a, 1, 1, 1)
    
    # Behavior with inf depends on C implementation
    # At minimum, output should have same shape
    assert out.shape == a.shape
