#!/usr/bin/env python3
"""
Main program that demonstrates creating a 2D numpy int16 array.
"""

import numpy as np


def create_2d_array(img_xsize, img_ysize):
    return np.zeros((img_ysize, img_xsize), dtype=np.int16)


def main():
    # Example usage
    width = 512
    height = 256
    
    # Create the 2D array
    array_2d = create_2d_array(width, height)
    
    print(f"Created 2D array with shape: {array_2d.shape}")
    print(f"Array data type: {array_2d.dtype}")
    print(f"Array size in memory: {array_2d.nbytes} bytes")
    
    # Optional: Fill with some example data
    array_2d[100:150, 200:300] = 1000
    print("Set a rectangular region to value 1000")
    print(f"Sample values: {array_2d[125, 250]}")


if __name__ == "__main__":
    main()