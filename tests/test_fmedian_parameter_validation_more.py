import numpy as np
import pytest

from ftools import fmedian
from ftools.fmedian3 import fmedian3


def test_fmedian_requires_x_y_sizes_not_none():
    a = np.ones((3, 3), dtype=np.float64)
    with pytest.raises(TypeError):
        fmedian(a, None, None)


def test_fmedian_rejects_zero_or_negative_sizes():
    a = np.ones((3, 3), dtype=np.float64)
    # Zero triggers the odd-number check (0 is even)
    with pytest.raises(ValueError, match="xsize must be an odd number"):
        fmedian(a, (0, 3), 0)
    with pytest.raises(ValueError, match="ysize must be an odd number"):
        fmedian(a, (3, 0), 0)
    # Negative sizes will pass the odd-number check in Python (e.g. -1 % 2 == 1)
    # and should trigger the positive-size validation
    with pytest.raises(ValueError, match="xsize must be positive"):
        fmedian(a, (-1, 3), 0)


def test_fmedian_accepts_non_int_but_coerces():
    a = np.ones((3, 3), dtype=np.float64)
    # floats that are integer-like should be coerced to ints
    out = fmedian(a, (3.0, 3.0), 0)
    assert out.shape == a.shape


def test_exclude_center_coerced_to_int():
    a = np.ones((3, 3), dtype=np.float64)
    # exclude_center provided as truthy string should be coerced (via int()) and accepted
    out = fmedian(a, (3, 3), True)
    assert out.shape == a.shape


def test_fmedian3_negative_ysize_and_zsize_rejected():
    a3 = np.ones((3, 3, 3), dtype=np.float64)
    # Negative ysize should trigger positive-size validation
    with pytest.raises(ValueError, match="ysize must be positive"):
        fmedian3(a3, 3, -1, 3, 0)

    # Negative zsize should trigger positive-size validation
    with pytest.raises(ValueError, match="zsize must be positive"):
        fmedian3(a3, 3, 3, -1, 0)
