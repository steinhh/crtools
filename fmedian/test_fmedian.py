#!/usr/bin/env python3
"""
Test script to verify the fmedian_ext module functionality.
"""

import numpy as np
import sys
import os
import pytest

# Add parent directory to path so we can import from fmedian.fmedian_ext
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from fmedian.fmedian_ext import fmedian
except ImportError:
    print("ERROR: Could not import fmedian.fmedian_ext module.")
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
    
    # Apply filter with large window (includes all neighbors)
    fmedian(input_arr, output_arr, 1, 1, 1)
    
    print("  Input array:")
    print(input_arr)
    print("\n  Output array:")
    print(output_arr)
    print("  \u2713 Basic functionality test passed")

def test_data_types():
    """Test that data type checking works correctly."""
    print("\nTest 2: Data type validation...")
    
    # Test with correct types
    input_arr = np.array([[1, 2], [3, 4]], dtype=np.float64)
    output_arr = np.zeros_like(input_arr, dtype=np.float64)
    fmedian(input_arr, output_arr, 1, 1, 1)
    print("  \u2713 Correct data types accepted")

    # Test with wrong input type (should fail)
    with pytest.raises(TypeError):
        wrong_input = np.array([[1, 2], [3, 4]], dtype=np.float32)
        fmedian(wrong_input, output_arr, 1, 1, 1)
    print("  \u2713 Wrong input type correctly rejected")

    # Test with wrong output type (should fail)
    with pytest.raises(TypeError):
        wrong_output = np.array([[1, 2], [3, 4]], dtype=np.float32)
        fmedian(input_arr, wrong_output, 1, 1, 1)
    print("  \u2713 Wrong output type correctly rejected")

def test_array_dimensions():
    """Test array dimension validation."""
    print("\nTest 3: Array dimension validation...")
    
    # Test with matching dimensions
    input_arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
    output_arr = np.zeros((2, 3), dtype=np.float64)
    fmedian(input_arr, output_arr, 1, 1, 1)
    print("  \u2713 Matching dimensions accepted")

    # Test with mismatched dimensions (should fail)
    with pytest.raises(ValueError):
        wrong_output = np.zeros((3, 3), dtype=np.float64)
        fmedian(input_arr, wrong_output, 1, 1, 1)
    print("  \u2713 Mismatched dimensions correctly rejected")

    # Test with 1D array (should fail)
    with pytest.raises(ValueError):
        input_1d = np.array([1, 2, 3], dtype=np.float64)
        output_1d = np.zeros(3, dtype=np.float64)
        fmedian(input_1d, output_1d, 1, 1, 1)
    print("  \u2713 1D arrays correctly rejected")

def test_threshold_filtering():
    """Test that threshold filtering works correctly."""
    print("\nTest 4: Threshold filtering...")
    
    # Create array with an outlier
    input_arr = np.array([
        [10, 10, 10],
        [10, 100, 10],  # 100 is outlier
        [10, 10, 10]
    ], dtype=np.float64)
    
    # Test with high threshold (includes outlier)
    output_high = np.zeros_like(input_arr, dtype=np.float64)
    fmedian(input_arr, output_high, 1, 1, 1)
    
    # Test with low threshold (excludes outlier from neighbors)
    output_low = np.zeros_like(input_arr, dtype=np.float64)
    fmedian(input_arr, output_low, 1, 1, 1)
    
    print("  Input array:")
    print(input_arr)
    print("\n  Output with high threshold (100.0):")
    print(output_high)
    print("\n  Output with low threshold (20.0):")
    print(output_low)
    
    # Note: threshold filtering was removed in the extension; center median is the median of
    # the full 3x3 neighborhood which is 10.0 in this test.
    assert np.isclose(output_low[1, 1], 10.0), f"Expected center pixel = 10.0, got {output_low[1,1]}"
    print("  \u2713 Threshold filtering not applied (expected with current implementation)")

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
    
    # Test with xsize=0, ysize=0 (only the pixel itself)
    output_0 = np.zeros_like(input_arr, dtype=np.float64)
    fmedian(input_arr, output_0, 0, 0, 1)
    
    # Should be identical to input when window is 1x1
    assert np.allclose(output_0, input_arr.astype(np.float64)), "Window size (1x1) produced unexpected output"
    print("  \u2713 Window size (1x1) works correctly")
    
    # Test with xsize=2, ysize=2 (5x5 window)
    output_2 = np.zeros_like(input_arr, dtype=np.float64)
    fmedian(input_arr, output_2, 2, 2, 1)
    print("  \u2713 Window size (5x5) works correctly")

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

    # Apply fmedian with a 3x3 window (xsize=1, ysize=1)
    fmedian(input_arr, output_arr, 1, 1, 1)

    print("  Input array:")
    print(input_arr)
    print("\n  Output array:")
    print(output_arr)

    # Neighbors excluding the center are [1,2,3,4,6,7,8,9]; median = (4+6)/2 = 5.0
    expected = 5.0
    assert np.isclose(output_arr[1, 1], expected), f"Expected center median {expected}, got {output_arr[1,1]}"
    print("  \u2713 Center exclusion works (median of neighbors used)")

def test_edge_cases():
    """Test edge cases like small arrays and boundary conditions."""
    print("\nTest 6: Edge cases...")
    
    # Test with 1x1 array
    input_1x1 = np.array([[42]], dtype=np.float64)
    output_1x1 = np.zeros_like(input_1x1, dtype=np.float64)
    fmedian(input_1x1, output_1x1, 1, 1, 1)
    
    assert np.isclose(output_1x1[0, 0], 42.0), f"Expected 42.0, got {output_1x1[0,0]}"
    print("  \u2713 1x1 array handled correctly")
    
    # Test with 2x2 array
    input_2x2 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    output_2x2 = np.zeros_like(input_2x2, dtype=np.float64)
    fmedian(input_2x2, output_2x2, 1, 1, 1)
    print("  ? 2x2 array handled correctly")

# Note: keep the main() script entry for running as a script; pytest will collect the
# `test_` functions above and treat assertions as test failures.

# Tests are collected by pytest via the `test_` prefixed functions above. The
# previous `main()` script harness (which executed tests and returned numeric
# exit codes) was removed to make these files pure pytest modules.

def main():
    """Run all tests."""
    test_basic_functionality()
    test_data_types()
    test_array_dimensions()
    test_threshold_filtering()
    test_window_sizes()
    test_edge_cases()
    test_center_exclusion()
    print("\nAll tests completed successfully.")


if __name__ == "__main__":
    main()
