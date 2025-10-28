#!/usr/bin/env python3
"""
Test script to verify the fsigma_ext module functionality.
"""

import numpy as np
import sys
import pytest

try:
    import fsigma_ext
except ImportError:
    print("ERROR: Could not import fsigma_ext module.")
    print("Please build the extension first using: python setup.py build_ext --inplace")
    sys.exit(1)

def test_basic_functionality():
    """Test basic functionality with a simple array."""
    print("Test 1: Basic functionality...")
    
    # Create simple 5x5 array
    input_arr = np.array([
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25]
    ], dtype=np.float64)
    
    output_arr = np.zeros_like(input_arr, dtype=np.float64)
    
    # Apply fsigma with large window (includes all neighbors)
    fsigma_ext.fsigma(input_arr, output_arr, 1, 1, 1)

    print("  Input array:")
    print(input_arr)
    print("\n  Output array (local sigma):")
    print(output_arr)

    # Basic checks: output has same shape and non-negative finite values
    assert output_arr.shape == input_arr.shape, "output shape mismatch"
    assert np.all(np.isfinite(output_arr)), "output contains non-finite values"
    assert not np.any(output_arr < 0), "sigma must be non-negative"

    print("  ? Basic functionality test passed")

def test_data_types():
    """Test that data type checking works correctly."""
    print("\nTest 2: Data type validation...")
    
    # Test with correct types
    input_arr = np.array([[1, 2], [3, 4]], dtype=np.float64)
    output_arr = np.zeros_like(input_arr, dtype=np.float64)
    fsigma_ext.fsigma(input_arr, output_arr, 1, 1, 1)
    print("  ? Correct data types accepted")

    # Test with wrong input type (should fail)
    with pytest.raises(TypeError):
        wrong_input = np.array([[1, 2], [3, 4]], dtype=np.float32)
        fsigma_ext.fsigma(wrong_input, output_arr, 1, 1, 1)
    print("  ? Wrong input type correctly rejected")

    # Test with wrong output type (should fail)
    with pytest.raises(TypeError):
        wrong_output = np.array([[1, 2], [3, 4]], dtype=np.float32)
        fsigma_ext.fsigma(input_arr, wrong_output, 1, 1, 1)
    print("  ? Wrong output type correctly rejected")

def test_array_dimensions():
    """Test array dimension validation."""
    print("\nTest 3: Array dimension validation...")
    
    # Test with matching dimensions
    input_arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
    output_arr = np.zeros((2, 3), dtype=np.float64)
    fsigma_ext.fsigma(input_arr, output_arr, 1, 1, 1)
    print("  ? Matching dimensions accepted")

    # Test with mismatched dimensions (should fail)
    with pytest.raises(ValueError):
        wrong_output = np.zeros((3, 3), dtype=np.float64)
        fsigma_ext.fsigma(input_arr, wrong_output, 1, 1, 1)
    print("  ? Mismatched dimensions correctly rejected")

    # Test with 1D array (should fail)
    with pytest.raises(ValueError):
        input_1d = np.array([1, 2, 3], dtype=np.float64)
        output_1d = np.zeros(3, dtype=np.float64)
        fsigma_ext.fsigma(input_1d, output_1d, 1, 1, 1)
    print("  ? 1D arrays correctly rejected")

def test_threshold_filtering():
    """Test that threshold filtering works correctly."""
    print("\nTest 4: Threshold filtering...")
    
    # Create array with an outlier
    input_arr = np.array([
        [10, 10, 10],
        [10, 100, 10],  # 100 is outlier
        [10, 10, 10]
    ], dtype=np.float64)
    
    # For sigma, just compute and ensure results are finite and non-negative
    output = np.zeros_like(input_arr, dtype=np.float64)
    fsigma_ext.fsigma(input_arr, output, 1, 1, 1)

    print("  Input array:")
    print(input_arr)
    print("\n  Sigma output:")
    print(output)

    assert np.all(np.isfinite(output)) and not np.any(output < 0), "invalid sigma output"
    print("  ? Sigma computation produced valid (finite, non-negative) values")

def test_window_sizes():
    """Test different window sizes."""
    print("\nTest 5: Different window sizes...")
    
    input_arr = np.array([
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25]
    ], dtype=np.float64)
    
    # Test with xsize=0, ysize=0 (only the pixel itself) => sigma should be 0
    output_0 = np.zeros_like(input_arr, dtype=np.float64)
    fsigma_ext.fsigma(input_arr, output_0, 0, 0, 1)

    assert np.allclose(output_0, 0.0), "Window size (1x1) produced non-zero sigma"
    print("  ? Window size (1x1) produces zero sigma")

    # Test with xsize=2, ysize=2 (5x5 window)
    output_2 = np.zeros_like(input_arr, dtype=np.float64)
    fsigma_ext.fsigma(input_arr, output_2, 2, 2, 1)
    print("  ? Window size (5x5) produced sigma values")

def test_center_exclusion():
    """Test that the center pixel is excluded from the median calculation."""
    print("\nTest 7: Center exclusion from median...")

    # Construct a 3x3 array where the center is an outlier
    input_arr = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 999.0, 6.0],
        [7.0, 8.0, 9.0]
    ], dtype=np.float64)

    output_arr = np.zeros_like(input_arr, dtype=np.float64)

    # Apply fsigma with a 3x3 window (xsize=1, ysize=1)
    # First compute with center included (exclude_center=0)
    fsigma_ext.fsigma(input_arr, output_arr, 1, 1, 0)
    output_included = output_arr.copy()

    # Now compute excluding the center from the neighborhood
    fsigma_ext.fsigma(input_arr, output_arr, 1, 1, 1)
    output_excluded = output_arr.copy()

    print("  Input array:")
    print(input_arr)
    print("\n  Output array:")
    print(output_arr)

    # Neighbors excluding the center are [1,2,3,4,6,7,8,9]; with the extreme center value
    # present, including it should increase local sigma
    sigma_with = output_included[1, 1]
    sigma_without = output_excluded[1, 1]

    print(f"  sigma with center: {sigma_with:.3f}, without center: {sigma_without:.3f}")
    assert sigma_with > sigma_without, "Center exclusion did not reduce sigma"
    print("  ? Center exclusion reduces sigma as expected")

def test_edge_cases():
    """Test edge cases like small arrays and boundary conditions."""
    print("\nTest 6: Edge cases...")
    
    # Test with 1x1 array
    input_1x1 = np.array([[42]], dtype=np.float64)
    output_1x1 = np.zeros_like(input_1x1, dtype=np.float64)
    fsigma_ext.fsigma(input_1x1, output_1x1, 1, 1, 1)
    
    # With only one pixel and excluding the center, sigma should be 0.0
    assert np.isclose(output_1x1[0, 0], 0.0), f"Expected sigma 0.0, got {output_1x1[0,0]}"
    print("  ? 1x1 array produced zero sigma")

    # Test with 2x2 array
    input_2x2 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    output_2x2 = np.zeros_like(input_2x2, dtype=np.float64)
    fsigma_ext.fsigma(input_2x2, output_2x2, 1, 1, 1)
    assert np.all(np.isfinite(output_2x2)) and not np.any(output_2x2 < 0), "2x2 produced invalid sigma values"
    print("  ? 2x2 array handled correctly")

# Note: keep the main() script entry for running as a script; pytest will collect the
# `test_` functions above and treat assertions as test failures.

# Tests are collected by pytest via the `test_` prefixed functions above. The
# previous `main()` script harness (which executed tests and returned numeric
# exit codes) was removed to make these files pure pytest modules.
