# Sorting Network Bug Report

## Test Results Summary

Comprehensive testing of all sorting networks (sort3 through sort27) against qsort with 10,000 random permutations each.

### Results

| Function | Status | Notes |
|----------|--------|-------|
| sort3    | ? PASS | All 10,000 tests passed |
| sort4    | ? PASS | All 10,000 tests passed |
| sort5    | ? PASS | All 10,000 tests passed |
| sort6    | ? PASS | All 10,000 tests passed |
| sort7    | ? PASS | All 10,000 tests passed |
| sort8    | ? PASS | All 10,000 tests passed |
| sort9    | ? PASS | All 10,000 tests passed |
| **sort11** | **? FAIL** | **OUT OF BOUNDS BUG** |
| sort12   | ? PASS | All 10,000 tests passed |
| sort13   | ? PASS | All 10,000 tests passed |
| sort14   | ? PASS | All 10,000 tests passed |
| sort15   | ? PASS | All 10,000 tests passed |
| sort16   | ? PASS | All 10,000 tests passed |
| sort17   | ? PASS | All 10,000 tests passed |
| sort18   | ? PASS | All 10,000 tests passed |
| sort19   | ? PASS | All 10,000 tests passed |
| sort20   | ? PASS | All 10,000 tests passed |
| sort21   | ? PASS | All 10,000 tests passed |
| sort22   | ? PASS | All 10,000 tests passed |
| sort23   | ? PASS | All 10,000 tests passed |
| sort24   | ? PASS | All 10,000 tests passed |
| sort25   | ? PASS | All 10,000 tests passed |
| sort26   | ? PASS | All 10,000 tests passed |
| sort27   | ? PASS | All 10,000 tests passed |

## Bug Details: sort11

### Location
File: `src/ftools/sorting/sorting_networks_generated.c`, lines 184-243

### Problem
The sorting network accesses `d[11]` when sorting an 11-element array (valid indices: 0-10).

**Problematic line (Stage 1):**
```c
SWAP(d[3], d[11]);  // BUG: d[11] is out of bounds!
```

**Also in Stage 2:**
```c
SWAP(d[10], d[11]);  // BUG: d[11] is out of bounds!
```

### Impact
- Undefined behavior: reads/writes to memory outside array bounds
- Can cause data corruption
- Results in incorrect sorting (duplicate values, missing values)
- Potential security vulnerability

### Example Failure
**Input:** `[3.00, 0.00, 1.00, 2.00, 9.00, 8.00, 10.00, 4.00, 7.00, 5.00, 6.00]`
**sort11 result:** `[0.00, 0.00, 1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00]`
**qsort result:** `[0.00, 1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.00]`

Notice: duplicate 0.00, missing 10.00

## Root Cause

This appears to be a copy-paste error where a 12-element sorting network was incorrectly adapted for 11 elements. The network references 12 indices (0-11) instead of 11 indices (0-10).

## Recommendations

### Option 1: Fix the Sorting Network (Preferred)
Replace `sort11` with a correct 11-element sorting network. A proper 11-element sorting network requires approximately 35-37 comparators.

### Option 2: Use Hybrid Approach
Replace the buggy sorting network with insertion sort for size 11:
```c
static inline void sort11(double *d)
{
  insertion_sort(d, 11);
}
```

### Option 3: Remove from Switch Statement
In `sorting.c`, remove the `case 11:` and let it fall through to the default case which uses insertion sort.

## Testing

Use the provided test suite `test_all_sorts.c` to verify any fixes:
```bash
cd src/ftools/sorting
gcc -O2 -o test_all_sorts test_all_sorts.c -lm
./test_all_sorts
```

## Files Affected

1. `src/ftools/sorting/sorting_networks_generated.c` - Contains buggy sort11
2. `src/ftools/sorting/sorting.c` - References sort11 in switch statement
3. `src/ftools/sorting/test_all_sorts.c` - New comprehensive test suite

## Date Identified
November 9, 2025

## Status
?? **CRITICAL BUG** - Causes data corruption and incorrect results
