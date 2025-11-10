# Benchmark Results: sort124 vs qsort

## Test Configuration

- **Array Size**: 124 elements (double precision)
- **Test Method**: Random permutations of values 0-123
- **Iterations**: 1,000,000 sorts
- **Compiler**: gcc with -O3 optimization
- **Platform**: macOS (Apple Silicon)

## Results

### Run 1

```text
sort124 (hybrid): 2.977 seconds (335,870 sorts/second)
qsort (stdlib):   4.983 seconds (200,672 sorts/second)
Speedup: 1.67x
```

### Run 2

```text
sort124 (hybrid): 2.975 seconds (336,156 sorts/second)
qsort (stdlib):   4.972 seconds (201,140 sorts/second)
Speedup: 1.67x
```

## Summary

**Average Speedup: 1.67x faster than qsort**

The hybrid sort124 implementation demonstrates consistent and significant performance improvement over the standard library qsort for 124-element arrays.

## Implementation Strategy

The hybrid sort124 uses:

1. **Pre-sorting phase**: Divides 124 elements into 5 blocks of 24 elements + 4 remaining elements
2. **Block sorting**: Each of the 5 blocks sorted using `sort24` (optimized sorting network)
3. **Final pass**: Insertion sort on the partially-ordered array (including the 4 unsorted elements)

This approach combines:

- The speed of specialized sorting networks for small fixed sizes
- The efficiency of insertion sort on nearly-sorted data
- Avoidance of the overhead from qsort's function pointer indirection

## Comparison with sort125

Both sort124 and sort125 show similar performance characteristics:

- **sort124**: 1.67x faster than qsort (uses 5 × sort24 blocks)
- **sort125**: 1.70x faster than qsort (uses 5 × sort25b blocks)

The slightly better performance of sort125 may be due to the cleaner division (125 = 5 × 25 exactly, vs 124 = 5 × 24 + 4).

## Conclusion

? The hybrid sort124 is **consistently ~67% faster** than qsort for 124-element arrays  
? This makes it highly suitable for image filtering operations with near-5×5×5 3D windows  
? The implementation maintains correctness (verified by 10,000 random permutation tests)
