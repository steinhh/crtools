/*
 * Benchmark: sort124 (hybrid) vs qsort
 *
 * This program compares the performance of the hybrid sort124 implementation
 * against the standard library qsort for 124-element arrays.
 *
 * Methodology:
 * 1. Generate many random permutations of 124 elements
 * 2. Time how long it takes to sort all of them with sort124
 * 3. Time how long it takes to sort all of them with qsort
 * 4. Report timing results and speedup factor
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Include the sorting networks */
#include "sorting_networks_generated.c"

/* Hybrid sort124: Uses sort24 blocks + insertion sort for 124 elements */
static inline void sort124(double *d)
{
  /* Hybrid approach: sort 5 blocks of 24 elements + 4 remaining, then insertion sort
   * 124 = 5 * 24 + 4
   * Pre-sorting the larger blocks creates a partially sorted structure
   */

  /* Sort 5 blocks of 24 elements each using sort24 */
  sort24(&d[0]);  /* Elements 0-23 */
  sort24(&d[24]); /* Elements 24-47 */
  sort24(&d[48]); /* Elements 48-71 */
  sort24(&d[72]); /* Elements 72-95 */
  sort24(&d[96]); /* Elements 96-119 */
  /* Elements 120-123 (4 elements) left unsorted initially */

  /* Complete the sort using insertion sort on the partially-sorted array */
  for (int i = 1; i < 124; i++)
  {
    double key = d[i];
    int j = i - 1;
    while (j >= 0 && d[j] > key)
    {
      d[j + 1] = d[j];
      j--;
    }
    d[j + 1] = key;
  }
}

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

/* Benchmark a sorting function */
static double benchmark_sort(void (*sort_func)(double *), int num_iterations, double *workspace)
{
  clock_t start, end;
  double test_array[124];

  start = clock();
  for (int i = 0; i < num_iterations; i++)
  {
    /* Generate random permutation */
    generate_random_permutation(test_array, 124);

    /* Sort it */
    sort_func(test_array);
  }
  end = clock();

  return ((double)(end - start)) / CLOCKS_PER_SEC;
}

/* Wrapper for qsort to match function signature */
static void qsort_wrapper(double *arr)
{
  qsort(arr, 124, sizeof(double), compare_double);
}

int main(void)
{
  /* Seed random number generator */
  srand(time(NULL));

  const int num_iterations = 1000000; /* 1 million sorts */
  double workspace[124];

  printf("========================================\n");
  printf("Benchmark: sort124 vs qsort\n");
  printf("========================================\n");
  printf("Array size: 124 elements\n");
  printf("Iterations: %d\n\n", num_iterations);

  /* Warm up caches */
  printf("Warming up...\n");
  for (int i = 0; i < 10000; i++)
  {
    generate_random_permutation(workspace, 124);
    sort124(workspace);
  }

  /* Benchmark sort124 */
  printf("Benchmarking sort124 (hybrid)...\n");
  double time_sort124 = benchmark_sort(sort124, num_iterations, workspace);
  printf("  Time: %.3f seconds\n", time_sort124);
  printf("  Rate: %.0f sorts/second\n\n", num_iterations / time_sort124);

  /* Benchmark qsort */
  printf("Benchmarking qsort (stdlib)...\n");
  double time_qsort = benchmark_sort(qsort_wrapper, num_iterations, workspace);
  printf("  Time: %.3f seconds\n", time_qsort);
  printf("  Rate: %.0f sorts/second\n\n", num_iterations / time_qsort);

  /* Calculate speedup */
  double speedup = time_qsort / time_sort124;
  printf("========================================\n");
  printf("Results:\n");
  printf("========================================\n");
  printf("sort124 is %.2fx faster than qsort\n", speedup);

  if (speedup > 1.5)
  {
    printf("? Hybrid sort124 shows significant improvement!\n");
  }
  else if (speedup > 1.0)
  {
    printf("? Hybrid sort124 shows modest improvement.\n");
  }
  else
  {
    printf("? qsort is faster. Hybrid approach not beneficial for N=124.\n");
  }
  printf("========================================\n");

  return 0;
}
