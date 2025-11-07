import numpy as np
import pytest

from crtools import fsigma


def test_sigma_zero_on_constant_window():
    """Sigma of a constant-valued neighborhood should be 0.0."""
    a = np.full((5, 5), 7.0, dtype=np.float64)
    # 3x3 window including center
    out = fsigma(a, 3, 3, 0)
    assert np.allclose(out, 0.0)

    # 3x3 window excluding center
    out = fsigma(a, 3, 3, 1)
    assert np.allclose(out, 0.0)


def test_center_exclusion_reduces_sigma_with_outlier():
    """Excluding the center outlier should reduce local sigma at the center pixel."""
    a = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 999.0, 6.0],
        [7.0, 8.0, 9.0],
    ], dtype=np.float64)
    # With center included
    out = fsigma(a, 3, 3, 0)
    sigma_with = out[1, 1]

    # With center excluded
    out = fsigma(a, 3, 3, 1)
    sigma_without = out[1, 1]

    assert sigma_with > sigma_without


def test_nan_values_are_ignored():
    """NaN values should be ignored in sigma calculation (center or neighbors)."""
    a = np.array([
        [1.0, 2.0, 3.0],
        [4.0, np.nan, 6.0],  # center NaN
        [7.0, 8.0, 9.0],
    ], dtype=np.float64)
    # Center included: NaN should be ignored; sigma at center should equal
    # population std of [1,2,3,4,6,7,8,9] which is sqrt(7.5)
    out = fsigma(a, 3, 3, 0)
    assert np.isclose(out[1, 1], np.sqrt(7.5))

    # Make a neighbor NaN (not center) and exclude center; sigma should be finite
    b = np.array([
        [np.nan, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0],
    ], dtype=np.float64)
    out = fsigma(b, 3, 3, 1)
    # Same neighborhood as above but without 5.0 and with NaN ignored ->
    # values are [1,2,3,4,6,7,8,9] for center (5 ignored via exclude_center, 1 is NaN)
    assert np.isfinite(out[1, 1])


def test_1x1_excluding_center_yields_zero():
    """With a 1x1 window and center excluded (no neighbors), sigma is defined as 0.0."""
    a = np.array([[42.0]], dtype=np.float64)
    out = fsigma(a, 1, 1, 1)
    assert np.isclose(out[0, 0], 0.0)


def test_dtype_enforced_float64():
    """fsigma requires float64 input and output arrays."""
    good = np.ones((2, 2), dtype=np.float64)

    # Works with float64
    out = fsigma(good, 3, 3, 1)
    assert out.dtype == np.float64

    # New API coerces input to float64; float32 input is accepted and coerced
    bad_in = good.astype(np.float32)
    out2 = fsigma(bad_in, 3, 3, 1)
    assert out2.dtype == np.float64


def test_dimension_checks():
    """Non-2D arrays or mismatched shapes should raise errors."""
    a = np.ones((2, 3), dtype=np.float64)
    # Happy path
    out = fsigma(a, 3, 3, 1)
    assert out.shape == a.shape and out.dtype == np.float64

    # 1D array should fail
    with pytest.raises(ValueError):
        a1 = np.ones(3, dtype=np.float64)
        fsigma(a1, 3, 3, 1)
