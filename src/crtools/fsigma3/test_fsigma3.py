#!/usr/bin/env python3
"""
Test script to verify the fsigma3_ext module functionality.
"""

import numpy as np
import sys
import pytest

try:
    # Prefer the new package import path
    from crtools import fsigma3
except ImportError:
    print("ERROR: Could not import crtools.fsigma3 module.")
    print("Please build the extension first (create fsigma3_ext shared object) or install the package.")
    sys.exit(1)

def test_basic_functionality():
    """Test basic functionality with a simple 3D array."""
    print("Test 1: Basic functionality...")
    
    # Create simple 3x3x3 array with varying values
    input_arr = np.arange(1, 28, dtype=np.float64).reshape((3, 3, 3))
    
    # Apply filter with 3x3x3 window
    out = fsigma3(input_arr, 3, 3, 3, 1)

    print("  Input array shape:", input_arr.shape)
    print("  Output array shape:", out.shape)
    assert out.shape == input_arr.shape and out.dtype == np.float64
    print("  \u2713 Basic functionality test passed")

def test_data_types():
    """Test that data type checking works correctly."""
    print("\nTest 2: Data type validation...")
    
    # Test with correct types
    input_arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], dtype=np.float64)
    out = fsigma3(input_arr, 3, 3, 3, 1)
    assert out.dtype == np.float64
    print("  \u2713 Correct data types accepted")

def test_uniform_array():
    """Test with uniform array (sigma should be zero)."""
    print("\nTest 3: Uniform array...")
    
    # Create uniform array
    input_arr = np.ones((5, 5, 5), dtype=np.float64)
    
    # Apply filter - should get zero sigma everywhere
    out = fsigma3(input_arr, 3, 3, 3, 1)
    
    # All values should be zero (no variation)
    assert np.allclose(out, np.zeros_like(input_arr))
    print("  \u2713 Uniform array test passed")

def test_high_variance_detection():
    """Test that high variance areas are detected."""
    print("\nTest 4: High variance detection...")
    
    # Create array with outlier to create high variance
    input_arr = np.ones((5, 5, 5), dtype=np.float64)
    input_arr[2, 2, 2] = 100.0  # Create high variance at center
    
    # Filter with exclude_center=0 (include outlier in calculation)
    out_with_center = fsigma3(input_arr, 3, 3, 3, 0)
    
    # Filter with exclude_center=1 (exclude outlier from calculation)
    out_without_center = fsigma3(input_arr, 3, 3, 3, 1)
    
    # The center position should have higher sigma when outlier is included
    center_sigma_with = out_with_center[2, 2, 2]
    center_sigma_without = out_without_center[2, 2, 2]
    
    print(f"  Center sigma (with outlier): {center_sigma_with:.3f}")
    print(f"  Center sigma (without outlier): {center_sigma_without:.3f}")
    
    # When outlier is included, sigma should be much higher
    assert center_sigma_with > center_sigma_without
    assert center_sigma_with > 10.0  # Should be significantly higher
    
    print("  \u2713 High variance detection test passed")

def test_nan_handling():
    """Test handling of NaN values."""
    print("\nTest 5: NaN handling...")
    
    # Create array with some NaN values
    input_arr = np.ones((3, 3, 3), dtype=np.float64)
    input_arr[0, 0, 0] = np.nan
    input_arr[1, 1, 1] = 2.0  # Add some variation
    
    # Filter should ignore NaN values
    out = fsigma3(input_arr, 3, 3, 3, 1)
    
    # Result should not contain unexpected NaN values in most positions
    assert not np.isnan(out[2, 2, 2])  # This position has valid neighbors
    
    print("  \u2713 NaN handling test passed")

def test_parameter_validation():
    """Test parameter validation."""
    print("\nTest 6: Parameter validation...")
    
    input_arr = np.ones((3, 3, 3), dtype=np.float64)
    
    # Test that window sizes must be odd
    with pytest.raises(ValueError, match="must be an odd number"):
        fsigma3(input_arr, 2, 3, 3, 1)  # even xsize
    
    with pytest.raises(ValueError, match="must be an odd number"):
        fsigma3(input_arr, 3, 2, 3, 1)  # even ysize
    
    with pytest.raises(ValueError, match="must be an odd number"):
        fsigma3(input_arr, 3, 3, 2, 1)  # even zsize
    
    # Test that window sizes must be positive
    with pytest.raises(ValueError, match="must be positive"):
        fsigma3(input_arr, 0, 3, 3, 1)
    
    with pytest.raises(ValueError, match="must be positive"):
        fsigma3(input_arr, -1, 3, 3, 1)
    
    # Test that input must be 3D
    input_2d = np.ones((3, 3), dtype=np.float64)
    with pytest.raises(ValueError, match="must be 3-dimensional"):
        fsigma3(input_2d, 3, 3, 3, 1)
    
    print("  \u2713 Parameter validation test passed")

def test_window_sizes():
    """Test various window sizes."""
    print("\nTest 7: Window sizes...")
    
    # Create array with some variation
    rng = np.random.default_rng(42)  # Fixed seed for reproducibility
    input_arr = rng.random((7, 7, 7)).astype(np.float64)
    
    # Test 1x1x1 window (should be zero everywhere when center excluded)
    out = fsigma3(input_arr, 1, 1, 1, 1)
    assert np.allclose(out, np.zeros_like(input_arr))
    
    # Test 1x1x1 window with center included (should be zero - only one value)
    out = fsigma3(input_arr, 1, 1, 1, 0)
    assert np.allclose(out, np.zeros_like(input_arr))
    
    # Test larger windows
    out3 = fsigma3(input_arr, 3, 3, 3, 1)
    out5 = fsigma3(input_arr, 5, 5, 5, 1)
    
    # Larger windows should generally have different results
    assert out3.shape == out5.shape == input_arr.shape
    
    print("  \u2713 Window sizes test passed")

def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\nTest 8: Edge cases...")
    
    # Very small array
    input_arr = np.array([[[1.0, 2.0]]], dtype=np.float64)
    out = fsigma3(input_arr, 1, 1, 1, 0)
    # Should have zero sigma (only one value in each neighborhood)
    assert np.allclose(out, np.zeros_like(input_arr))
    
    # All NaN array
    input_arr = np.full((2, 2, 2), np.nan, dtype=np.float64)
    out = fsigma3(input_arr, 3, 3, 3, 1)
    # Should return 0.0 when no valid neighbors
    assert np.allclose(out, np.zeros_like(input_arr), equal_nan=True)
    
    print("  \u2713 Edge cases test passed")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing fsigma3 extension module")
    print("=" * 60)
    
    test_basic_functionality()
    test_data_types()
    test_uniform_array()
    test_high_variance_detection()
    test_nan_handling()
    test_parameter_validation()
    test_window_sizes()
    test_edge_cases()
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)