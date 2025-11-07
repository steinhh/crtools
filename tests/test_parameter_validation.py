"""Parameter validation and error handling tests for ftools."""
import numpy as np
import pytest

from ftools import fmedian, fsigma


class TestFmedianParameterValidation:
    """Test parameter validation for fmedian."""
    
    def test_fmedian_negative_xsize(self):
        """Test fmedian rejects negative xsize."""
        a = np.ones((3, 3), dtype=np.float64)
        with pytest.raises((ValueError, RuntimeError, MemoryError)):
            fmedian(a, (-1, 1))
    
    def test_fmedian_negative_ysize(self):
        """Test fmedian rejects negative ysize."""
        a = np.ones((3, 3), dtype=np.float64)
        with pytest.raises((ValueError, RuntimeError, MemoryError)):
            fmedian(a, (1, -1))
    
    def test_fmedian_invalid_exclude_center(self):
        """Test fmedian with invalid exclude_center values."""
        a = np.ones((3, 3), dtype=np.float64)
        # Non-0/1 values for exclude_center should work (treated as boolean)
        out = fmedian(a, (1, 1), exclude_center=2)
        assert out.shape == (3, 3)
    
    def test_fmedian_none_parameters(self):
        """Test fmedian rejects None parameters."""
        a = np.ones((3, 3), dtype=np.float64)

        # None for window_size should raise TypeError
        with pytest.raises(TypeError):
            fmedian(a, None)  # NOSONAR - intentionally testing invalid input
        
        # Tuple with None elements should raise an error
        with pytest.raises((TypeError, ValueError)):
            fmedian(a, (None, 1))  # NOSONAR - intentionally testing invalid input

    def test_fmedian_non_integer_parameters(self):
        """Test fmedian handles float parameters (should convert to int)."""
        a = np.ones((3, 3), dtype=np.float64)
        # Float values in tuple should work (will be converted to int by underlying functions)
        result = fmedian(a, (1.0, 1.0))
        assert result.shape == (3, 3)
    
    def test_fmedian_empty_array(self):
        """Test fmedian with empty array."""
        a = np.array([], dtype=np.float64).reshape(0, 0)
        # Should either work or raise a clear error
        try:
            out = fmedian(a, (1, 1), 1)
            assert out.shape == (0, 0)
        except (ValueError, RuntimeError):
            pass  # Acceptable to reject empty arrays
    
    def test_fmedian_3d_array(self):
        """Test fmedian accepts 3D arrays with 3-tuple window_size."""
        a = np.ones((3, 3, 3), dtype=np.float64)
        # Should work with 3-tuple
        result = fmedian(a, (1, 1, 1))
        assert result.shape == (3, 3, 3)
        
        # Should fail with 2-tuple for 3D array (dispatches to 2D function)
        with pytest.raises(ValueError, match="Arrays must be 2-dimensional"):
            fmedian(a, (1, 1))
    
    def test_fmedian_no_input(self):
        """Test fmedian raises TypeError when called with no arguments."""
        with pytest.raises(TypeError):
            fmedian()  # NOSONAR - intentionally testing invalid input
    
    def test_fmedian_missing_parameters(self):
        """Test fmedian raises TypeError when called with too few arguments.""" 
        a = np.ones((3, 3), dtype=np.float64)
        # These should still raise TypeError for missing required parameters
        with pytest.raises(TypeError):
            fmedian()  # NOSONAR - intentionally testing invalid input
        
        with pytest.raises(TypeError):
            fmedian(a)  # NOSONAR - intentionally testing invalid input
        
        with pytest.raises(TypeError):
            fmedian(a, 1)  # NOSONAR - intentionally testing invalid input
