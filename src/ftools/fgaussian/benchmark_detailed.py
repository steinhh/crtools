"""
Detailed benchmark to understand performance characteristics
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import numpy as np
import time
from ftools.fgaussian import gaussian


def benchmark_sizes():
    """Benchmark different array sizes"""
    print("Performance vs Array Size")
    print("=" * 70)
    print(f"{'Size':>12} {'C (ms)':>10} {'NumPy (ms)':>12} {'Speedup':>10}")
    print("-" * 70)
    
    sizes = [100, 1000, 10_000, 100_000, 1_000_000, 10_000_000]
    
    for n in sizes:
        x = np.linspace(-100, 100, n)
        
        # Warm up
        _ = gaussian(x, i0=1.0, mu=0.0, sigma=10.0)
        _ = 1.0 * np.exp(-((x - 0.0) ** 2) / (2 * 10.0 ** 2))
        
        # Benchmark C
        times_c = []
        for _ in range(20):
            start = time.time()
            result_c = gaussian(x, i0=1.0, mu=0.0, sigma=10.0)
            times_c.append(time.time() - start)
        time_c = np.median(times_c) * 1000  # Convert to ms
        
        # Benchmark NumPy
        times_np = []
        for _ in range(20):
            start = time.time()
            result_np = 1.0 * np.exp(-((x - 0.0) ** 2) / (2 * 10.0 ** 2))
            times_np.append(time.time() - start)
        time_np = np.median(times_np) * 1000  # Convert to ms
        
        speedup = time_np / time_c
        print(f"{n:12,} {time_c:10.3f} {time_np:12.3f} {speedup:10.2f}x")


def benchmark_operations():
    """Break down NumPy operations"""
    print("\nNumPy Operation Breakdown (10M elements)")
    print("=" * 70)
    
    n = 10_000_000
    x = np.linspace(-100, 100, n)
    mu = 0.0
    sigma = 10.0
    i0 = 1.0
    
    # Warm up
    _ = x - mu
    
    # Subtraction
    times = []
    for _ in range(20):
        start = time.time()
        t1 = x - mu
        times.append(time.time() - start)
    print(f"x - mu:           {np.median(times)*1000:8.3f} ms")
    
    # Squaring
    t1 = x - mu
    times = []
    for _ in range(20):
        start = time.time()
        t2 = t1 ** 2
        times.append(time.time() - start)
    print(f"t1**2:            {np.median(times)*1000:8.3f} ms")
    
    # Division
    t2 = t1 ** 2
    denom = 2 * sigma ** 2
    times = []
    for _ in range(20):
        start = time.time()
        t3 = t2 / denom
        times.append(time.time() - start)
    print(f"t2 / denom:       {np.median(times)*1000:8.3f} ms")
    
    # Negation
    t3 = t2 / denom
    times = []
    for _ in range(20):
        start = time.time()
        t4 = -t3
        times.append(time.time() - start)
    print(f"-t3:              {np.median(times)*1000:8.3f} ms")
    
    # Exp
    t4 = -t3
    times = []
    for _ in range(20):
        start = time.time()
        t5 = np.exp(t4)
        times.append(time.time() - start)
    print(f"np.exp(t4):       {np.median(times)*1000:8.3f} ms")
    
    # Multiplication
    t5 = np.exp(t4)
    times = []
    for _ in range(20):
        start = time.time()
        result = i0 * t5
        times.append(time.time() - start)
    print(f"i0 * t5:          {np.median(times)*1000:8.3f} ms")
    
    # Total with temporaries
    times = []
    for _ in range(20):
        start = time.time()
        result = i0 * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
        times.append(time.time() - start)
    print(f"\nTotal (chained):  {np.median(times)*1000:8.3f} ms")
    
    # C extension
    times = []
    for _ in range(20):
        start = time.time()
        result_c = gaussian(x, i0=i0, mu=mu, sigma=sigma)
        times.append(time.time() - start)
    print(f"C extension:      {np.median(times)*1000:8.3f} ms")


def benchmark_memory_patterns():
    """Test different memory access patterns"""
    print("\nMemory Access Patterns (1M elements)")
    print("=" * 70)
    
    n = 1_000_000
    
    # Contiguous
    x = np.linspace(-100, 100, n)
    times = []
    for _ in range(50):
        start = time.time()
        result = gaussian(x, i0=1.0, mu=0.0, sigma=10.0)
        times.append(time.time() - start)
    print(f"Contiguous array: {np.median(times)*1000:8.3f} ms")
    
    # Strided (every other element)
    x_strided = np.linspace(-100, 100, n*2)[::2]
    times = []
    for _ in range(50):
        start = time.time()
        result = gaussian(x_strided, i0=1.0, mu=0.0, sigma=10.0)
        times.append(time.time() - start)
    print(f"Strided (step=2): {np.median(times)*1000:8.3f} ms")
    
    # Non-contiguous (transpose creates copy in C extension)
    x_2d = np.linspace(-100, 100, n).reshape(1000, 1000)
    times = []
    for _ in range(50):
        start = time.time()
        result = gaussian(x_2d, i0=1.0, mu=0.0, sigma=10.0)
        times.append(time.time() - start)
    print(f"2D contiguous:    {np.median(times)*1000:8.3f} ms")


if __name__ == "__main__":
    benchmark_sizes()
    benchmark_operations()
    benchmark_memory_patterns()
