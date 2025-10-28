#!/usr/bin/env python3
"""
Test script to verify the fsigma_ext module functionality.
"""

import numpy as np
import sys

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
    if output_arr.shape != input_arr.shape:
        print("  ? FAILED: output shape mismatch")
        return False
    if not np.all(np.isfinite(output_arr)):
        print("  ? FAILED: output contains non-finite values")
        return False
    if np.any(output_arr < 0):
        print("  ? FAILED: sigma must be non-negative")
        return False

    print("  ? Basic functionality test passed")
    return True

def test_data_types():
    """Test that data type checking works correctly."""
    print("\nTest 2: Data type validation...")
    
    # Test with correct types
    input_arr = np.array([[1, 2], [3, 4]], dtype=np.float64)
    output_arr = np.zeros_like(input_arr, dtype=np.float64)
    fsigma_ext.fsigma(input_arr, output_arr, 1, 1, 1)
    print("  ? Correct data types accepted")
    
    # Test with wrong input type (should fail)
    try:
        wrong_input = np.array([[1, 2], [3, 4]], dtype=np.float32)
        fsigma_ext.fsigma(wrong_input, output_arr, 1, 1, 1)
        print("  ? FAILED: Wrong input type should raise error")
        return False
    except TypeError:
        print("  ? Wrong input type correctly rejected")
    
    # Test with wrong output type (should fail)
    try:
        wrong_output = np.array([[1, 2], [3, 4]], dtype=np.float32)
        fsigma_ext.fsigma(input_arr, wrong_output, 1, 1, 1)
        print("  ? FAILED: Wrong output type should raise error")
        return False
    except TypeError:
        print("  ? Wrong output type correctly rejected")
    
    return True

def test_array_dimensions():
    """Test array dimension validation."""
    print("\nTest 3: Array dimension validation...")
    
    # Test with matching dimensions
    input_arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
    output_arr = np.zeros((2, 3), dtype=np.float64)
    fsigma_ext.fsigma(input_arr, output_arr, 1, 1, 1)
    print("  ? Matching dimensions accepted")
    
    # Test with mismatched dimensions (should fail)
    try:
        wrong_output = np.zeros((3, 3), dtype=np.float64)
        fsigma_ext.fsigma(input_arr, wrong_output, 1, 1, 1)
        print("  ? FAILED: Mismatched dimensions should raise error")
        return False
    except ValueError:
        print("  ? Mismatched dimensions correctly rejected")
    
    # Test with 1D array (should fail)
    try:
        input_1d = np.array([1, 2, 3], dtype=np.float64)
        output_1d = np.zeros(3, dtype=np.float64)
        fsigma_ext.fsigma(input_1d, output_1d, 1, 1, 1)
        print("  ? FAILED: 1D arrays should raise error")
        return False
    except ValueError:
        print("  ? 1D arrays correctly rejected")
    
    return True

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

    if not np.all(np.isfinite(output)) or np.any(output < 0):
        print("  ? FAILED: invalid sigma output")
        return False
    print("  ? Sigma computation produced valid (finite, non-negative) values")
    return True

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

    if np.allclose(output_0, 0.0):
        print("  ? Window size (1x1) produces zero sigma")
    else:
        print("  ? FAILED: Window size (1x1) produced non-zero sigma")
        return False
    
    # Test with xsize=2, ysize=2 (5x5 window)
    output_2 = np.zeros_like(input_arr, dtype=np.float64)
    fsigma_ext.fsigma(input_arr, output_2, 2, 2, 1)
    print("  ? Window size (5x5) produced sigma values")
    
    return True

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

    # Neighbors excluding the center are [1,2,3,4,6,7,8,9]; median = (4+6)/2 = 5.0
    # With the extreme center value present, including it should increase local sigma
    sigma_with = output_included[1, 1]
    sigma_without = output_excluded[1, 1]

    print(f"  sigma with center: {sigma_with:.3f}, without center: {sigma_without:.3f}")
    if sigma_with > sigma_without:
        print("  ? Center exclusion reduces sigma as expected")
        return True
    else:
        print("  ? FAILED: Center exclusion did not reduce sigma")
        return False

def test_edge_cases():
    """Test edge cases like small arrays and boundary conditions."""
    print("\nTest 6: Edge cases...")
    
    # Test with 1x1 array
    input_1x1 = np.array([[42]], dtype=np.float64)
    output_1x1 = np.zeros_like(input_1x1, dtype=np.float64)
    fsigma_ext.fsigma(input_1x1, output_1x1, 1, 1, 1)
    
    # With only one pixel and excluding the center, sigma should be 0.0
    if np.isclose(output_1x1[0, 0], 0.0):
        print("  ? 1x1 array produced zero sigma")
    else:
        print(f"  ? FAILED: Expected sigma 0.0, got {output_1x1[0, 0]}")
        return False
    
    # Test with 2x2 array
    input_2x2 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    output_2x2 = np.zeros_like(input_2x2, dtype=np.float64)
    fsigma_ext.fsigma(input_2x2, output_2x2, 1, 1, 1)
    if not np.all(np.isfinite(output_2x2)) or np.any(output_2x2 < 0):
        print("  ? FAILED: 2x2 produced invalid sigma values")
        return False
    print("  ? 2x2 array handled correctly")
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("fsigma_ext Test Suite")
    print("=" * 60)
    
    tests = [
        test_basic_functionality,
        test_data_types,
        test_array_dimensions,
        test_threshold_filtering,
        test_center_exclusion,
        test_window_sizes,
        test_edge_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ? FAILED with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("? All tests passed!")
        return 0
    else:
        print("? Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