class TestFsigmaParameterValidation:
    """Test parameter validation for fsigma."""
    
    def test_fsigma_negative_xsize(self):
        """Test fsigma rejects negative xsize."""
        a = np.ones((3, 3), dtype=np.float64)
        with pytest.raises((ValueError, RuntimeError, MemoryError)):
            fsigma(a, (-1, 1))
    
    def test_fsigma_negative_ysize(self):
        """Test fsigma rejects negative ysize."""
        a = np.ones((3, 3), dtype=np.float64)
        with pytest.raises((ValueError, RuntimeError, MemoryError)):
            fsigma(a, (1, -1))
    
    def test_fsigma_invalid_exclude_center(self):
        """Test fsigma with invalid exclude_center values."""
        a = np.ones((3, 3), dtype=np.float64)
        # Non-0/1 values for exclude_center should work (treated as boolean)
        out = fsigma(a, (1, 1), exclude_center=2)
        assert out.shape == (3, 3)
    
    def test_fsigma_none_parameters(self):
        """Test fsigma rejects None parameters."""
        a = np.ones((3, 3), dtype=np.float64)
        
        # None for window_size should raise TypeError
        with pytest.raises(TypeError):
            fsigma(a, None)  # NOSONAR - intentionally testing invalid input
        
        # Tuple with None elements should raise an error
        with pytest.raises((TypeError, ValueError)):
            fsigma(a, (None, 1))  # NOSONAR - intentionally testing invalid input

    def test_fsigma_non_integer_parameters(self):
        """Test fsigma handles float parameters (should convert to int)."""
        a = np.ones((3, 3), dtype=np.float64)
        # Float values in tuple should work (will be converted to int by underlying functions)
        result = fsigma(a, (1.0, 1.0))
        assert result.shape == (3, 3)

    def test_fsigma_empty_array(self):
        """Test fsigma with empty array."""
        a = np.array([], dtype=np.float64).reshape(0, 0)
        # Should either work or raise a clear error
        try:
            out = fsigma(a, (1, 1), 1)
            assert out.shape == (0, 0)
        except (ValueError, RuntimeError):
            pass  # Acceptable to reject empty arrays
    
    def test_fsigma_3d_array(self):
        """Test fsigma accepts 3D arrays with 3-tuple window_size."""
        a = np.ones((3, 3, 3), dtype=np.float64)
        # Should work with 3-tuple
        result = fsigma(a, (1, 1, 1))
        assert result.shape == (3, 3, 3)
        
        # Should fail with 2-tuple for 3D array (dispatches to 2D function)
        with pytest.raises(ValueError, match="Arrays must be 2-dimensional"):
            fsigma(a, (1, 1))
    
    def test_fsigma_no_input(self):
        """Test fsigma raises TypeError when called with no arguments."""
        with pytest.raises(TypeError):
            fsigma()  # NOSONAR - intentionally testing invalid input
    
    def test_fsigma_missing_parameters(self):
        """Test fsigma raises TypeError when called with too few arguments."""
        a = np.ones((3, 3), dtype=np.float64)
        # These should still raise TypeError for missing required parameters
        with pytest.raises(TypeError):
            fsigma()  # NOSONAR - intentionally testing invalid input
        
        with pytest.raises(TypeError):
            fsigma(a)  # NOSONAR - intentionally testing invalid input
        
        with pytest.raises(TypeError):
            fsigma(a, 1)  # NOSONAR - intentionally testing invalid input


class TestBothFunctions:
    """Test both functions together for consistency."""
    
    def test_consistent_shapes(self):
        """Test both functions return consistent shapes."""
        rng = np.random.default_rng(42)
        a = rng.standard_normal((10, 10)).astype(np.float64)
        
        med = fmedian(a, (1, 1), 1)
        sig = fsigma(a, (1, 1), 1)
        
        assert med.shape == sig.shape == a.shape
    
    def test_consistent_dtypes(self):
        """Test both functions return float64."""
        a = np.ones((5, 5), dtype=np.float64)
        
        med = fmedian(a, (1, 1), 1)
        sig = fsigma(a, (1, 1), 1)
        
        assert med.dtype == sig.dtype == np.float64
    
    def test_accept_same_window_sizes(self):
        """Test both functions accept the same window size parameters."""
        rng = np.random.default_rng(123)
        a = rng.standard_normal((7, 7)).astype(np.float64)
        
        # Only test odd window sizes since that's what the new API requires
        for xsize in [1, 3, 5]:
            for ysize in [1, 3, 5]:
                med = fmedian(a, (xsize, ysize), 1)
                sig = fsigma(a, (xsize, ysize), 1)
                assert med.shape == sig.shape == a.shape
