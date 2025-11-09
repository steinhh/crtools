/*
 * Direct test of sorting networks from sorting.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

/* Include the sorting implementations */
#include "sorting.c"

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
  all_passed &= test_sorting_network(sort4, 4, "sort4");
  all_passed &= test_sorting_network(sort9, 9, "sort9");
  all_passed &= test_sorting_network(sort27, 27, "sort27 (hybrid)");
  all_passed &= test_sorting_network(sort27b, 27, "sort27b (complete network)");

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
