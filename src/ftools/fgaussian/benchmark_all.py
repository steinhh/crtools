"""
Comprehensive Benchmark: All implementations
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import numpy as np
import time
from ftools.fgaussian import fgaussian_ext, fgaussian_simd_ext, fgaussian_accelerate_ext


def benchmark_all():
    """Compare all implementations"""
    print("Complete Performance Comparison")
    print("=" * 95)
    print(f"{'Size':>12} {'NumPy':>10} {'Scalar C':>10} {'SIMD C':>10} {'Accelerate':>10} "
          f"{'C Speed':>10} {'SIMD':>10} {'Accel':>10}")
    print(f"{'':>12} {'(ms)':>10} {'(ms)':>10} {'(ms)':>10} {'(ms)':>10} "
          f"{'up':>10} {'Speedup':>10} {'Speedup':>10}")
    print("-" * 95)
    
    sizes = [1000, 10_000, 100_000, 1_000_000, 10_000_000]
    
    for n in sizes:
        x = np.linspace(-100, 100, n, dtype=np.float64)
        i0, mu, sigma = 1.0, 0.0, 10.0
        
        # Warm up all implementations
        _ = i0 * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
        _ = fgaussian_ext.gaussian(x, i0, mu, sigma)
        _ = fgaussian_simd_ext.gaussian(x, i0, mu, sigma)
        _ = fgaussian_accelerate_ext.gaussian(x, i0, mu, sigma)
        
        n_runs = 20 if n <= 1_000_000 else 10
        
        # Benchmark NumPy
        times_np = []
        for _ in range(n_runs):
            start = time.time()
            result_np = i0 * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
            times_np.append(time.time() - start)
        time_np = np.median(times_np) * 1000
        
        # Benchmark Scalar C
        times_scalar = []
        for _ in range(n_runs):
            start = time.time()
            result_scalar = fgaussian_ext.gaussian(x, i0, mu, sigma)
            times_scalar.append(time.time() - start)
        time_scalar = np.median(times_scalar) * 1000
        
        # Benchmark SIMD C
        times_simd = []
        for _ in range(n_runs):
            start = time.time()
            result_simd = fgaussian_simd_ext.gaussian(x, i0, mu, sigma)
            times_simd.append(time.time() - start)
        time_simd = np.median(times_simd) * 1000
        
        # Benchmark Accelerate
        times_accel = []
        for _ in range(n_runs):
            start = time.time()
            result_accel = fgaussian_accelerate_ext.gaussian(x, i0, mu, sigma)
            times_accel.append(time.time() - start)
        time_accel = np.median(times_accel) * 1000
        
        # Verify accuracy
        if n == 1000:
            max_diff_scalar = np.max(np.abs(result_np - result_scalar))
            max_diff_simd = np.max(np.abs(result_np - result_simd))
            max_diff_accel = np.max(np.abs(result_np - result_accel))
            print(f"\nAccuracy (n={n}):")
            print(f"  Scalar C:    {max_diff_scalar:.2e}")
            print(f"  SIMD C:      {max_diff_simd:.2e}")
            print(f"  Accelerate:  {max_diff_accel:.2e}\n")
        
        speedup_scalar = time_np / time_scalar
        speedup_simd = time_np / time_simd
        speedup_accel = time_np / time_accel
        
        print(f"{n:12,} {time_np:10.3f} {time_scalar:10.3f} {time_simd:10.3f} {time_accel:10.3f} "
              f"{speedup_scalar:10.2f}x {speedup_simd:10.2f}x {speedup_accel:10.2f}x")
    
    print()


def benchmark_detailed():
    """Detailed analysis for 10M elements"""
    print("Detailed Statistics (10M elements, 50 runs)")
    print("=" * 95)
    
    n = 10_000_000
    x = np.linspace(-100, 100, n, dtype=np.float64)
    i0, mu, sigma = 1.0, 0.0, 10.0
    
    n_runs = 50
    
    times = {
        'NumPy': [],
        'Scalar C': [],
        'SIMD C': [],
        'Accelerate': []
    }
    
    for _ in range(n_runs):
        start = time.time()
        _ = i0 * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
        times['NumPy'].append((time.time() - start) * 1000)
        
        start = time.time()
        _ = fgaussian_ext.gaussian(x, i0, mu, sigma)
        times['Scalar C'].append((time.time() - start) * 1000)
        
        start = time.time()
        _ = fgaussian_simd_ext.gaussian(x, i0, mu, sigma)
        times['SIMD C'].append((time.time() - start) * 1000)
        
        start = time.time()
        _ = fgaussian_accelerate_ext.gaussian(x, i0, mu, sigma)
        times['Accelerate'].append((time.time() - start) * 1000)
    
    print(f"{'Method':>15} {'Min':>8} {'Median':>8} {'Mean':>8} {'Max':>8} {'Std':>8} {'vs NumPy':>10}")
    print("-" * 95)
    
    for name in ['NumPy', 'Scalar C', 'SIMD C', 'Accelerate']:
        t = np.array(times[name])
        speedup = np.median(times['NumPy']) / np.median(t)
        print(f"{name:>15} {np.min(t):8.2f} {np.median(t):8.2f} {np.mean(t):8.2f} "
              f"{np.max(t):8.2f} {np.std(t):8.2f} {speedup:10.2f}x")
    
    print("\nSpeedup Summary:")
    print(f"  Scalar C vs NumPy:    {np.median(times['NumPy'])/np.median(times['Scalar C']):.2f}x")
    print(f"  SIMD C vs NumPy:      {np.median(times['NumPy'])/np.median(times['SIMD C']):.2f}x")
    print(f"  Accelerate vs NumPy:  {np.median(times['NumPy'])/np.median(times['Accelerate']):.2f}x")
    print(f"  Accelerate vs Scalar: {np.median(times['Scalar C'])/np.median(times['Accelerate']):.2f}x")
    print(f"  Accelerate vs SIMD:   {np.median(times['SIMD C'])/np.median(times['Accelerate']):.2f}x")


if __name__ == "__main__":
    benchmark_all()
    print()
    benchmark_detailed()
