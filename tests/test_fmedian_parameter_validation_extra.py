import numpy as np
import pytest

from ftools import fmedian


def test_fmedian_rejects_even_xsize():
    a = np.ones((4, 4), dtype=np.float64)
    # xsize even should raise ValueError
    with pytest.raises(ValueError, match="xsize must be an odd number"):
        fmedian(a, (2, 3), 0)


def test_fmedian_rejects_even_ysize():
    a = np.ones((4, 4), dtype=np.float64)
    # ysize even should raise ValueError
    with pytest.raises(ValueError, match="ysize must be an odd number"):
        fmedian(a, (3, 2), 0)
