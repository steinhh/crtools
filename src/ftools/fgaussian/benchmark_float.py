"""
Benchmark: Float32 vs Float64 performance
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import numpy as np
import time
from ftools.fgaussian import (fgaussian_ext, fgaussian_accelerate_ext, 
                               fgaussian_float_ext)


def benchmark_float_vs_double():
    """Compare float32 vs float64 performance"""
    print("Float32 vs Float64 Performance Comparison")
    print("=" * 110)
    print(f"{'Size':>12} {'NumPy f64':>12} {'Accel f64':>12} {'NumPy f32':>12} {'Accel f32':>12} "
          f"{'f64 Speed':>11} {'f32 Speed':>11} {'f32 Gain':>11}")
    print(f"{'':>12} {'(ms)':>12} {'(ms)':>12} {'(ms)':>12} {'(ms)':>12} "
          f"{'up':>11} {'up':>11} {'vs f64':>11}")
    print("-" * 110)
    
    sizes = [1000, 10_000, 100_000, 1_000_000, 10_000_000]
    
    for n in sizes:
        # Float64 data
        x_f64 = np.linspace(-100, 100, n, dtype=np.float64)
        # Float32 data
        x_f32 = np.linspace(-100, 100, n, dtype=np.float32)
        
        i0, mu, sigma = 1.0, 0.0, 10.0
        
        # Warm up
        _ = i0 * np.exp(-((x_f64 - mu) ** 2) / (2 * sigma ** 2))
        _ = fgaussian_accelerate_ext.gaussian(x_f64, i0, mu, sigma)
        _ = i0 * np.exp(-((x_f32 - mu) ** 2) / (2 * sigma ** 2))
        _ = fgaussian_float_ext.gaussian(x_f32, i0, mu, sigma)
        
        n_runs = 20 if n <= 1_000_000 else 10
        
        # Benchmark NumPy float64
        times = []
        for _ in range(n_runs):
            start = time.time()
            _ = i0 * np.exp(-((x_f64 - mu) ** 2) / (2 * sigma ** 2))
            times.append(time.time() - start)
        time_np_f64 = np.median(times) * 1000
        
        # Benchmark Accelerate float64
        times = []
        for _ in range(n_runs):
            start = time.time()
            _ = fgaussian_accelerate_ext.gaussian(x_f64, i0, mu, sigma)
            times.append(time.time() - start)
        time_accel_f64 = np.median(times) * 1000
        
        # Benchmark NumPy float32
        times = []
        for _ in range(n_runs):
            start = time.time()
            _ = i0 * np.exp(-((x_f32 - mu) ** 2) / (2 * sigma ** 2))
            times.append(time.time() - start)
        time_np_f32 = np.median(times) * 1000
        
        # Benchmark Accelerate float32
        times = []
        for _ in range(n_runs):
            start = time.time()
            _ = fgaussian_float_ext.gaussian(x_f32, i0, mu, sigma)
            times.append(time.time() - start)
        time_accel_f32 = np.median(times) * 1000
        
        # Accuracy check
        if n == 1000:
            result_f64 = i0 * np.exp(-((x_f64 - mu) ** 2) / (2 * sigma ** 2))
            result_f32_np = i0 * np.exp(-((x_f32 - mu) ** 2) / (2 * sigma ** 2))
            result_f32_c = fgaussian_float_ext.gaussian(x_f32, i0, mu, sigma)
            
            # Compare f32 to f64 (convert to same type)
            diff_np = np.max(np.abs(result_f64 - result_f32_np.astype(np.float64)))
            diff_c = np.max(np.abs(result_f64 - result_f32_c.astype(np.float64)))
            
            print(f"\nAccuracy (n={n}):")
            print(f"  NumPy f32 vs f64:     {diff_np:.2e}")
            print(f"  Accelerate f32 vs f64: {diff_c:.2e}\n")
        
        speedup_f64 = time_np_f64 / time_accel_f64
        speedup_f32 = time_np_f32 / time_accel_f32
        gain_f32_vs_f64 = time_accel_f64 / time_accel_f32
        
        print(f"{n:12,} {time_np_f64:12.3f} {time_accel_f64:12.3f} {time_np_f32:12.3f} {time_accel_f32:12.3f} "
              f"{speedup_f64:11.2f}x {speedup_f32:11.2f}x {gain_f32_vs_f64:11.2f}x")
    
    print()


def benchmark_detailed_float():
    """Detailed float32 analysis"""
    print("Detailed Float32 Statistics (10M elements, 50 runs)")
    print("=" * 95)
    
    n = 10_000_000
    x_f64 = np.linspace(-100, 100, n, dtype=np.float64)
    x_f32 = np.linspace(-100, 100, n, dtype=np.float32)
    i0, mu, sigma = 1.0, 0.0, 10.0
    
    n_runs = 50
    
    times = {
        'NumPy f64': [],
        'Scalar C f64': [],
        'Accel f64': [],
        'NumPy f32': [],
        'Accel f32': []
    }
    
    for _ in range(n_runs):
        start = time.time()
        _ = i0 * np.exp(-((x_f64 - mu) ** 2) / (2 * sigma ** 2))
        times['NumPy f64'].append((time.time() - start) * 1000)
        
        start = time.time()
        _ = fgaussian_ext.gaussian(x_f64, i0, mu, sigma)
        times['Scalar C f64'].append((time.time() - start) * 1000)
        
        start = time.time()
        _ = fgaussian_accelerate_ext.gaussian(x_f64, i0, mu, sigma)
        times['Accel f64'].append((time.time() - start) * 1000)
        
        start = time.time()
        _ = i0 * np.exp(-((x_f32 - mu) ** 2) / (2 * sigma ** 2))
        times['NumPy f32'].append((time.time() - start) * 1000)
        
        start = time.time()
        _ = fgaussian_float_ext.gaussian(x_f32, i0, mu, sigma)
        times['Accel f32'].append((time.time() - start) * 1000)
    
    print(f"{'Method':>18} {'Min':>8} {'Median':>8} {'Mean':>8} {'Max':>8} {'Std':>8} {'vs NumPy f64':>13}")
    print("-" * 95)
    
    for name in ['NumPy f64', 'Scalar C f64', 'Accel f64', 'NumPy f32', 'Accel f32']:
        t = np.array(times[name])
        speedup = np.median(times['NumPy f64']) / np.median(t)
        print(f"{name:>18} {np.min(t):8.2f} {np.median(t):8.2f} {np.mean(t):8.2f} "
              f"{np.max(t):8.2f} {np.std(t):8.2f} {speedup:13.2f}x")
    
    print("\nKey Comparisons:")
    print(f"  Accel f64 vs NumPy f64:  {np.median(times['NumPy f64'])/np.median(times['Accel f64']):.2f}x")
    print(f"  Accel f32 vs NumPy f32:  {np.median(times['NumPy f32'])/np.median(times['Accel f32']):.2f}x")
    print(f"  Accel f32 vs Accel f64:  {np.median(times['Accel f64'])/np.median(times['Accel f32']):.2f}x")
    print(f"  NumPy f32 vs NumPy f64:  {np.median(times['NumPy f64'])/np.median(times['NumPy f32']):.2f}x")
    print(f"  BEST (Accel f32) vs NumPy f64: {np.median(times['NumPy f64'])/np.median(times['Accel f32']):.2f}x")


if __name__ == "__main__":
    benchmark_float_vs_double()
    print()
    benchmark_detailed_float()
