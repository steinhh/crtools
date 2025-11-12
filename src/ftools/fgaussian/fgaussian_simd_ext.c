/*
 * SIMD-optimized C extension for computing Gaussian profiles
 *
 * Implements: result = i0 * exp(-((x - mu)^2) / (2 * sigma^2))
 *
 * Uses ARM NEON intrinsics for vectorized computation on Apple Silicon.
 * Falls back to scalar code on other architectures.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include <math.h>

/* Detect ARM NEON support (Apple Silicon, ARM64) */
#if defined(__aarch64__) || defined(__arm64__) || defined(_M_ARM64)
#define USE_NEON 1
#include <arm_neon.h>
#endif

/* Detect x86 AVX support */
#if defined(__AVX__) && defined(__x86_64__)
#define USE_AVX 1
#include <immintrin.h>
#endif

#ifdef USE_NEON
/*
 * NEON vectorized Gaussian computation (processes 2 doubles at a time)
 * Uses scalar exp() for accuracy - SIMD exp approximations are complex
 */
static void compute_gaussian_neon(const double *x, double i0, double mu, double sigma,
                                  double *result, npy_intp n)
{
  const double two_sigma_sq = 2.0 * sigma * sigma;
  const float64x2_t v_mu = vdupq_n_f64(mu);
  const float64x2_t v_two_sigma_sq = vdupq_n_f64(two_sigma_sq);
  const float64x2_t v_i0 = vdupq_n_f64(i0);
  const float64x2_t v_neg_one = vdupq_n_f64(-1.0);

  npy_intp i = 0;

  /* Process 2 elements at a time with NEON */
  for (; i + 1 < n; i += 2)
  {
    /* Load 2 doubles */
    float64x2_t v_x = vld1q_f64(&x[i]);

    /* diff = x - mu */
    float64x2_t v_diff = vsubq_f64(v_x, v_mu);

    /* diff_sq = diff * diff */
    float64x2_t v_diff_sq = vmulq_f64(v_diff, v_diff);

    /* exponent = -(diff_sq / two_sigma_sq) */
    float64x2_t v_exponent = vdivq_f64(v_diff_sq, v_two_sigma_sq);
    v_exponent = vmulq_f64(v_exponent, v_neg_one);

    /* Use scalar exp for accuracy - extract, compute, reload */
    double exponents[2];
    vst1q_f64(exponents, v_exponent);
    exponents[0] = exp(exponents[0]);
    exponents[1] = exp(exponents[1]);
    float64x2_t v_exp_val = vld1q_f64(exponents);

    /* result = i0 * exp_val */
    float64x2_t v_result = vmulq_f64(v_i0, v_exp_val);

    /* Store results */
    vst1q_f64(&result[i], v_result);
  }

  /* Handle remaining elements with scalar code */
  for (; i < n; i++)
  {
    double diff = x[i] - mu;
    result[i] = i0 * exp(-(diff * diff) / two_sigma_sq);
  }
}
#endif /* USE_NEON */

#ifdef USE_AVX
/*
 * AVX vectorized Gaussian computation (processes 4 doubles at a time)
 */
static void compute_gaussian_avx(const double *x, double i0, double mu, double sigma,
                                 double *result, npy_intp n)
{
  const double two_sigma_sq = 2.0 * sigma * sigma;
  const __m256d v_mu = _mm256_set1_pd(mu);
  const __m256d v_two_sigma_sq = _mm256_set1_pd(two_sigma_sq);
  const __m256d v_i0 = _mm256_set1_pd(i0);

  npy_intp i = 0;

  /* Process 4 elements at a time with AVX */
  for (; i + 3 < n; i += 4)
  {
    /* Load 4 doubles */
    __m256d v_x = _mm256_loadu_pd(&x[i]);

    /* diff = x - mu */
    __m256d v_diff = _mm256_sub_pd(v_x, v_mu);

    /* diff_sq = diff * diff */
    __m256d v_diff_sq = _mm256_mul_pd(v_diff, v_diff);

    /* exponent = -diff_sq / two_sigma_sq */
    __m256d v_exponent = _mm256_div_pd(v_diff_sq, v_two_sigma_sq);
    v_exponent = _mm256_sub_pd(_mm256_setzero_pd(), v_exponent);

    /* exp_val = exp(exponent) - use scalar exp for now */
    /* Note: Intel SVML provides vectorized exp, but it's not portable */
    double exp_vals[4];
    _mm256_storeu_pd(exp_vals, v_exponent);
    for (int j = 0; j < 4; j++)
    {
      exp_vals[j] = exp(exp_vals[j]);
    }
    __m256d v_exp_val = _mm256_loadu_pd(exp_vals);

    /* result = i0 * exp_val */
    __m256d v_result = _mm256_mul_pd(v_i0, v_exp_val);

    /* Store results */
    _mm256_storeu_pd(&result[i], v_result);
  }

  /* Handle remaining elements with scalar code */
  for (; i < n; i++)
  {
    double diff = x[i] - mu;
    result[i] = i0 * exp(-(diff * diff) / two_sigma_sq);
  }
}
#endif /* USE_AVX */

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
#ifdef USE_NEON
  compute_gaussian_neon(x, i0, mu, sigma, result, n);
#elif defined(USE_AVX)
  compute_gaussian_avx(x, i0, mu, sigma, result, n);
#else
  compute_gaussian_scalar(x, i0, mu, sigma, result, n);
#endif
}

/*
 * Python interface: gaussian(x, i0, mu, sigma)
 */
static PyObject *fgaussian_simd_gaussian(PyObject *self, PyObject *args)
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
static PyMethodDef FGaussianSIMDMethods[] = {
    {"gaussian", fgaussian_simd_gaussian, METH_VARARGS,
     "SIMD-optimized Gaussian profile computation\n\n"
     "Uses ARM NEON or x86 AVX when available, falls back to scalar code."},
    {NULL, NULL, 0, NULL}};

/* Module definition */
static struct PyModuleDef fgaussian_simd_module = {
    PyModuleDef_HEAD_INIT,
    "fgaussian_simd_ext",
    "SIMD-optimized C extension for computing Gaussian profiles",
    -1,
    FGaussianSIMDMethods};

/* Module initialization */
PyMODINIT_FUNC PyInit_fgaussian_simd_ext(void)
{
  import_array();

  if (PyErr_Occurred())
  {
    return NULL;
  }

  return PyModule_Create(&fgaussian_simd_module);
}
