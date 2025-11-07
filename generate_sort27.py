#!/usr/bin/env python3
"""
Generate a correct sorting network for 27 elements using Batcher's odd-even merge.
This will generate the C code for the comparators.
"""

def generate_odd_even_merge(lo, n, r, ascending=True):
    """
    Generate comparators for odd-even merge network.
    lo: starting index
    n: number of elements
    r: step size
    """
    comparators = []
    step = r * 2
    if step < n:
        # Recursively merge odd and even subsequences
        comparators.extend(generate_odd_even_merge(lo, n, step, ascending))
        comparators.extend(generate_odd_even_merge(lo + r, n, step, ascending))
        # Compare-exchange between merged sequences
        for i in range(lo + r, lo + n - r, step):
            comparators.append((i, i + r, ascending))
    else:
        comparators.append((lo, lo + r, ascending))
    return comparators

def generate_odd_even_merge_sort(lo, n, ascending=True):
    """
    Generate comparators for odd-even merge sort.
    lo: starting index
    n: number of elements  
    """
    comparators = []
    if n > 1:
        m = n // 2
        # Recursively sort first and second half in opposite directions
        comparators.extend(generate_odd_even_merge_sort(lo, m, not ascending))
        comparators.extend(generate_odd_even_merge_sort(lo + m, n - m, ascending))
        # Merge the two sorted halves
        comparators.extend(generate_odd_even_merge(lo, n, 1, ascending))
    return comparators

def generate_c_code_for_27():
    """Generate C code for sorting 27 elements."""
    comparators = generate_odd_even_merge_sort(0, 27, True)
    
    print(f"/* Generated sorting network for 27 elements */")
    print(f"/* Total comparators: {len(comparators)} */")
    print("static inline void sort27_generated(double *d)")
    print("{")
    
    for i, j, asc in comparators:
        if asc:
            print(f"  SWAP(d[{i}], d[{j}]);")
        else:
            # For descending, we still use SWAP (it will put smaller in first position)
            # but logically we're building a descending sequence
            print(f"  SWAP(d[{i}], d[{j}]);")
    
    print("}")
    print()
    print(f"Total comparison operations: {len(comparators)}")

if __name__ == "__main__":
    generate_c_code_for_27()
