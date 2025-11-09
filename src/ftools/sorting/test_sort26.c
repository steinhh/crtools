#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "sorting.c"

int is_sorted(double *arr, int n)
{
  for (int i = 1; i < n; i++)
  {
    if (arr[i] < arr[i - 1])
      return 0;
  }
  return 1;
}

int main()
{
  srand(time(NULL));
  int num_tests = 10000;
  int failures = 0;

  printf("Testing sort26 with %d random permutations...\n", num_tests);

  for (int t = 0; t < num_tests; t++)
  {
    double arr[26];
    for (int i = 0; i < 26; i++)
    {
      arr[i] = (double)rand() / RAND_MAX * 1000.0;
    }

    sort26(arr);

    if (!is_sorted(arr, 26))
    {
      failures++;
    }
  }

  if (failures == 0)
  {
    printf("? PASSED: All %d tests passed\n", num_tests);
    return 0;
  }
  else
  {
    printf("? FAILED: %d/%d tests failed\n", failures, num_tests);
    return 1;
  }
}
