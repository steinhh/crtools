#!/usr/bin/env python3
"""
Verification script for sorting networks.
Tests that sort3, sort9, sort25, and sort27 actually sort arrays correctly.
"""

import numpy as np
from ftools import fmedian
from ftools.fmedian3 import fmedian3


def verify_sorting_via_median(func, shape, window_size, num_tests=1000, is_3d=False):
    """
    Verify sorting by checking that median computation gives correct results.
    The median function relies on the sorting networks, so if sorting is broken,
    medians will be incorrect.
    """
    print(f"\nTesting {func.__name__} with window size {window_size}...")
    
    failures = []
    rng = np.random.default_rng(42)
    
    for i in range(num_tests):
        # Create random test array
        arr = rng.standard_normal(shape).astype(np.float64)
        
        # Compute median using our function
        if is_3d:
            wx, wy, wz = window_size
            result = func(arr, wx, wy, wz, 0)
        else:
            result = func(arr, window_size, 0)
        
        # Verify by computing median manually for center pixel
        center_idx = tuple(s // 2 for s in shape)
        
        # Extract window around center
        if len(shape) == 2:
            h, w = shape
            cy, cx = center_idx
            wy, wx = window_size
            
            # Calculate window bounds
            y_start = max(0, cy - wy)
            y_end = min(h, cy + wy + 1)
            x_start = max(0, cx - wx)
            x_end = min(w, cx + wx + 1)
            
            window = arr[y_start:y_end, x_start:x_end].flatten()
        else:  # 3D
            d, h, w = shape
            cz, cy, cx = center_idx
            wz, wy, wx = window_size
            
            z_start = max(0, cz - wz)
            z_end = min(d, cz + wz + 1)
            y_start = max(0, cy - wy)
            y_end = min(h, cy + wy + 1)
            x_start = max(0, cx - wx)
            x_end = min(w, cx + wx + 1)
            
            window = arr[z_start:z_end, y_start:y_end, x_start:x_end].flatten()
        
        # Compute expected median using numpy
        expected = np.median(window)
        computed = result[center_idx]
        
        # Check if they match
        if not np.isclose(computed, expected, rtol=1e-10, atol=1e-12):
            failures.append({
                'test': i,
                'expected': expected,
                'computed': computed,
                'diff': abs(expected - computed),
                'window': window.copy()
            })
    
    if failures:
        print(f"  ? FAILED: {len(failures)}/{num_tests} tests failed")
        # Show first few failures
        for f in failures[:3]:
            print(f"    Test {f['test']}: expected {f['expected']:.10f}, got {f['computed']:.10f} (diff: {f['diff']:.2e})")
            print(f"    Window values: {sorted(f['window'])}")
        return False
    else:
        print(f"  ? PASSED: All {num_tests} tests passed")
        return True


def test_specific_cases():
    """Test specific edge cases and known patterns."""
    print("\nTesting specific edge cases...")
    
    all_passed = True
    
    # Test 1: sort3 via 3x1 window (1D horizontal)
    print("  Testing sort3 (via 3x1 window)...")
    arr = np.array([[3.0, 1.0, 2.0, 5.0, 4.0]], dtype=np.float64)
    result = fmedian(arr, (1, 1), 0)  # 3x3 window centered on each pixel
    # Middle element should be median of [1, 2, 3]
    expected_middle = 2.0
    if np.isclose(result[0, 2], expected_middle):
        print("    ? sort3 test passed")
    else:
        print(f"    ? sort3 test failed: expected {expected_middle}, got {result[0, 2]}")
        all_passed = False
    
    # Test 2: sort9 via 3x3 window
    print("  Testing sort9 (via 3x3 window)...")
    arr = np.array([
        [9.0, 1.0, 5.0],
        [3.0, 7.0, 2.0],
        [6.0, 4.0, 8.0]
    ], dtype=np.float64)
    result = fmedian(arr, (1, 1), 0)  # 3x3 window
    # Center should be median of [1,2,3,4,5,6,7,8,9] = 5.0
    expected_center = 5.0
    if np.isclose(result[1, 1], expected_center):
        print("    ? sort9 test passed")
    else:
        print(f"    ? sort9 test failed: expected {expected_center}, got {result[1, 1]}")
        all_passed = False
    
    # Test 3: sort25 via 5x5 window
    print("  Testing sort25 (via 5x5 window)...")
    arr = np.arange(49, dtype=np.float64).reshape(7, 7)
    rng = np.random.default_rng(42)
    rng.shuffle(arr.ravel())
    result = fmedian(arr, (2, 2), 0)  # 5x5 window
    # Center (3,3) should be median of 25 values
    window = arr[1:6, 1:6].flatten()
    expected_center = np.median(window)
    if np.isclose(result[3, 3], expected_center, rtol=1e-10):
        print("    ? sort25 test passed")
    else:
        print(f"    ? sort25 test failed: expected {expected_center}, got {result[3, 3]}")
        all_passed = False
    
    # Test 4: sort27 via 3x3x3 window
    print("  Testing sort27 (via 3x3x3 window)...")
    arr = np.arange(27, dtype=np.float64).reshape(3, 3, 3)
    rng = np.random.default_rng(42)
    rng.shuffle(arr.ravel())
    result = fmedian3(arr, 3, 3, 3, 0)
    # Center should be median of all 27 values
    expected_center = np.median(arr)
    if np.isclose(result[1, 1, 1], expected_center, rtol=1e-10):
        print("    ? sort27 test passed")
    else:
        print(f"    ? sort27 test failed: expected {expected_center}, got {result[1, 1, 1]}")
        all_passed = False
    
    return all_passed


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Sorting Network Verification")
    print("=" * 60)
    
    all_passed = True
    
    # Test specific cases first
    all_passed &= test_specific_cases()
    
    # Random tests for 2D median (uses sort9 and sort25)
    all_passed &= verify_sorting_via_median(fmedian, (7, 7), (1, 1), num_tests=500, is_3d=False)
    all_passed &= verify_sorting_via_median(fmedian, (9, 9), (2, 2), num_tests=500, is_3d=False)
    
    # Random tests for 3D median (uses sort27)
    all_passed &= verify_sorting_via_median(fmedian3, (5, 5, 5), (3, 3, 3), num_tests=500, is_3d=True)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("? ALL TESTS PASSED - Sorting networks are correct!")
    else:
        print("? SOME TESTS FAILED - Sorting networks need fixing!")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
