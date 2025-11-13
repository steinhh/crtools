def gaussian(x, i0, mu, sigma):
  """
Gaussian definition.

Parameters

----------

x : `xarray.Dataset` or `numpy.ndarray` Doppler or wavelength values.

i0 : `xarray.Dataset` or `numpy.ndarray` or `float` : Peak intensity.

mu : `xarray.Dataset` or `numpy.ndarray` or `float` : Doppler shift in same units as ``x``.

sigma : `xarray.Dataset` or `numpy.ndarray` or `float` : Width in same units as ``x``.

Returns

-------

`xarray.Dataset` or `numpy.ndarray`

Gaussian profile over ``x``.

"""
return i0 * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))  # NOSONAR python:S2711
