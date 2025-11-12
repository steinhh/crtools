/*
 * C extension for computing Gaussian profiles
 * 
 * Implements: result = i0 * exp(-((x - mu)^2) / (2 * sigma^2))
 * 
 * This provides high-performance computation of Gaussian profiles over arrays.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include <math.h>

/*
 * Compute Gaussian profile over array
 * 
 * result[i] = i0 * exp(-((x[i] - mu)^2) / (2 * sigma^2))
 * 
 * Parameters:
 *   x      - Input array (double)
 *   i0     - Peak intensity (scalar)
 *   mu     - Center position (scalar)
 *   sigma  - Width parameter (scalar)
 *   result - Output array (double, same shape as x)
 *   n      - Array length
 */
static void compute_gaussian(const double *x, double i0, double mu, double sigma,
                             double *result, npy_intp n)
{
  const double two_sigma_sq = 2.0 * sigma * sigma;
  
  for (npy_intp i = 0; i < n; i++)
  {
    double diff = x[i] - mu;
    result[i] = i0 * exp(-(diff * diff) / two_sigma_sq);
  }
}

/*
 * Python interface: gaussian(x, i0, mu, sigma)
 * 
 * All inputs must be numpy arrays of type double (or scalars coerced to double)
 * Returns numpy array of type double
 */
static PyObject *fgaussian_gaussian(PyObject *self, PyObject *args)
{
  PyArrayObject *x_array = NULL;
  double i0, mu, sigma;
  
  /* Parse arguments: x (array), i0, mu, sigma (scalars) */
  if (!PyArg_ParseTuple(args, "O!ddd",
                        &PyArray_Type, &x_array,
                        &i0, &mu, &sigma))
  {
    return NULL;
  }
  
  /* Validate x is a numpy array */
  if (!PyArray_Check(x_array))
  {
    PyErr_SetString(PyExc_TypeError, "x must be a numpy array");
    return NULL;
  }
  
  /* Ensure x is double type and contiguous */
  PyArrayObject *x_contig = (PyArrayObject *)PyArray_FROM_OTF(
      (PyObject *)x_array, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  if (x_contig == NULL)
  {
    return NULL;
  }
  
  /* Get array dimensions */
  int ndim = PyArray_NDIM(x_contig);
  npy_intp *dims = PyArray_DIMS(x_contig);
  npy_intp total_size = PyArray_SIZE(x_contig);
  
  /* Create output array with same shape as input */
  PyArrayObject *result = (PyArrayObject *)PyArray_SimpleNew(ndim, dims, NPY_DOUBLE);
  if (result == NULL)
  {
    Py_DECREF(x_contig);
    return NULL;
  }
  
  /* Get pointers to data */
  const double *x_data = (const double *)PyArray_DATA(x_contig);
  double *result_data = (double *)PyArray_DATA(result);
  
  /* Validate sigma is positive */
  if (sigma <= 0.0)
  {
    Py_DECREF(x_contig);
    Py_DECREF(result);
    PyErr_SetString(PyExc_ValueError, "sigma must be positive");
    return NULL;
  }
  
  /* Compute Gaussian profile */
  compute_gaussian(x_data, i0, mu, sigma, result_data, total_size);
  
  Py_DECREF(x_contig);
  
  return (PyObject *)result;
}

/* Method definition */
static PyMethodDef FGaussianMethods[] = {
    {"gaussian", fgaussian_gaussian, METH_VARARGS,
     "Compute Gaussian profile: i0 * exp(-((x - mu)^2) / (2 * sigma^2))\n\n"
     "Parameters\n"
     "----------\n"
     "x : numpy.ndarray\n"
     "    Input array (double)\n"
     "i0 : float\n"
     "    Peak intensity\n"
     "mu : float\n"
     "    Center position\n"
     "sigma : float\n"
     "    Width parameter (must be positive)\n\n"
     "Returns\n"
     "-------\n"
     "numpy.ndarray\n"
     "    Gaussian profile with same shape as x"},
    {NULL, NULL, 0, NULL}
};

/* Module definition */
static struct PyModuleDef fgaussian_module = {
    PyModuleDef_HEAD_INIT,
    "fgaussian_ext",
    "C extension for computing Gaussian profiles",
    -1,
    FGaussianMethods
};

/* Module initialization */
PyMODINIT_FUNC PyInit_fgaussian_ext(void)
{
  import_array(); /* Initialize NumPy C API */
  
  if (PyErr_Occurred())
  {
    return NULL;
  }
  
  return PyModule_Create(&fgaussian_module);
}
