"""
Tests for fgaussian_f64 (float64 version)
"""

import sys
sys.path.insert(0, 'src')

import numpy as np
import pytest
from ftools import fgaussian_f64


def test_fgaussian_f64_basic():
    """Test basic functionality with float64 input"""
    x = np.linspace(-5, 5, 100, dtype=np.float64)
    result = fgaussian_f64(x, i0=1.0, mu=0.0, sigma=1.0)
    
    assert result.dtype == np.float64
    assert result.shape == x.shape
    assert 0.9 < result.max() < 1.1  # Peak near 1.0


def test_fgaussian_f64_vs_numpy():
    """Test accuracy vs NumPy reference implementation"""
    x = np.linspace(-10, 10, 1000, dtype=np.float64)
    i0, mu, sigma = 1.5, 2.0, 0.8
    
    result = fgaussian_f64(x, i0, mu, sigma)
    expected = i0 * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    
    # Should be nearly identical (within floating point precision)
    np.testing.assert_allclose(result, expected, rtol=1e-14, atol=1e-14)


def test_fgaussian_f64_peak_position():
    """Test that peak is at the correct position"""
    x = np.linspace(-10, 10, 1001, dtype=np.float64)
    mu = 3.0
    result = fgaussian_f64(x, i0=1.0, mu=mu, sigma=1.0)
    
    peak_idx = result.argmax()
    peak_x = x[peak_idx]
    
    # Peak should be very close to mu
    assert abs(peak_x - mu) < 0.05


def test_fgaussian_f64_peak_value():
    """Test that peak value equals i0"""
    x = np.linspace(-5, 5, 1001, dtype=np.float64)
    i0 = 2.5
    result = fgaussian_f64(x, i0=i0, mu=0.0, sigma=1.0)
    
    # Peak value should be close to i0
    assert abs(result.max() - i0) < 0.01


def test_fgaussian_f64_sigma_effect():
    """Test that larger sigma gives wider profile"""
    x = np.linspace(-10, 10, 1000, dtype=np.float64)
    
    result_narrow = fgaussian_f64(x, i0=1.0, mu=0.0, sigma=0.5)
    result_wide = fgaussian_f64(x, i0=1.0, mu=0.0, sigma=2.0)
    
    # Wider profile should have higher values away from center
    assert result_wide[100] > result_narrow[100]
    assert result_wide[900] > result_narrow[900]


def test_fgaussian_f64_requires_float64():
    """Test that function expects float64 input"""
    x_f32 = np.linspace(-5, 5, 100, dtype=np.float32)
    
    # Should accept and convert to float64
    result = fgaussian_f64(x_f32, i0=1.0, mu=0.0, sigma=1.0)
    assert result.dtype == np.float64


def test_fgaussian_f64_invalid_sigma():
    """Test that negative sigma raises error"""
    x = np.linspace(-5, 5, 100, dtype=np.float64)
    
    with pytest.raises(ValueError, match="sigma must be positive"):
        fgaussian_f64(x, i0=1.0, mu=0.0, sigma=-1.0)
    
    with pytest.raises(ValueError, match="sigma must be positive"):
        fgaussian_f64(x, i0=1.0, mu=0.0, sigma=0.0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
