#!/usr/bin/env python3
"""
Test script to verify the fmedian3_ext module functionality.
"""

import numpy as np
import sys
import pytest

try:
    # Import the function directly from the crtools package
    from crtools import fmedian3d as fmedian3
except ImportError:
    print("ERROR: Could not import crtools.fmedian3d function.")
    print("Please build the extension first (create fmedian3_ext shared object) or install the package.")
    sys.exit(1)

def test_basic_functionality():
    """Test basic functionality with a simple 3D array."""
    print("Test 1: Basic functionality...")
    
    # Create simple 3x3x3 array
    input_arr = np.arange(1, 28, dtype=np.float64).reshape((3, 3, 3))
    
    # Apply filter with 3x3x3 window (includes immediate neighbors)
    out = fmedian3(input_arr, 3, 3, 3, 1)

    print("  Input array shape:", input_arr.shape)
    print("  Input array:")
    print(input_arr)
    print("\n  Output array shape:", out.shape)
    print("  Output array:")
    print(out)
    assert out.shape == input_arr.shape and out.dtype == np.float64
    print("  \u2713 Basic functionality test passed")

def test_data_types():
    """Test that data type checking works correctly."""
    print("\nTest 2: Data type validation...")
    
    # Test with correct types
    input_arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], dtype=np.float64)
    out = fmedian3(input_arr, 3, 3, 3, 1)
    assert out.dtype == np.float64
    print("  \u2713 Correct data types accepted")

def test_window_sizes():
    """Test various window sizes."""
    print("\nTest 3: Window sizes...")
    
    input_arr = np.ones((5, 5, 5), dtype=np.float64)
    
    # Test 1x1x1 window (should fall back to original values when center excluded)
    out = fmedian3(input_arr, 1, 1, 1, 1)
    assert np.allclose(out, input_arr)  # Falls back to center value when no neighbors
    
    # Test 1x1x1 window with center included
    out = fmedian3(input_arr, 1, 1, 1, 0)
    assert np.allclose(out, input_arr)  # Should match input
    
    # Test 3x3x3 window
    out = fmedian3(input_arr, 3, 3, 3, 1)
    assert np.allclose(out, np.ones_like(input_arr))  # All neighbors are 1
    
    # Test 5x5x5 window
    out = fmedian3(input_arr, 5, 5, 5, 1)
    assert np.allclose(out, np.ones_like(input_arr))  # All neighbors are 1
    
    print("  \u2713 Window sizes test passed")

def test_outlier_removal():
    """Test outlier detection/removal capability."""
    print("\nTest 4: Outlier removal...")
    
    # Create array with outlier
    input_arr = np.ones((5, 5, 5), dtype=np.float64)
    input_arr[2, 2, 2] = 100.0  # Center outlier
    
    # Filter with exclude_center=1 (should remove outlier influence from neighbors)
    out = fmedian3(input_arr, 3, 3, 3, 1)
    
    # The outlier position should get the median of its neighbors (which are all 1)
    assert np.isclose(out[2, 2, 2], 1.0)
    
    # Other positions should also be 1 (neighbors are all 1)
    assert np.allclose(out, np.ones_like(input_arr))
    
    print("  \u2713 Outlier removal test passed")

def test_nan_handling():
    """Test handling of NaN values."""
    print("\nTest 5: NaN handling...")
    
    # Create array with NaN
    input_arr = np.ones((3, 3, 3), dtype=np.float64)
    input_arr[0, 0, 0] = np.nan
    input_arr[1, 1, 1] = np.nan  # center
    
    # Filter should ignore NaN values
    out = fmedian3(input_arr, 3, 3, 3, 1)
    
    # Result should not contain NaN in most positions (except where all neighbors are NaN)
    assert not np.isnan(out[2, 2, 2])  # This position has valid neighbors
    
    print("  \u2713 NaN handling test passed")

def test_parameter_validation():
    """Test parameter validation."""
    print("\nTest 6: Parameter validation...")
    
    input_arr = np.ones((3, 3, 3), dtype=np.float64)
    
    # Test that window sizes must be odd
    with pytest.raises(ValueError, match="must be an odd number"):
        fmedian3(input_arr, 2, 3, 3, 1)  # even xsize
    
    with pytest.raises(ValueError, match="must be an odd number"):
        fmedian3(input_arr, 3, 2, 3, 1)  # even ysize
    
    with pytest.raises(ValueError, match="must be an odd number"):
        fmedian3(input_arr, 3, 3, 2, 1)  # even zsize
    
    # Test that window sizes must be positive
    with pytest.raises(ValueError, match="must be positive"):
        fmedian3(input_arr, 0, 3, 3, 1)
    
    with pytest.raises(ValueError, match="must be positive"):
        fmedian3(input_arr, -1, 3, 3, 1)
    
    # Test that input must be 3D
    input_2d = np.ones((3, 3), dtype=np.float64)
    with pytest.raises(ValueError, match="must be 3-dimensional"):
        fmedian3(input_2d, 3, 3, 3, 1)
    
    print("  \u2713 Parameter validation test passed")

def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\nTest 7: Edge cases...")
    
    # Very small array
    input_arr = np.array([[[1.0]]], dtype=np.float64)
    out = fmedian3(input_arr, 1, 1, 1, 0)  # Must include center for 1x1x1 array
    assert np.isclose(out[0, 0, 0], 1.0)
    
    # All NaN array
    input_arr = np.full((2, 2, 2), np.nan, dtype=np.float64)
    out = fmedian3(input_arr, 3, 3, 3, 1)
    assert np.all(np.isnan(out))  # Should preserve NaN
    
    print("  \u2713 Edge cases test passed")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing fmedian3 extension module")
    print("=" * 60)
    
    test_basic_functionality()
    test_data_types()
    test_window_sizes()
    test_outlier_removal()
    test_nan_handling()
    test_parameter_validation()
    test_edge_cases()
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)