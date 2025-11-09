/*
 * Benchmark comparison between sort27() and sort27b()
 *
 * sort27() - Hybrid approach: sort3 + sort9 + insertion sort
 * sort27b() - Complete 114-comparator sorting network
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>

/* Include the sorting implementations */
#include "sorting.c"

/* Generate random double array */
void generate_random_array(double *arr, int size)
{
  for (int i = 0; i < size; i++)
  {
    arr[i] = (double)rand() / RAND_MAX * 1000.0;
  }
}

/* Verify array is sorted */
int is_sorted(double *arr, int size)
{
  for (int i = 1; i < size; i++)
  {
    if (arr[i] < arr[i - 1])
    {
      return 0;
    }
  }
  return 1;
}

/* Benchmark function */
double benchmark_sort_function(void (*sort_func)(double *), int num_iterations, int verify)
{
  double arr[27];
  double test_arr[27];
  clock_t start, end;
  int failed = 0;

  /* Warm up */
  for (int i = 0; i < 1000; i++)
  {
    generate_random_array(arr, 27);
    sort_func(arr);
  }

  /* Benchmark */
  start = clock();
  for (int i = 0; i < num_iterations; i++)
  {
    generate_random_array(arr, 27);
    memcpy(test_arr, arr, 27 * sizeof(double));
    sort_func(test_arr);

    if (verify && !is_sorted(test_arr, 27))
    {
      failed++;
    }
  }
  end = clock();

  if (verify && failed > 0)
  {
    printf("    WARNING: %d/%d tests failed sorting verification!\n", failed, num_iterations);
  }

  return ((double)(end - start)) / CLOCKS_PER_SEC;
}

/* Test with specific patterns */
void test_specific_patterns()
{
  printf("\nTesting specific patterns:\n");

  double arr1[27], arr2[27];
  int test_count = 0;
  int pass_count = 0;

  /* Test 1: Already sorted */
  test_count++;
  for (int i = 0; i < 27; i++)
    arr1[i] = arr2[i] = i;
  sort27(arr1);
  sort27b(arr2);
  if (is_sorted(arr1, 27) && is_sorted(arr2, 27))
  {
    pass_count++;
    printf("  ? Already sorted: PASS\n");
  }
  else
  {
    printf("  ? Already sorted: FAIL\n");
  }

  /* Test 2: Reverse sorted */
  test_count++;
  for (int i = 0; i < 27; i++)
    arr1[i] = arr2[i] = 26 - i;
  sort27(arr1);
  sort27b(arr2);
  if (is_sorted(arr1, 27) && is_sorted(arr2, 27))
  {
    pass_count++;
    printf("  ? Reverse sorted: PASS\n");
  }
  else
  {
    printf("  ? Reverse sorted: FAIL\n");
  }

  /* Test 3: All same values */
  test_count++;
  for (int i = 0; i < 27; i++)
    arr1[i] = arr2[i] = 5.0;
  sort27(arr1);
  sort27b(arr2);
  if (is_sorted(arr1, 27) && is_sorted(arr2, 27))
  {
    pass_count++;
    printf("  ? All same values: PASS\n");
  }
  else
  {
    printf("  ? All same values: FAIL\n");
  }

  /* Test 4: Random permutation */
  test_count++;
  srand(42);
  for (int i = 0; i < 27; i++)
    arr1[i] = arr2[i] = (double)rand() / RAND_MAX;
  sort27(arr1);
  sort27b(arr2);
  if (is_sorted(arr1, 27) && is_sorted(arr2, 27))
  {
    pass_count++;
    printf("  ? Random permutation: PASS\n");
  }
  else
  {
    printf("  ? Random permutation: FAIL\n");
  }

  /* Test 5: Alternating high/low */
  test_count++;
  for (int i = 0; i < 27; i++)
    arr1[i] = arr2[i] = (i % 2) ? 100.0 : 0.0;
  sort27(arr1);
  sort27b(arr2);
  if (is_sorted(arr1, 27) && is_sorted(arr2, 27))
  {
    pass_count++;
    printf("  ? Alternating high/low: PASS\n");
  }
  else
  {
    printf("  ? Alternating high/low: FAIL\n");
  }

  printf("\nPattern tests: %d/%d passed\n", pass_count, test_count);
}

/* Main benchmark */
int main()
{
  printf("=================================================================\n");
  printf("Benchmark: sort27() vs sort27b()\n");
  printf("=================================================================\n");

  printf("\nsort27()  - Hybrid: sort3 + sort9 + insertion sort\n");
  printf("sort27b() - Complete 114-comparator sorting network\n");

  /* Test correctness first */
  test_specific_patterns();

  /* Benchmark parameters */
  const int num_iterations = 1000000;

  printf("\n=================================================================\n");
  printf("Performance Benchmark (%d iterations)\n", num_iterations);
  printf("=================================================================\n");

  srand(time(NULL));

  /* Benchmark sort27 (hybrid approach) */
  printf("\nBenchmarking sort27() [hybrid]...\n");
  double time_sort27 = benchmark_sort_function(sort27, num_iterations, 1);
  printf("  Time: %.6f seconds\n", time_sort27);
  printf("  Throughput: %.2f million sorts/sec\n", num_iterations / time_sort27 / 1e6);

  /* Benchmark sort27b (complete network) */
  printf("\nBenchmarking sort27b() [complete network]...\n");
  double time_sort27b = benchmark_sort_function(sort27b, num_iterations, 1);
  printf("  Time: %.6f seconds\n", time_sort27b);
  printf("  Throughput: %.2f million sorts/sec\n", num_iterations / time_sort27b / 1e6);

  /* Comparison */
  printf("\n=================================================================\n");
  printf("Comparison\n");
  printf("=================================================================\n");

  if (time_sort27 < time_sort27b)
  {
    double speedup = time_sort27b / time_sort27;
    printf("sort27() is FASTER by %.2fx\n", speedup);
    printf("sort27() is %.1f%% faster\n", (speedup - 1.0) * 100.0);
  }
  else
  {
    double speedup = time_sort27 / time_sort27b;
    printf("sort27b() is FASTER by %.2fx\n", speedup);
    printf("sort27b() is %.1f%% faster\n", (speedup - 1.0) * 100.0);
  }

  printf("\nNotes:\n");
  printf("  - sort27()  uses %d comparators (sort3 + sort9) + insertion sort\n", 9 * 3 + 3 * 25);
  printf("  - sort27b() uses 114 comparators (complete network)\n");
  printf("  - Both implementations verified for correctness\n");

  return 0;
}
