/*
 * Accelerate-optimized C extension for computing Gaussian profiles
 *
 * Uses Apple's Accelerate framework (vForce) for vectorized exp()
 * Available on macOS/iOS - provides dramatic speedup over scalar exp()
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include <math.h>

/* Use Accelerate framework on macOS/iOS */
#if defined(__APPLE__)
#define USE_ACCELERATE 1
#include <Accelerate/Accelerate.h>
#endif

#ifdef USE_ACCELERATE
/*
 * Accelerate-optimized Gaussian computation (zero-copy version)
 * Uses vForce vvexp for vectorized exponential
 * Works directly in the output array to avoid temporary allocation
 */
static void compute_gaussian_accelerate(const double *x, double i0, double mu, double sigma,
                                        double *result, npy_intp n)
{
  const double two_sigma_sq = 2.0 * sigma * sigma;
  const double inv_two_sigma_sq = 1.0 / two_sigma_sq;
  const double scale = -inv_two_sigma_sq;
  const double neg_mu = -mu;

  /* Step 1: result = x - mu (vectorized subtraction) */
  vDSP_vsaddD(x, 1, &neg_mu, result, 1, n);

  /* Step 2: result = result * result (vectorized squaring - in place) */
  vDSP_vsqD(result, 1, result, 1, n);

  /* Step 3: result = result * (-1 / two_sigma_sq) (vectorized scale - in place) */
  vDSP_vsmulD(result, 1, &scale, result, 1, n);

  /* Step 4: result = exp(result) (vectorized exponential - in place) */
  int n_int = (int)n;
  vvexp(result, result, &n_int);

  /* Step 5: result = i0 * result (vectorized scale - in place) */
  vDSP_vsmulD(result, 1, &i0, result, 1, n);
}
#endif /* USE_ACCELERATE */

/*
 * Scalar fallback implementation
 */
static void compute_gaussian_scalar(const double *x, double i0, double mu, double sigma,
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
 * Main computation function - dispatches to appropriate implementation
 */
static void compute_gaussian(const double *x, double i0, double mu, double sigma,
                             double *result, npy_intp n)
{
#ifdef USE_ACCELERATE
  compute_gaussian_accelerate(x, i0, mu, sigma, result, n);
#else
  compute_gaussian_scalar(x, i0, mu, sigma, result, n);
#endif
}

/*
 * Python interface: gaussian(x, i0, mu, sigma)
 */
static PyObject *fgaussian_accelerate_gaussian(PyObject *self, PyObject *args)
{
  PyArrayObject *x_array = NULL;
  double i0, mu, sigma;

  /* Parse arguments */
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

  /* Create output array */
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
static PyMethodDef FGaussianAccelerateMethods[] = {
    {"gaussian", fgaussian_accelerate_gaussian, METH_VARARGS,
     "Accelerate-optimized Gaussian profile computation\n\n"
     "Uses Apple's vForce library for vectorized exp() on macOS."},
    {NULL, NULL, 0, NULL}};

/* Module definition */
static struct PyModuleDef fgaussian_accelerate_module = {
    PyModuleDef_HEAD_INIT,
    "fgaussian_accelerate_ext",
    "Accelerate-optimized C extension for computing Gaussian profiles",
    -1,
    FGaussianAccelerateMethods};

/* Module initialization */
PyMODINIT_FUNC PyInit_fgaussian_accelerate_ext(void)
{
  import_array();

  if (PyErr_Occurred())
  {
    return NULL;
  }

  return PyModule_Create(&fgaussian_accelerate_module);
}
