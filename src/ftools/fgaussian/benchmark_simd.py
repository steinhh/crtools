"""
Benchmark: NumPy vs Scalar C vs SIMD C
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import numpy as np
import time
from ftools.fgaussian import fgaussian_ext, fgaussian_simd_ext


def benchmark_comparison():
    """Compare all three implementations"""
    print("Performance Comparison: NumPy vs Scalar C vs SIMD C")
    print("=" * 80)
    print(f"{'Size':>12} {'NumPy (ms)':>12} {'Scalar C':>12} {'SIMD C':>12} {'C Speedup':>12} {'SIMD Speedup':>12}")
    print("-" * 80)
    
    sizes = [1000, 10_000, 100_000, 1_000_000, 10_000_000]
    
    for n in sizes:
        x = np.linspace(-100, 100, n, dtype=np.float64)
        i0, mu, sigma = 1.0, 0.0, 10.0
        
        # Warm up
        _ = i0 * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
        _ = fgaussian_ext.gaussian(x, i0, mu, sigma)
        _ = fgaussian_simd_ext.gaussian(x, i0, mu, sigma)
        
        # Benchmark NumPy
        times_np = []
        for _ in range(20):
            start = time.time()
            result_np = i0 * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
            times_np.append(time.time() - start)
        time_np = np.median(times_np) * 1000
        
        # Benchmark Scalar C
        times_scalar = []
        for _ in range(20):
            start = time.time()
            result_scalar = fgaussian_ext.gaussian(x, i0, mu, sigma)
            times_scalar.append(time.time() - start)
        time_scalar = np.median(times_scalar) * 1000
        
        # Benchmark SIMD C
        times_simd = []
        for _ in range(20):
            start = time.time()
            result_simd = fgaussian_simd_ext.gaussian(x, i0, mu, sigma)
            times_simd.append(time.time() - start)
        time_simd = np.median(times_simd) * 1000
        
        # Verify results match
        max_diff_scalar = np.max(np.abs(result_np - result_scalar))
        max_diff_simd = np.max(np.abs(result_np - result_simd))
        
        speedup_scalar = time_np / time_scalar
        speedup_simd = time_np / time_simd
        
        print(f"{n:12,} {time_np:12.3f} {time_scalar:12.3f} {time_simd:12.3f} "
              f"{speedup_scalar:12.2f}x {speedup_simd:12.2f}x")
        
        # Check accuracy for first size
        if n == 1000:
            print(f"\nAccuracy check (n={n}):")
            print(f"  Scalar C max diff: {max_diff_scalar:.2e}")
            print(f"  SIMD C max diff:   {max_diff_simd:.2e}")
            print()


def benchmark_detailed_simd():
    """Detailed SIMD performance analysis"""
    print("\nDetailed SIMD Analysis (10M elements)")
    print("=" * 80)
    
    n = 10_000_000
    x = np.linspace(-100, 100, n, dtype=np.float64)
    i0, mu, sigma = 1.0, 0.0, 10.0
    
    # Multiple runs for statistics
    n_runs = 50
    
    times_np = []
    times_scalar = []
    times_simd = []
    
    for _ in range(n_runs):
        # NumPy
        start = time.time()
        _ = i0 * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
        times_np.append((time.time() - start) * 1000)
        
        # Scalar C
        start = time.time()
        _ = fgaussian_ext.gaussian(x, i0, mu, sigma)
        times_scalar.append((time.time() - start) * 1000)
        
        # SIMD C
        start = time.time()
        _ = fgaussian_simd_ext.gaussian(x, i0, mu, sigma)
        times_simd.append((time.time() - start) * 1000)
    
    print(f"NumPy:     min={np.min(times_np):6.2f} median={np.median(times_np):6.2f} "
          f"mean={np.mean(times_np):6.2f} max={np.max(times_np):6.2f} ms")
    print(f"Scalar C:  min={np.min(times_scalar):6.2f} median={np.median(times_scalar):6.2f} "
          f"mean={np.mean(times_scalar):6.2f} max={np.max(times_scalar):6.2f} ms")
    print(f"SIMD C:    min={np.min(times_simd):6.2f} median={np.median(times_simd):6.2f} "
          f"mean={np.mean(times_simd):6.2f} max={np.max(times_simd):6.2f} ms")
    
    print(f"\nSpeedup vs NumPy:")
    print(f"  Scalar C: {np.median(times_np)/np.median(times_scalar):.2f}x")
    print(f"  SIMD C:   {np.median(times_np)/np.median(times_simd):.2f}x")
    print(f"\nSIMD vs Scalar C: {np.median(times_scalar)/np.median(times_simd):.2f}x")


if __name__ == "__main__":
    benchmark_comparison()
    benchmark_detailed_simd()
