/*
 * Direct test of sorting networks from sorting.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

/* Copy the sorting network code */
#define SWAP(a, b)                           \
  do                                         \
  {                                          \
    double tmp_swap = (a);                   \
    (a) = ((a) > (b)) ? (b) : (a);           \
    (b) = ((b) > tmp_swap) ? (b) : tmp_swap; \
  } while (0)

/* Sorting network for 3 elements */
static inline void sort3(double *d)
{
  SWAP(d[0], d[1]);
  SWAP(d[1], d[2]);
  SWAP(d[0], d[1]);
}

/* Sorting network for 9 elements (3x3 window) */
static inline void sort9(double *d)
{
  /* Stage 1: Sort columns */
  SWAP(d[0], d[1]);
  SWAP(d[3], d[4]);
  SWAP(d[6], d[7]);
  SWAP(d[1], d[2]);
  SWAP(d[4], d[5]);
  SWAP(d[7], d[8]);
  SWAP(d[0], d[1]);
  SWAP(d[3], d[4]);
  SWAP(d[6], d[7]);
  /* Stage 2: Sort rows */
  SWAP(d[0], d[3]);
  SWAP(d[3], d[6]);
  SWAP(d[0], d[3]);
  /* Stage 3: Merge */
  SWAP(d[1], d[4]);
  SWAP(d[4], d[7]);
  SWAP(d[1], d[4]);
  SWAP(d[2], d[5]);
  SWAP(d[5], d[8]);
  SWAP(d[2], d[5]);
  SWAP(d[1], d[3]);
  SWAP(d[5], d[7]);
  SWAP(d[2], d[6]);
  SWAP(d[4], d[6]);
  SWAP(d[2], d[4]);
  SWAP(d[2], d[3]);
  SWAP(d[5], d[6]);
}

/* Sorting network for 27 elements (3x3x3 window) */
static inline void sort27(double *d)
{
  /* Hybrid approach for 27 elements.
   * A pure sorting network for 27 elements is complex (~170-200 comparators).
   * This hybrid uses proven sorting networks for initial structure,
   * then completes with insertion sort.
   * Performance: The pre-sorting makes insertion sort very efficient (mostly sorted input).
   * Correctness: Guaranteed by insertion sort.
   */

  /* Stage 1: Sort 9 groups of 3 elements each using sort3 network (27 comparators) */
  sort3(&d[0]);
  sort3(&d[3]);
  sort3(&d[6]);
  sort3(&d[9]);
  sort3(&d[12]);
  sort3(&d[15]);
  sort3(&d[18]);
  sort3(&d[21]);
  sort3(&d[24]);

  /* Stage 2: Sort 3 groups of 9 elements each using sort9 network */
  sort9(&d[0]);
  sort9(&d[9]);
  sort9(&d[18]);

  /* Stage 3: Complete the sort using insertion sort on the mostly-sorted array */
  /* After stages 1&2, most elements are close to their final positions */
  for (int i = 1; i < 27; i++)
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

/* Helper function to check if array is sorted */
int is_sorted(double *arr, int n)
{
  for (int i = 1; i < n; i++)
  {
    if (arr[i] < arr[i - 1])
    {
      return 0;
    }
  }
  return 1;
}

/* Test function */
int test_sorting_network(void (*sort_func)(double *), int n, const char *name)
{
  int num_tests = 10000;
  int failures = 0;

  printf("Testing %s with %d random permutations...\n", name, num_tests);

  for (int t = 0; t < num_tests; t++)
  {
    double arr[n];

    /* Fill with random values */
    for (int i = 0; i < n; i++)
    {
      arr[i] = (double)rand() / RAND_MAX * 1000.0 - 500.0;
    }

    /* Sort using the network */
    sort_func(arr);

    /* Check if sorted */
    if (!is_sorted(arr, n))
    {
      failures++;
      if (failures <= 3)
      {
        printf("  FAILED at test %d:\n  ", t);
        for (int i = 0; i < n; i++)
        {
          printf("%.2f ", arr[i]);
        }
        printf("\n");
      }
    }
  }

  if (failures == 0)
  {
    printf("  ? PASSED: All %d tests passed\n\n", num_tests);
    return 1;
  }
  else
  {
    printf("  ? FAILED: %d/%d tests failed\n\n", failures, num_tests);
    return 0;
  }
}

int main()
{
  srand(time(NULL));

  printf("==================================================\n");
  printf("Sorting Network Verification (C)\n");
  printf("==================================================\n\n");

  int all_passed = 1;

  all_passed &= test_sorting_network(sort3, 3, "sort3");
  all_passed &= test_sorting_network(sort9, 9, "sort9");
  all_passed &= test_sorting_network(sort27, 27, "sort27");

  printf("==================================================\n");
  if (all_passed)
  {
    printf("? ALL TESTS PASSED\n");
  }
  else
  {
    printf("? SOME TESTS FAILED\n");
  }
  printf("==================================================\n");

  return all_passed ? 0 : 1;
}
