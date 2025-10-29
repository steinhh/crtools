#!/usr/bin/env python3
"""
Test script to verify the fsigma_ext module functionality.
"""

import numpy as np
import sys
import os
import pytest

# Add parent directory to path so we can import from fsigma.fsigma_ext
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from fsigma.fsigma_ext import fsigma
except ImportError:
    print("ERROR: Could not import fsigma.fsigma_ext module.")
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
    fsigma(input_arr, output_arr, 1, 1, 1)

    print("  Input array:")
    print(input_arr)
    print("\n  Output array (local sigma):")
    print(output_arr)

    # Basic checks: output has same shape and non-negative finite values
    assert output_arr.shape == input_arr.shape, "output shape mismatch"
    assert np.all(np.isfinite(output_arr)), "output contains non-finite values"
    assert not np.any(output_arr < 0), "sigma must be non-negative"

    print("  \u2713 Basic functionality test passed")

def test_data_types():
    """Test that data type checking works correctly."""
    print("\nTest 2: Data type validation...")
    
    # Test with correct types
    input_arr = np.array([[1, 2], [3, 4]], dtype=np.float64)
    output_arr = np.zeros_like(input_arr, dtype=np.float64)
    fsigma(input_arr, output_arr, 1, 1, 1)
    print("  \u2713 Correct data types accepted")

    # Test with wrong input type (should fail)
    with pytest.raises(TypeError):
        wrong_input = np.array([[1, 2], [3, 4]], dtype=np.float32)
        fsigma(wrong_input, output_arr, 1, 1, 1)
    print("  \u2713 Wrong input type correctly rejected")

    # Test with wrong output type (should fail)
    with pytest.raises(TypeError):
        wrong_output = np.array([[1, 2], [3, 4]], dtype=np.float32)
        fsigma(input_arr, wrong_output, 1, 1, 1)
    print("  \u2713 Wrong output type correctly rejected")

def test_array_dimensions():
    """Test array dimension validation."""
    print("\nTest 3: Array dimension validation...")
    
    # Test with matching dimensions
    input_arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
    output_arr = np.zeros((2, 3), dtype=np.float64)
    fsigma(input_arr, output_arr, 1, 1, 1)
    print("  \u2713 Matching dimensions accepted")

    # Test with mismatched dimensions (should fail)
    with pytest.raises(ValueError):
        wrong_output = np.zeros((3, 3), dtype=np.float64)
        fsigma(input_arr, wrong_output, 1, 1, 1)
    print("  \u2713 Mismatched dimensions correctly rejected")

    # Test with 1D array (should fail)
    with pytest.raises(ValueError):
        input_1d = np.array([1, 2, 3], dtype=np.float64)
        output_1d = np.zeros(3, dtype=np.float64)
        fsigma(input_1d, output_1d, 1, 1, 1)
    print("  \u2713 1D arrays correctly rejected")

def test_window_sizes():
    """Test different window sizes."""
    print("\nTest 4: Different window sizes...")
    
    input_arr = np.array([
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25]
    ], dtype=np.float64)
    
    # Test with xsize=0, ysize=0 (only the pixel itself) => sigma should be 0
    output_0 = np.zeros_like(input_arr, dtype=np.float64)
    fsigma(input_arr, output_0, 0, 0, 1)

    assert np.allclose(output_0, 0.0), "Window size (1x1) produced non-zero sigma"
    print("  \u2713 Window size (1x1) produces zero sigma")

    # Test with xsize=2, ysize=2 (5x5 window)
    output_2 = np.zeros_like(input_arr, dtype=np.float64)
    fsigma(input_arr, output_2, 2, 2, 1)
    print("  \u2713 Window size (5x5) produced sigma values")

def test_center_exclusion():
    """Verify that excluding the center pixel lowers the local sigma."""
    print("\nTest 6: Center exclusion from sigma computation...")

    # Construct a 3x3 array where the center is an outlier
    input_arr = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 999.0, 6.0],
        [7.0, 8.0, 9.0]
    ], dtype=np.float64)

    output_arr = np.zeros_like(input_arr, dtype=np.float64)

    # Apply fsigma with a 3x3 window (xsize=1, ysize=1)
    # First compute with center included (exclude_center=0)
    fsigma(input_arr, output_arr, 1, 1, 0)
    output_included = output_arr.copy()

    # Now compute excluding the center from the neighborhood
    fsigma(input_arr, output_arr, 1, 1, 1)
    output_excluded = output_arr.copy()

    print("  Input array:")
    print(input_arr)
    print("\n  Output array:")
    print(output_arr)

    # Neighbors excluding the center are [1,2,3,4,6,7,8,9]; including the outlier should
    # increase the measured sigma relative to the excluded case
    sigma_with = output_included[1, 1]
    sigma_without = output_excluded[1, 1]

    print(f"  sigma with center: {sigma_with:.3f}, without center: {sigma_without:.3f}")
    assert sigma_with > sigma_without, "Center exclusion did not reduce sigma"
    print("  \u2713 Center exclusion reduces sigma as expected")

def test_edge_cases():
    """Test edge cases like small arrays and boundary conditions."""
    print("\nTest 5: Edge cases...")
    
    # Test with 1x1 array
    input_1x1 = np.array([[42]], dtype=np.float64)
    output_1x1 = np.zeros_like(input_1x1, dtype=np.float64)
    fsigma(input_1x1, output_1x1, 1, 1, 1)
    
    # With only one pixel and excluding the center, sigma should be 0.0
    assert np.isclose(output_1x1[0, 0], 0.0), f"Expected sigma 0.0, got {output_1x1[0,0]}"
    print("  \u2713 1x1 array produced zero sigma")

    # Test with 2x2 array
    input_2x2 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    output_2x2 = np.zeros_like(input_2x2, dtype=np.float64)
    fsigma(input_2x2, output_2x2, 1, 1, 1)
    assert np.all(np.isfinite(output_2x2)) and not np.any(output_2x2 < 0), "2x2 produced invalid sigma values"
    print("  \u2713 2x2 array handled correctly")

# Pytest discovers the `test_` functions automatically.
# A minimal `main()` helper remains for manual runs without pytest.


def main():
    """Run all tests in this module when executed as a script.

    This calls the local `test_...` functions sequentially so their
    informational prints (OK / NOT OK!) are visible on the console.
    If any test raises, print a NOT OK! message and exit with a non-zero code.
    """
    tests = [
        test_basic_functionality,
        test_data_types,
        test_array_dimensions,
        test_window_sizes,
        test_edge_cases,
        test_center_exclusion,
    ]

    for t in tests:
        try:
            t()
        except Exception as e:  # noqa: BLE001 - broad catch for test harness
            print(f"\nNOT OK! Test '{t.__name__}' failed: {e}")
            raise SystemExit(1)

    print("\nAll tests completed successfully.")


if __name__ == "__main__":
    main()
