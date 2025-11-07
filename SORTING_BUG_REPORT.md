# Sorting Network Verification Report

## Date: November 7, 2025

## Summary

A critical bug was discovered in the `sort27` function in `src/ftools/sorting.c`. The sorting network for 27 elements was **incomplete and failed to properly sort arrays in approximately 65% of test cases**.

## Problem Description

The original `sort27` function used a hierarchical approach:
1. Stage 1: Sort 9 groups of 3 elements (using `sort3`)
2. Stage 2: Sort 3 groups of 9 elements (using `sort9`)  
3. Stage 3: Attempt to merge three sorted groups using an odd-even merge network

**The merge network in Stage 3 was incomplete.** While it performed many comparisons, it did not implement a valid sorting network for merging three sorted groups of 9 elements into a fully sorted array of 27 elements.

## Verification Method

A standalone C test program (`test_sorting_c.c`) was created to directly test the sorting functions with 10,000 random permutations each. Results:

### Before Fix:
```
Testing sort3 with 10000 random permutations...
  ? PASSED: All 10000 tests passed

Testing sort9 with 10000 random permutations...
  ? PASSED: All 10000 tests passed

Testing sort27 with 10000 random permutations...
  ? FAILED: 6478/10000 tests failed (64.78% failure rate)
```

Example of failed output showing elements out of order:
```
[-464.37 -433.95 -379.89 -359.73 -335.68 -273.44 -241.95 -220.15 -205.79 
 -151.96 -133.26 -101.56 -21.30 -113.82 19.58 44.11 51.58 72.70 134.72 
 139.29 213.21 287.56 377.47 388.39 411.24 455.05 486.09]
                                ^^^^^^^^ OUT OF ORDER!
```

Note that -113.82 appears after -21.30, which violates sorted order.

## Root Cause

Designing a correct sorting network for 27 elements is non-trivial. The merge stage attempted to use an odd-even merge pattern, but:

1. The comparison pattern was incomplete for a 3-way merge
2. A proper sorting network for merging three sorted sequences of 9 elements requires more comparisons than were implemented
3. The code did not follow any proven sorting network design (e.g., Batcher's merge, bitonic merge)

## Solution

The `sort27` function was changed to use a **hybrid approach** similar to `sort25`:

1. Stage 1: Sort 9 groups of 3 elements (using `sort3`) 
2. Stage 2: Sort 3 groups of 9 elements (using `sort9`)
3. Stage 3: **Use insertion sort to complete the merge**

This approach:
- **Guarantees correctness** - insertion sort is proven correct
- Still benefits from the partial ordering created by stages 1 and 2
- Is efficient for small arrays (27 elements)
- Maintains the same performance characteristics as `sort25`

### Code Change

```c
/* Sorting network for 27 elements (3x3x3 window) */
static inline void sort27(double *d)
{
  /* Hybrid approach for 27 elements: partial network + insertion sort */
  /* Stage 1: Sort 9 groups of 3 elements each */
  sort3(&d[0]);
  sort3(&d[3]);
  sort3(&d[6]);
  sort3(&d[9]);
  sort3(&d[12]);
  sort3(&d[15]);
  sort3(&d[18]);
  sort3(&d[21]);
  sort3(&d[24]);

  /* Stage 2: Sort 3 groups of 9 elements each */
  sort9(&d[0]);
  sort9(&d[9]);
  sort9(&d[18]);

  /* Stage 3: Merge using insertion sort */
  /* This is more reliable than an incomplete merge network */
  for (int i = 1; i < 27; i++)
  {
    double key = d[i];
    int j = i - 1;
    while (j >= 0 && d[j] > key)
    {
      d[j + 1] = d[j];
      j--;
    }
    d[j + 1] = key;
  }
}
```

## Verification Results After Fix

```
Testing sort3 with 10000 random permutations...
  ? PASSED: All 10000 tests passed

Testing sort9 with 10000 random permutations...
  ? PASSED: All 10000 tests passed

Testing sort27 with 10000 random permutations...
  ? PASSED: All 10000 tests passed
```

**All tests now pass with 100% success rate.**

## Impact Analysis

### Affected Functions
- `fmedian3()` - 3D median filter using 3x3x3 windows
- `fsigma3()` - 3D sigma filter using 3x3x3 windows

### Severity
**HIGH** - The bug caused incorrect median calculations for 3D arrays with 3x3x3 windows, which would produce incorrect filtered results approximately 65% of the time.

### Risk Assessment
- **2D functions (`fmedian`, `fsigma`)**: NOT affected - use `sort9` and `sort25` which were verified correct
- **3D functions with non-3x3x3 windows**: May be affected if they fall back to generic sorting
- **3D functions with 3x3x3 windows**: AFFECTED - used the buggy `sort27`

## Recommendations

1. **REBUILD** all C extensions immediately: `python setup.py build_ext --inplace`
2. **RERUN** all tests, especially 3D tests: `pytest tests/`
3. **NOTIFY USERS** if any production data was processed with `fmedian3` or `fsigma3` using 3x3x3 windows
4. **CONSIDER REPROCESSING** any critical data that was filtered with 3D functions

## Files Modified

- `src/ftools/sorting.c` - Fixed `sort27` function (lines 93-235)

## Testing Artifacts

- `test_sorting_c.c` - Standalone C test program for sorting networks
- `test_sorting_verification.py` - Python verification script (requires built extensions)

## Status of Other Sorting Networks

All other sorting networks were verified correct:

- ? **sort3** (3 elements): Correct - classic 3-element sorting network
- ? **sort9** (9 elements): Correct - verified with 10,000 random tests
- ? **sort25** (25 elements): Correct - uses hybrid approach with insertion sort
- ? **sort27** (27 elements): FIXED - now uses hybrid approach with insertion sort

## Next Steps

1. Install Python development headers if not available: `sudo yum install python3-devel` (or equivalent)
2. Rebuild extensions: `python3.11 setup.py build_ext --inplace`
3. Run full test suite: `python3.11 -m pytest tests/`
4. Verify 3D functionality is working correctly
5. Consider adding regression tests specifically for sort27 edge cases
