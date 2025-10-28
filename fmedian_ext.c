#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <numpy/arrayobject.h>
#include <stdlib.h>
#include <math.h>

/* Comparison function for qsort */
static int compare_int16(const void *a, const void *b) {
    return (*(int16_t*)a - *(int16_t*)b);
}

/* Function to compute median from a sorted array */
static double compute_median(int16_t *values, int count) {
    if (count == 0) {
        return 0.0;
    }
    
    qsort(values, count, sizeof(int16_t), compare_int16);
    
    if (count % 2 == 0) {
        return (values[count/2 - 1] + values[count/2]) / 2.0;
    } else {
        return (double)values[count/2];
    }
}

/* Main fmedian function */
static PyObject* fmedian(PyObject* self, PyObject* args) {
    PyArrayObject *input_array, *output_array;
    int16_t xsize, ysize;
    double threshold;
    
    /* Parse arguments */
    if (!PyArg_ParseTuple(args, "O!O!hhd", 
                          &PyArray_Type, &input_array,
                          &PyArray_Type, &output_array,
                          &xsize, &ysize, &threshold)) {
        return NULL;
    }
    
    /* Check array dimensions */
    if (PyArray_NDIM(input_array) != 2 || PyArray_NDIM(output_array) != 2) {
        PyErr_SetString(PyExc_ValueError, "Arrays must be 2-dimensional");
        return NULL;
    }
    
    /* Get array dimensions */
    npy_intp *input_dims = PyArray_DIMS(input_array);
    npy_intp *output_dims = PyArray_DIMS(output_array);
    
    /* Check that arrays have same size */
    if (input_dims[0] != output_dims[0] || input_dims[1] != output_dims[1]) {
        PyErr_SetString(PyExc_ValueError, "Input and output arrays must have identical size");
        return NULL;
    }
    
    int height = (int)input_dims[0];
    int width = (int)input_dims[1];
    
    /* Check data types */
    if (PyArray_TYPE(input_array) != NPY_INT16) {
        PyErr_SetString(PyExc_TypeError, "input_array must be of type int16");
        return NULL;
    }
    
    if (PyArray_TYPE(output_array) != NPY_FLOAT64) {
        PyErr_SetString(PyExc_TypeError, "output_array must be of type float64");
        return NULL;
    }
    
    /* Get data pointers */
    int16_t *input_data = (int16_t*)PyArray_DATA(input_array);
    double *output_data = (double*)PyArray_DATA(output_array);
    
    /* Get strides */
    npy_intp *input_strides = PyArray_STRIDES(input_array);
    npy_intp *output_strides = PyArray_STRIDES(output_array);
    
    /* Allocate buffer for neighborhood values */
    int max_neighbors = (2 * xsize + 1) * (2 * ysize + 1);
    int16_t *neighbors = (int16_t*)malloc(max_neighbors * sizeof(int16_t));
    if (neighbors == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory for neighbors");
        return NULL;
    }
    
    /* Process each pixel */
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int count = 0;
            
            /* Get current pixel value */
            int16_t center_value = *(int16_t*)(((char*)input_data) + y * input_strides[0] + x * input_strides[1]);
            
            /* Collect neighborhood values */
            for (int dy = -ysize; dy <= ysize; dy++) {
                for (int dx = -xsize; dx <= xsize; dx++) {
                    int ny = y + dy;
                    int nx = x + dx;
                    
                    /* Check bounds */
                    if (ny >= 0 && ny < height && nx >= 0 && nx < width) {
                        int16_t neighbor_value = *(int16_t*)(((char*)input_data) + ny * input_strides[0] + nx * input_strides[1]);
                        
                        /* Only include values that differ from center by less than threshold */
                        if (fabs((double)(neighbor_value - center_value)) < threshold) {
                            neighbors[count++] = neighbor_value;
                        }
                    }
                }
            }
            
            /* Compute median and store in output */
            double median_value = compute_median(neighbors, count);
            *(double*)(((char*)output_data) + y * output_strides[0] + x * output_strides[1]) = median_value;
        }
    }
    
    free(neighbors);
    
    Py_RETURN_NONE;
}

/* Method definitions */
static PyMethodDef FmedianMethods[] = {
    {"fmedian", fmedian, METH_VARARGS, 
     "Compute filtered median of 2D array.\n\n"
     "Parameters:\n"
     "    input_array : numpy.ndarray (int16, 2D)\n"
     "        Input array\n"
     "    output_array : numpy.ndarray (float64, 2D)\n"
     "        Output array (same size as input)\n"
     "    xsize : int16\n"
     "        Half-width of window in x direction\n"
     "    ysize : int16\n"
     "        Half-width of window in y direction\n"
     "    threshold : float64\n"
     "        Threshold for including values in median calculation\n"},
    {NULL, NULL, 0, NULL}
};

/* Module definition */
static struct PyModuleDef fmedian_module = {
    PyModuleDef_HEAD_INIT,
    "fmedian_ext",
    "Python extension for filtered median computation",
    -1,
    FmedianMethods
};

/* Module initialization */
PyMODINIT_FUNC PyInit_fmedian_ext(void) {
    import_array();
    return PyModule_Create(&fmedian_module);
}
