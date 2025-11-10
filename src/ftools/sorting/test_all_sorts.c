/*
 * Comprehensive test suite for all sorting network routines
 *
 * This program tests all sort[N] functions (N=3 to 27) against qsort
 * to identify any incorrect sorting networks.
 *
 * Test methodology:
 * 1. Generate random permutations of N elements
 * 2. Sort one copy with sort[N], another with qsort
 * 3. Compare results element-by-element
 * 4. Report any discrepancies
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

/* Include the sorting networks */
#include "sorting_networks_generated.c"

/* Comparison function for qsort (double) */
static int compare_double(const void *a, const void *b)
{
  double da = *(const double *)a;
  double db = *(const double *)b;
  if (da < db)
    return -1;
  if (da > db)
    return 1;
  return 0;
}

/* Check if two arrays are equal */
static int arrays_equal(const double *a, const double *b, int n)
{
  for (int i = 0; i < n; i++)
  {
    if (fabs(a[i] - b[i]) > 1e-10)
    {
      return 0;
    }
  }
  return 1;
}

/* Print array for debugging */
static void print_array(const double *arr, int n, const char *label)
{
  printf("%s: [", label);
  for (int i = 0; i < n; i++)
  {
    printf("%.2f", arr[i]);
    if (i < n - 1)
      printf(", ");
  }
  printf("]\n");
}

/* Generate a random permutation of values 0 to n-1 */
static void generate_random_permutation(double *arr, int n)
{
  /* Initialize with values 0, 1, 2, ..., n-1 */
  for (int i = 0; i < n; i++)
  {
    arr[i] = (double)i;
  }

  /* Fisher-Yates shuffle */
  for (int i = n - 1; i > 0; i--)
  {
    int j = rand() % (i + 1);
    double temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
  }
}

/* Test a sorting function against qsort */
typedef void (*sort_func_t)(double *);

#define MAX_SIZE 150

static int test_sort_function(sort_func_t sort_func, int size, const char *name, int num_tests)
{
  int failures = 0;
  static double test_array[MAX_SIZE];
  static double qsort_array[MAX_SIZE];
  static double original_array[MAX_SIZE];

  printf("Testing %s (%d elements) with %d random permutations...\n", name, size, num_tests);

  for (int test = 0; test < num_tests; test++)
  {
    /* Generate random permutation */
    generate_random_permutation(test_array, size);

    /* Make copies for qsort and for display */
    memcpy(qsort_array, test_array, size * sizeof(double));
    memcpy(original_array, test_array, size * sizeof(double));

    /* Sort with both methods */
    sort_func(test_array);
    qsort(qsort_array, size, sizeof(double), compare_double);

    /* Compare results */
    if (!arrays_equal(test_array, qsort_array, size))
    {
      failures++;
      if (failures <= 3) /* Only show first 3 failures per function */
      {
        printf("  ? FAILURE #%d (test %d):\n", failures, test + 1);
        printf("     ");
        print_array(original_array, size, "Original");
        printf("     ");
        print_array(test_array, size, "sort result");
        printf("     ");
        print_array(qsort_array, size, "qsort result");
      }
      /* Stop after finding first failure to avoid crashes */
      if (failures >= 1)
        break;
    }
  }

  if (failures == 0)
  {
    printf("  ? PASSED: All %d tests passed\n\n", num_tests);
  }
  else
  {
    printf("  ? FAILED: %d/%d tests failed (%.1f%% failure rate)\n\n",
           failures, num_tests, 100.0 * failures / num_tests);
  }

  return failures;
}

int main(void)
{
  /* Seed random number generator */
  srand(time(NULL));

  int total_failures = 0;
  const int num_tests = 10000; /* Number of random permutations to test per function */

  printf("========================================\n");
  printf("Testing All Sorting Networks vs qsort\n");
  printf("========================================\n\n");

  /* Test all sorting functions */
  total_failures += test_sort_function(sort3, 3, "sort3", num_tests);
  total_failures += test_sort_function(sort4, 4, "sort4", num_tests);
  total_failures += test_sort_function(sort5, 5, "sort5", num_tests);
  total_failures += test_sort_function(sort6, 6, "sort6", num_tests);
  total_failures += test_sort_function(sort7, 7, "sort7", num_tests);
  total_failures += test_sort_function(sort8, 8, "sort8", num_tests);
  total_failures += test_sort_function(sort9, 9, "sort9", num_tests);
  total_failures += test_sort_function(sort11, 11, "sort11", num_tests);
  total_failures += test_sort_function(sort12, 12, "sort12", num_tests);
  total_failures += test_sort_function(sort13, 13, "sort13", num_tests);
  total_failures += test_sort_function(sort14, 14, "sort14", num_tests);
  total_failures += test_sort_function(sort15, 15, "sort15", num_tests);
  total_failures += test_sort_function(sort16, 16, "sort16", num_tests);
  total_failures += test_sort_function(sort17, 17, "sort17", num_tests);
  total_failures += test_sort_function(sort18, 18, "sort18", num_tests);
  total_failures += test_sort_function(sort19, 19, "sort19", num_tests);
  total_failures += test_sort_function(sort20, 20, "sort20", num_tests);
  total_failures += test_sort_function(sort21, 21, "sort21", num_tests);
  total_failures += test_sort_function(sort22, 22, "sort22", num_tests);
  total_failures += test_sort_function(sort23, 23, "sort23", num_tests);
  total_failures += test_sort_function(sort24, 24, "sort24", num_tests);
  total_failures += test_sort_function(sort25, 25, "sort25 (hybrid)", num_tests);
  total_failures += test_sort_function(sort25b, 25, "sort25b (complete network)", num_tests);
  total_failures += test_sort_function(sort26, 26, "sort26", num_tests);
  total_failures += test_sort_function(sort27, 27, "sort27 (hybrid)", num_tests);
  total_failures += test_sort_function(sort27b, 27, "sort27b (complete network)", num_tests);
  total_failures += test_sort_function(sort124, 124, "sort124 (hybrid)", num_tests);
  total_failures += test_sort_function(sort125, 125, "sort125 (hybrid)", num_tests);

  printf("========================================\n");
  if (total_failures == 0)
  {
    printf("? ALL TESTS PASSED\n");
    printf("All sorting networks produce results identical to qsort\n");
  }
  else
  {
    printf("? TESTS FAILED\n");
    printf("Total failures detected: %d\n", total_failures);
    printf("Some sorting networks produce different results than qsort\n");
  }
  printf("========================================\n");

  return total_failures > 0 ? 1 : 0;
}
