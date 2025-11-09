import numpy as np
import pytest

from ftools.fmedian3 import fmedian3
from ftools.fsigma import fsigma
from ftools.fsigma3 import fsigma3


def test_fmedian3_requires_sizes_not_none():
    a = np.ones((3, 3, 3), dtype=np.float64)
    with pytest.raises(TypeError):
        fmedian3(a, None, None, None)


def test_fmedian3_even_size_checks_and_dimension():
    a2 = np.ones((3, 3), dtype=np.float64)
    a3 = np.ones((3, 3, 3), dtype=np.float64)
    # wrong dimensionality (expects 3D input)
    with pytest.raises(ValueError, match="3-dimensional"):
        fmedian3(a2, 3, 3, 3, 0)

    # even sizes trigger odd-number ValueError
    with pytest.raises(ValueError, match="xsize must be an odd number"):
        fmedian3(a3, 2, 3, 3, 0)


def test_fsigma_requires_x_y_sizes_not_none():
    a = np.ones((3, 3), dtype=np.float64)
    with pytest.raises(TypeError):
        fsigma(a, None, None)


def test_fsigma_even_and_positive_checks():
    a = np.ones((3, 3), dtype=np.float64)
    with pytest.raises(ValueError, match="xsize must be an odd number"):
        fsigma(a, 2, 3, 0)
    with pytest.raises(ValueError, match="xsize must be positive"):
        fsigma(a, -1, 3, 0)
    # ysize oddness should be checked as well
    with pytest.raises(ValueError, match="ysize must be an odd number"):
        fsigma(a, 3, 2, 0)


def test_fsigma3_requires_sizes_and_dimension():
    a2 = np.ones((3, 3), dtype=np.float64)
    a3 = np.ones((3, 3, 3), dtype=np.float64)
    with pytest.raises(TypeError):
        fsigma3(a3, None, None, None)
    with pytest.raises(ValueError, match="3-dimensional"):
        fsigma3(a2, 3, 3, 3, 0)
    with pytest.raises(ValueError, match="zsize must be an odd number"):
        fsigma3(a3, 3, 3, 2, 0)


def test_fsigma3_negative_ysize_and_zsize_rejected():
    a3 = np.ones((3, 3, 3), dtype=np.float64)
    # Negative ysize should trigger positive-size validation
    with pytest.raises(ValueError, match="ysize must be positive"):
        fsigma3(a3, 3, -1, 3, 0)

    # Negative zsize should trigger positive-size validation
    with pytest.raises(ValueError, match="zsize must be positive"):
        fsigma3(a3, 3, 3, -1, 0)
