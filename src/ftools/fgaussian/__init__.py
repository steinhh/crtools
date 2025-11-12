"""
Gaussian profile computation module

Provides high-performance computation of Gaussian profiles using C extensions.
Uses float32 for optimal performance (~5x faster than NumPy float64).
"""

import numpy as np
from . import fgaussian_ext


def gaussian(x, i0, mu, sigma):
    """
    Compute Gaussian profile: i0 * exp(-((x - mu)^2) / (2 * sigma^2))
    
    Parameters
    ----------
    x : array_like or scalar
        Input array (Doppler or wavelength values).
        Will be converted to numpy.ndarray of type float32.
    i0 : float
        Peak intensity. Must be scalar.
    mu : float
        Center position (Doppler shift). Must be scalar.
    sigma : float
        Width parameter. Must be scalar and positive.
    
    Returns
    -------
    numpy.ndarray or float
        Gaussian profile with same shape as x, dtype=float32.
        If x is scalar, returns scalar float.
    
    Notes
    -----
    Uses Apple Accelerate framework for vectorized computation.
    Converts inputs to float32 for optimal performance.
    All parameters except x must be scalars.
    
    Performance: ~5x faster than NumPy with float64.
    Accuracy: <1e-7 difference vs float64 for typical values.
    
    Examples
    --------
    >>> import numpy as np
    >>> from ftools.fgaussian import gaussian
    >>> x = np.linspace(-5, 5, 100)
    >>> profile = gaussian(x, i0=1.0, mu=0.0, sigma=1.0)
    >>> # Scalar input
    >>> value = gaussian(0.0, i0=1.0, mu=0.0, sigma=1.0)
    """
    # Check if input x is scalar
    x_is_scalar = np.isscalar(x)
    
    # Convert x to numpy array of type float32
    x_array = np.asarray(x, dtype=np.float32)
    
    # Check if parameters are scalars
    i0_is_scalar = np.isscalar(i0)
    mu_is_scalar = np.isscalar(mu)
    sigma_is_scalar = np.isscalar(sigma)
    
    # All parameters except x must be scalars
    if not (i0_is_scalar and mu_is_scalar and sigma_is_scalar):
        raise ValueError("i0, mu, and sigma must be scalars")
    
    # Convert to Python float to ensure proper type
    i0_float = float(i0)
    mu_float = float(mu)
    sigma_float = float(sigma)
    
    # Call C extension
    result = fgaussian_ext.gaussian(x_array, i0_float, mu_float, sigma_float)
    
    # If input was scalar, return scalar
    if x_is_scalar:
        return float(result)
    
    return result


__all__ = ['gaussian']
