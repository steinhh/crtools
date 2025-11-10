/*
 * Benchmark: sort125 (hybrid) vs qsort
 *
 * This program compares the performance of the hybrid sort125 implementation
 * against the standard library qsort for 125-element arrays.
 *
 * Methodology:
 * 1. Generate many random permutations of 125 elements
 * 2. Time how long it takes to sort all of them with sort125
 * 3. Time how long it takes to sort all of them with qsort
 * 4. Report timing results and speedup factor
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Include the sorting networks */
#include "sorting_networks_generated.c"

/* Hybrid sort125: Uses sort25 blocks + insertion sort for 125 elements */
static inline void sort125(double *d)
{
  /* Hybrid approach: sort 5 blocks of 25 elements, then insertion sort
   * 125 = 5 * 25, so we can use sort25b for pre-sorting
   * This creates a partially sorted structure that makes insertion sort efficient
   */

  /* Sort 5 blocks of 25 elements each using sort25b */
  sort25b(&d[0]);   /* Elements 0-24 */
  sort25b(&d[25]);  /* Elements 25-49 */
  sort25b(&d[50]);  /* Elements 50-74 */
  sort25b(&d[75]);  /* Elements 75-99 */
  sort25b(&d[100]); /* Elements 100-124 */

  /* Complete the sort using insertion sort on the partially-sorted array
   * The pre-sorted blocks reduce the number of comparisons needed
   */
  for (int i = 1; i < 125; i++)
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
  double test_array[125];

  start = clock();
  for (int i = 0; i < num_iterations; i++)
  {
    /* Generate random permutation */
    generate_random_permutation(test_array, 125);
    
    /* Sort it */
    sort_func(test_array);
  }
  end = clock();

  return ((double)(end - start)) / CLOCKS_PER_SEC;
}

/* Wrapper for qsort to match function signature */
static void qsort_wrapper(double *arr)
{
  qsort(arr, 125, sizeof(double), compare_double);
}

int main(void)
{
  /* Seed random number generator */
  srand(time(NULL));

  const int num_iterations = 1000000; /* 1 million sorts */
  double workspace[125];
  
  printf("========================================\n");
  printf("Benchmark: sort125 vs qsort\n");
  printf("========================================\n");
  printf("Array size: 125 elements\n");
  printf("Iterations: %d\n\n", num_iterations);

  /* Warm up caches */
  printf("Warming up...\n");
  for (int i = 0; i < 10000; i++)
  {
    generate_random_permutation(workspace, 125);
    sort125(workspace);
  }

  /* Benchmark sort125 */
  printf("Benchmarking sort125 (hybrid)...\n");
  double time_sort125 = benchmark_sort(sort125, num_iterations, workspace);
  printf("  Time: %.3f seconds\n", time_sort125);
  printf("  Rate: %.0f sorts/second\n\n", num_iterations / time_sort125);

  /* Benchmark qsort */
  printf("Benchmarking qsort (stdlib)...\n");
  double time_qsort = benchmark_sort(qsort_wrapper, num_iterations, workspace);
  printf("  Time: %.3f seconds\n", time_qsort);
  printf("  Rate: %.0f sorts/second\n\n", num_iterations / time_qsort);

  /* Calculate speedup */
  double speedup = time_qsort / time_sort125;
  printf("========================================\n");
  printf("Results:\n");
  printf("========================================\n");
  printf("sort125 is %.2fx faster than qsort\n", speedup);
  
  if (speedup > 1.5)
  {
    printf("? Hybrid sort125 shows significant improvement!\n");
  }
  else if (speedup > 1.0)
  {
    printf("? Hybrid sort125 is faster\n");
  }
  else
  {
    printf("? qsort is faster (consider using qsort for this size)\n");
  }
  
  printf("========================================\n");

  return 0;
}
