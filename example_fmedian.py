#!/usr/bin/env python3
"""
Example program demonstrating the use of fmedian_ext module.

This program creates a sample 2D array with some noise and applies
the filtered median function to smooth it.
"""

import numpy as np
import fmedian_ext

def main():
    print("=" * 60)
    print("Filtered Median Example")
    print("=" * 60)
    
    # Create a sample input array (10x10) with int16 type
    print("\n1. Creating sample input array (10x10)...")
    input_array = np.array([
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 20, 20, 20, 20, 20, 20, 20, 20, 10],
        [10, 20, 30, 30, 30, 30, 30, 30, 20, 10],
        [10, 20, 30, 40, 40, 40, 40, 30, 20, 10],
        [10, 20, 30, 40, 100, 40, 40, 30, 20, 10],  # 100 is an outlier
        [10, 20, 30, 40, 40, 40, 40, 30, 20, 10],
        [10, 20, 30, 30, 30, 30, 30, 30, 20, 10],
        [10, 20, 20, 20, 20, 20, 20, 20, 20, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [5, 10, 10, 10, 10, 10, 10, 10, 10, 5],
    ], dtype=np.float64)
    
    print("Input array:")
    print(input_array)
    
    # Create output array with same shape but float64 type
    output_array = np.zeros_like(input_array, dtype=np.float64)
    
    # Define filter parameters
    xsize = np.int16(1)      # Window half-width in x direction
    ysize = np.int16(1)      # Window half-width in y direction
    threshold = 50.0         # Threshold for including neighbors
    
    print(f"\n2. Applying filtered median with parameters:")
    print(f"   - Window size: ({2*xsize+1} x {2*ysize+1})")
    print(f"   - Threshold: {threshold}")
    
    # Call the fmedian function
    fmedian_ext.fmedian(input_array, output_array, xsize, ysize, threshold)
    
    print("\n3. Output array (filtered median):")
    print(output_array)
    
    # Show the difference (particularly for the outlier)
    print("\n4. Difference (input - output):")
    difference = input_array.astype(np.float64) - output_array
    print(difference)
    
    # Highlight where the filter made significant changes
    print("\n5. Analysis:")
    significant_changes = np.abs(difference) > 5
    if np.any(significant_changes):
        print(f"   Significant changes (|diff| > 5) at {np.sum(significant_changes)} locations:")
        coords = np.argwhere(significant_changes)
        for coord in coords[:5]:  # Show first 5
            y, x = coord
            print(f"   Position ({y}, {x}): {input_array[y, x]} -> {output_array[y, x]:.2f} (diff: {difference[y, x]:.2f})")
        if len(coords) > 5:
            print(f"   ... and {len(coords) - 5} more")
    else:
        print("   No significant changes detected.")
    
    # Test with stricter threshold
    print("\n6. Testing with stricter threshold (10.0)...")
    output_array2 = np.zeros_like(input_array, dtype=np.float64)
    threshold2 = 10.0
    fmedian_ext.fmedian(input_array, output_array2, xsize, ysize, threshold2)
    
    print("Output array with threshold=10.0:")
    print(output_array2)
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
