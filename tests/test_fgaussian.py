"""
Unit tests for fgaussian module
"""

import numpy as np
import pytest
from ftools import fgaussian


class TestGaussianBasic:
    """Basic functionality tests"""
    
    def test_scalar_inputs(self):
        """Test with scalar inputs"""
        result = fgaussian(0.0, i0=1.0, mu=0.0, sigma=1.0)
        assert isinstance(result, float)
        assert result == pytest.approx(1.0)
    
    def test_array_input(self):
        """Test with array input"""
        x = np.array([-1.0, 0.0, 1.0])
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=1.0)
        assert isinstance(result, np.ndarray)
        assert result.shape == (3,)
        assert result[1] == pytest.approx(1.0)  # Peak at mu=0
    
    def test_peak_location(self):
        """Test that peak is at mu"""
        x = np.linspace(-10, 10, 1000)
        result = fgaussian(x, i0=2.5, mu=3.0, sigma=1.5)
        
        peak_idx = np.argmax(result)
        peak_x = x[peak_idx]
        
        assert peak_x == pytest.approx(3.0, abs=0.1)
        assert result[peak_idx] == pytest.approx(2.5, rel=0.01)
    
    def test_symmetry(self):
        """Test Gaussian is symmetric around mu"""
        x = np.linspace(-5, 5, 1001)
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=1.0)
        
        # Compare left and right halves
        mid = 500
        left = result[:mid]
        right = result[mid+1:][::-1]
        
        np.testing.assert_allclose(left, right, rtol=1e-10)
    
    def test_fwhm(self):
        """Test Full Width at Half Maximum"""
        x = np.linspace(-10, 10, 10000)
        sigma = 2.0
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=sigma)
        
        # FWHM = 2 * sqrt(2 * ln(2)) * sigma ? 2.355 * sigma
        expected_fwhm = 2.355 * sigma
        
        half_max = 0.5
        above_half = x[result >= half_max]
        measured_fwhm = above_half[-1] - above_half[0]
        
        assert measured_fwhm == pytest.approx(expected_fwhm, rel=0.01)


class TestGaussianParameters:
    """Test different parameter values"""
    
    def test_different_amplitudes(self):
        """Test i0 parameter"""
        x = np.array([0.0])
        
        assert fgaussian(x, i0=1.0, mu=0.0, sigma=1.0)[0] == pytest.approx(1.0)
        assert fgaussian(x, i0=2.0, mu=0.0, sigma=1.0)[0] == pytest.approx(2.0)
        assert fgaussian(x, i0=0.5, mu=0.0, sigma=1.0)[0] == pytest.approx(0.5)
    
    def test_different_centers(self):
        """Test mu parameter"""
        for mu in [-5.0, 0.0, 5.0, 10.0]:
            result = fgaussian(mu, i0=1.0, mu=mu, sigma=1.0)
            assert result == pytest.approx(1.0)
    
    def test_different_widths(self):
        """Test sigma parameter"""
        x = np.array([1.0])  # One sigma away from mu=0
        
        result1 = fgaussian(x, i0=1.0, mu=0.0, sigma=1.0)
        result2 = fgaussian(x, i0=1.0, mu=0.0, sigma=2.0)
        
        # Wider Gaussian should have higher value at x=1
        assert result2 > result1
        
        # At x = 1*sigma, value should be exp(-0.5)
        assert result1 == pytest.approx(np.exp(-0.5))


class TestGaussianValidation:
    """Test input validation"""
    
    def test_zero_sigma_raises(self):
        """Sigma = 0 should raise ValueError"""
        with pytest.raises(ValueError, match="sigma must be positive"):
            fgaussian(0.0, i0=1.0, mu=0.0, sigma=0.0)
    
    def test_negative_sigma_raises(self):
        """Negative sigma should raise ValueError"""
        with pytest.raises(ValueError, match="sigma must be positive"):
            fgaussian(0.0, i0=1.0, mu=0.0, sigma=-1.0)
    
    def test_array_sigma_raises(self):
        """Array sigma should raise ValueError"""
        x = np.linspace(0, 1, 10)
        sigma = np.ones(10)
        
        with pytest.raises(ValueError, match="must be scalars"):
            fgaussian(x, i0=1.0, mu=0.0, sigma=sigma)


class TestGaussianNumerical:
    """Test numerical accuracy"""
    
    def test_matches_numpy(self):
        """Compare with NumPy implementation"""
        x = np.linspace(-10, 10, 1000)
        i0, mu, sigma = 2.5, 1.5, 3.0
        
        result = fgaussian(x, i0=i0, mu=mu, sigma=sigma)
        expected = i0 * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
        
        # Float32 has lower precision than float64
        np.testing.assert_allclose(result, expected, rtol=1e-6)
    
    def test_extreme_values(self):
        """Test with extreme x values"""
        x = np.array([-1e6, -100, 0, 100, 1e6])
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=1.0)
        
        # Far from center should be ~0
        assert result[0] == pytest.approx(0.0, abs=1e-300)
        assert result[-1] == pytest.approx(0.0, abs=1e-300)
        
        # Center should be 1.0
        assert result[2] == pytest.approx(1.0)
    
    def test_large_sigma(self):
        """Test with large sigma (nearly flat)"""
        x = np.linspace(-10, 10, 100)
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=1000.0)
        
        # Should be nearly constant ~1.0 over this range
        assert np.std(result) < 0.001
        assert np.mean(result) == pytest.approx(1.0, rel=0.001)
    
    def test_small_sigma(self):
        """Test with small sigma (narrow peak)"""
        x = np.linspace(-1, 1, 10000)
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=0.01)
        
        # Most values should be near 0
        near_zero = np.sum(result < 0.01)
        assert near_zero > 9500  # More than 95% near zero


class TestGaussianTypes:
    """Test type handling"""
    
    def test_int_input(self):
        """Test with integer input"""
        result = fgaussian(0, i0=1.0, mu=0.0, sigma=1.0)
        assert isinstance(result, float)
        assert result == pytest.approx(1.0)
    
    def test_int_array_input(self):
        """Test with integer array"""
        x = np.array([0, 1, 2], dtype=np.int32)
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=1.0)
        
        assert result.dtype == np.float32
        assert result[0] == pytest.approx(1.0)
    
    def test_float32_input(self):
        """Test with float32 input"""
        x = np.array([0.0, 1.0, 2.0], dtype=np.float32)
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=1.0)
        
        # Returns float32
        assert result.dtype == np.float32
    
    def test_list_input(self):
        """Test with list input"""
        x = [0.0, 1.0, 2.0]
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=1.0)
        
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float32


class TestGaussianEdgeCases:
    """Test edge cases"""
    
    def test_empty_array(self):
        """Test with empty array"""
        x = np.array([])
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=1.0)
        
        assert result.shape == (0,)
    
    def test_single_element(self):
        """Test with single element array"""
        x = np.array([5.0])
        result = fgaussian(x, i0=2.0, mu=5.0, sigma=1.5)
        
        assert result.shape == (1,)
        assert result[0] == pytest.approx(2.0)
    
    def test_large_array(self):
        """Test with large array"""
        n = 1_000_000
        x = np.linspace(-100, 100, n)
        result = fgaussian(x, i0=1.0, mu=0.0, sigma=10.0)
        
        assert result.shape == (n,)
        assert result.dtype == np.float32
        
        # Check peak
        peak_idx = np.argmax(result)
        assert result[peak_idx] == pytest.approx(1.0, rel=1e-6)
