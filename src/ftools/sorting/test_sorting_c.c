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
  all_passed &= test_sorting_network(sort5, 5, "sort5");
  all_passed &= test_sorting_network(sort6, 6, "sort6");
  all_passed &= test_sorting_network(sort7, 7, "sort7");
  all_passed &= test_sorting_network(sort8, 8, "sort8");
  all_passed &= test_sorting_network(sort9, 9, "sort9");
  all_passed &= test_sorting_network(sort11, 11, "sort11");
  all_passed &= test_sorting_network(sort12, 12, "sort12");
  all_passed &= test_sorting_network(sort13, 13, "sort13");
  all_passed &= test_sorting_network(sort14, 14, "sort14");
  all_passed &= test_sorting_network(sort15, 15, "sort15");
  all_passed &= test_sorting_network(sort16, 16, "sort16");
  all_passed &= test_sorting_network(sort17, 17, "sort17");
  all_passed &= test_sorting_network(sort18, 18, "sort18");
  all_passed &= test_sorting_network(sort19, 19, "sort19");
  all_passed &= test_sorting_network(sort20, 20, "sort20");
  all_passed &= test_sorting_network(sort21, 21, "sort21");
  all_passed &= test_sorting_network(sort22, 22, "sort22");
  all_passed &= test_sorting_network(sort23, 23, "sort23");
  all_passed &= test_sorting_network(sort24, 24, "sort24");
  all_passed &= test_sorting_network(sort25, 25, "sort25 (hybrid)");
  all_passed &= test_sorting_network(sort25b, 25, "sort25b (complete network)");
  all_passed &= test_sorting_network(sort26, 26, "sort26");
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
