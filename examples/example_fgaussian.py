"""
Example usage of fgaussian module
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import numpy as np
from ftools.fgaussian import gaussian


def example_basic():
    """Basic Gaussian profile example"""
    print("Example 1: Basic Gaussian profile")
    print("=" * 50)
    
    # Create x values
    x = np.linspace(-10, 10, 1000)
    
    # Compute Gaussian profile
    y = gaussian(x, i0=1.0, mu=0.0, sigma=1.0)
    
    print(f"Input shape: {x.shape}")
    print(f"Output shape: {y.shape}")
    print(f"Peak value: {y.max():.6f} (expected 1.0)")
    print(f"Value at mu: {y[500]:.6f} (expected 1.0)")
    print()


def example_multiple_gaussians():
    """Multiple Gaussian profiles"""
    print("Example 2: Multiple Gaussian profiles")
    print("=" * 50)
    
    x = np.linspace(-10, 10, 1000)
    
    # Different parameters
    y1 = gaussian(x, i0=1.0, mu=0.0, sigma=1.0)
    y2 = gaussian(x, i0=0.5, mu=2.0, sigma=0.5)
    y3 = gaussian(x, i0=0.8, mu=-3.0, sigma=1.5)
    
    # Sum of Gaussians
    y_total = y1 + y2 + y3
    
    print(f"Gaussian 1 peak: {y1.max():.6f}")
    print(f"Gaussian 2 peak: {y2.max():.6f}")
    print(f"Gaussian 3 peak: {y3.max():.6f}")
    print(f"Total peak: {y_total.max():.6f}")
    print()


def example_2d():
    """2D Gaussian (separable)"""
    print("Example 3: 2D Gaussian (separable)")
    print("=" * 50)
    
    # Create 2D grid
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    
    # Compute radial distance
    R = np.sqrt(X**2 + Y**2)
    
    # 2D Gaussian (radially symmetric)
    Z = gaussian(R, i0=1.0, mu=0.0, sigma=1.5)
    
    print(f"2D grid shape: {Z.shape}")
    print(f"Peak value: {Z.max():.6f}")
    print(f"Central value: {Z[50, 50]:.6f}")
    print()


def example_benchmark():
    """Benchmark C vs NumPy"""
    print("Example 4: Performance benchmark")
    print("=" * 50)
    
    import time
    
    # Large array
    n = 10_000_000
    x = np.linspace(-100, 100, n)
    
    # Warm up
    _ = gaussian(x, i0=1.0, mu=0.0, sigma=10.0)
    
    # Benchmark C extension
    start = time.time()
    for _ in range(10):
        result_c = gaussian(x, i0=1.0, mu=0.0, sigma=10.0)
    time_c = (time.time() - start) / 10
    
    # Benchmark NumPy
    start = time.time()
    for _ in range(10):
        result_np = 1.0 * np.exp(-((x - 0.0) ** 2) / (2 * 10.0 ** 2))
    time_np = (time.time() - start) / 10
    
    # Verify results match
    max_diff = np.max(np.abs(result_c - result_np))
    
    print(f"Array size: {n:,} elements")
    print(f"C extension: {time_c*1000:.2f} ms")
    print(f"NumPy:       {time_np*1000:.2f} ms")
    print(f"Speedup:     {time_np/time_c:.2f}x")
    print(f"Max difference: {max_diff:.2e}")
    print()


if __name__ == "__main__":
    try:
        example_basic()
        example_multiple_gaussians()
        example_2d()
        example_benchmark()
        
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
