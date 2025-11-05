"""Parameter validation and error handling tests for crtools."""
import numpy as np
import pytest

from crtools import fmedian, fsigma


class TestFmedianParameterValidation:
    """Test parameter validation for fmedian."""
    
    def test_fmedian_negative_xsize(self):
        """Test fmedian rejects negative xsize."""
        a = np.ones((3, 3), dtype=np.float64)
        with pytest.raises((ValueError, RuntimeError, MemoryError)):
            fmedian(a, -1, 1, 1)
    
    def test_fmedian_negative_ysize(self):
        """Test fmedian rejects negative ysize."""
        a = np.ones((3, 3), dtype=np.float64)
        with pytest.raises((ValueError, RuntimeError, MemoryError)):
            fmedian(a, 1, -1, 1)
    
    def test_fmedian_invalid_exclude_center(self):
        """Test fmedian with invalid exclude_center values."""
        a = np.ones((3, 3), dtype=np.float64)
        # Should handle non-0/1 values (likely treating as boolean)
        out = fmedian(a, 1, 1, 2)
        assert out.shape == a.shape
    
    def test_fmedian_none_parameters(self):
        """Test fmedian rejects None parameters."""
        a = np.ones((3, 3), dtype=np.float64)
        
        with pytest.raises(TypeError):
            fmedian(a, None, 1, 1)
        
        with pytest.raises(TypeError):
            fmedian(a, 1, None, 1)
        
        with pytest.raises(TypeError):
            fmedian(a, 1, 1, None)
    
    def test_fmedian_non_integer_parameters(self):
        """Test fmedian handles float parameters (should convert to int)."""
        a = np.ones((3, 3), dtype=np.float64)
        # Should work by converting to int
        out = fmedian(a, 1.5, 1.7, 1.0)
        assert out.shape == a.shape
    
    def test_fmedian_empty_array(self):
        """Test fmedian with empty array."""
        a = np.array([], dtype=np.float64).reshape(0, 0)
        # Should either work or raise a clear error
        try:
            out = fmedian(a, 1, 1, 1)
            assert out.shape == (0, 0)
        except (ValueError, RuntimeError):
            pass  # Acceptable to reject empty arrays
    
    def test_fmedian_3d_array(self):
        """Test fmedian rejects 3D arrays."""
        a = np.ones((3, 3, 3), dtype=np.float64)
        with pytest.raises(ValueError):
            fmedian(a, 1, 1, 1)
    
    def test_fmedian_no_input(self):
        """Test fmedian raises TypeError when called with no arguments."""
        with pytest.raises(TypeError):
            fmedian()
    
    def test_fmedian_missing_parameters(self):
        """Test fmedian raises TypeError when called with too few arguments."""
        a = np.ones((3, 3), dtype=np.float64)
        with pytest.raises(TypeError):
            fmedian(a)
        
        with pytest.raises(TypeError):
            fmedian(a, 1)
        
        with pytest.raises(TypeError):
            fmedian(a, 1, 1)


class TestFsigmaParameterValidation:
    """Test parameter validation for fsigma."""
    
    def test_fsigma_negative_xsize(self):
        """Test fsigma rejects negative xsize."""
        a = np.ones((3, 3), dtype=np.float64)
        with pytest.raises((ValueError, RuntimeError, MemoryError)):
            fsigma(a, -1, 1, 1)
    
    def test_fsigma_negative_ysize(self):
        """Test fsigma rejects negative ysize."""
        a = np.ones((3, 3), dtype=np.float64)
        with pytest.raises((ValueError, RuntimeError, MemoryError)):
            fsigma(a, 1, -1, 1)
    
    def test_fsigma_invalid_exclude_center(self):
        """Test fsigma with invalid exclude_center values."""
        a = np.ones((3, 3), dtype=np.float64)
        # Should handle non-0/1 values (likely treating as boolean)
        out = fsigma(a, 1, 1, 2)
        assert out.shape == a.shape
    
    def test_fsigma_none_parameters(self):
        """Test fsigma rejects None parameters."""
        a = np.ones((3, 3), dtype=np.float64)
        
        with pytest.raises(TypeError):
            fsigma(a, None, 1, 1)
        
        with pytest.raises(TypeError):
            fsigma(a, 1, None, 1)
        
        with pytest.raises(TypeError):
            fsigma(a, 1, 1, None)
    
    def test_fsigma_non_integer_parameters(self):
        """Test fsigma handles float parameters (should convert to int)."""
        a = np.ones((3, 3), dtype=np.float64)
        # Should work by converting to int
        out = fsigma(a, 1.5, 1.7, 1.0)
        assert out.shape == a.shape
    
    def test_fsigma_empty_array(self):
        """Test fsigma with empty array."""
        a = np.array([], dtype=np.float64).reshape(0, 0)
        # Should either work or raise a clear error
        try:
            out = fsigma(a, 1, 1, 1)
            assert out.shape == (0, 0)
        except (ValueError, RuntimeError):
            pass  # Acceptable to reject empty arrays
    
    def test_fsigma_3d_array(self):
        """Test fsigma rejects 3D arrays."""
        a = np.ones((3, 3, 3), dtype=np.float64)
        with pytest.raises(ValueError):
            fsigma(a, 1, 1, 1)
    
    def test_fsigma_no_input(self):
        """Test fsigma raises TypeError when called with no arguments."""
        with pytest.raises(TypeError):
            fsigma()
    
    def test_fsigma_missing_parameters(self):
        """Test fsigma raises TypeError when called with too few arguments."""
        a = np.ones((3, 3), dtype=np.float64)
        with pytest.raises(TypeError):
            fsigma(a)
        
        with pytest.raises(TypeError):
            fsigma(a, 1)
        
        with pytest.raises(TypeError):
            fsigma(a, 1, 1)


class TestBothFunctions:
    """Test both functions together for consistency."""
    
    def test_consistent_shapes(self):
        """Test both functions return consistent shapes."""
        rng = np.random.default_rng(42)
        a = rng.standard_normal((10, 10)).astype(np.float64)
        
        med = fmedian(a, 1, 1, 1)
        sig = fsigma(a, 1, 1, 1)
        
        assert med.shape == sig.shape == a.shape
    
    def test_consistent_dtypes(self):
        """Test both functions return float64."""
        a = np.ones((5, 5), dtype=np.float64)
        
        med = fmedian(a, 1, 1, 1)
        sig = fsigma(a, 1, 1, 1)
        
        assert med.dtype == sig.dtype == np.float64
    
    def test_accept_same_window_sizes(self):
        """Test both functions accept the same window size parameters."""
        rng = np.random.default_rng(123)
        a = rng.standard_normal((7, 7)).astype(np.float64)
        
        for xsize in [0, 1, 2, 3]:
            for ysize in [0, 1, 2, 3]:
                med = fmedian(a, xsize, ysize, 1)
                sig = fsigma(a, xsize, ysize, 1)
                assert med.shape == sig.shape == a.shape
