# Benchmark Results: sort125 vs qsort

## Test Configuration

- **Array Size**: 125 elements (double precision)
- **Test Method**: Random permutations of values 0-124
- **Iterations**: 1,000,000 sorts
- **Compiler**: gcc with -O3 optimization
- **Platform**: macOS (Apple Silicon)

## Results

### Run 1
```
sort125 (hybrid): 3.014 seconds (331,805 sorts/second)
qsort (stdlib):   5.151 seconds (194,132 sorts/second)
Speedup: 1.71x
```

### Run 2
```
sort125 (hybrid): 3.046 seconds (328,312 sorts/second)
qsort (stdlib):   5.132 seconds (194,837 sorts/second)
Speedup: 1.69x
```

## Summary

**Average Speedup: ~1.70x faster than qsort**

The hybrid sort125 implementation demonstrates consistent and significant performance improvement over the standard library qsort for 125-element arrays.

## Implementation Strategy

The hybrid sort125 uses:
1. **Pre-sorting phase**: Divides 125 elements into 5 blocks of 25 elements
2. **Block sorting**: Each block sorted using `sort25b` (optimized sorting network)
3. **Final pass**: Insertion sort on the partially-ordered array

This approach combines:
- The speed of specialized sorting networks for small fixed sizes
- The efficiency of insertion sort on nearly-sorted data
- Avoidance of the overhead from qsort's function pointer indirection

## Conclusion

? The hybrid sort125 is **consistently ~70% faster** than qsort for 125-element arrays
? This makes it highly suitable for image filtering operations with 5󬊅 3D windows
? The implementation maintains correctness (verified by 10,000 random permutation tests)
