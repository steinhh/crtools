// Benchmark: compare sort_doubles (specialized networks) vs qsort
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

/* Include project sorting code (dispatch and generated networks) */
#include "sorting.c"

static double rand_double()
{
  return (double)rand() / (double)RAND_MAX * 2000.0 - 1000.0;
}

static long long timespec_to_ns(const struct timespec *t)
{
  return (long long)t->tv_sec * 1000000000LL + t->tv_nsec;
}

int compare_double_qsort(const void *a, const void *b)
{
  double da = *(const double *)a;
  double db = *(const double *)b;
  if (da < db)
    return -1;
  if (da > db)
    return 1;
  return 0;
}

int main(int argc, char **argv)
{
  (void)argc;
  (void)argv;
  srand(42);

  int sizes[] = {2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27};
  const int nsizes = sizeof(sizes) / sizeof(sizes[0]);

  const int iters = 200000; /* total sorts per size (may be reduced for large sizes) */

  printf("Benchmarking sort_doubles (networks) vs qsort\n");
  printf("Iterations per size: %d\n", iters);
  printf("------------------------------------------------------------\n");

  for (int si = 0; si < nsizes; ++si)
  {
    int n = sizes[si];
    /* adjust iterations for larger sizes to limit runtime */
    int its = iters;
    if (n >= 20)
      its = iters / 10;
    if (n >= 24)
      its = iters / 20;

    double *arr = malloc(sizeof(double) * n);
    double *tmp = malloc(sizeof(double) * n);
    if (!arr || !tmp)
    {
      fprintf(stderr, "alloc failed\n");
      return 1;
    }

    struct timespec t0, t1;

    /* warmup */
    for (int k = 0; k < 100; ++k)
    {
      for (int i = 0; i < n; ++i)
        arr[i] = rand_double();
      sort_doubles(arr, n);
    }

    /* Benchmark sort_doubles */
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (int k = 0; k < its; ++k)
    {
      for (int i = 0; i < n; ++i)
        tmp[i] = rand_double();
      sort_doubles(tmp, n);
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    long long ns_network = timespec_to_ns(&t1) - timespec_to_ns(&t0);

    /* Benchmark qsort */
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (int k = 0; k < its; ++k)
    {
      for (int i = 0; i < n; ++i)
        tmp[i] = rand_double();
      qsort(tmp, n, sizeof(double), compare_double_qsort);
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    long long ns_qsort = timespec_to_ns(&t1) - timespec_to_ns(&t0);

    double per_network_ns = (double)ns_network / (double)its;
    double per_qsort_ns = (double)ns_qsort / (double)its;

    printf("n=%2d: network: %10.0f ns/sort (%.1f sorts/sec), qsort: %10.0f ns/sort (%.1f sorts/sec), ratio qsort/network: %.2f\n",
           n,
           per_network_ns,
           1e9 / per_network_ns,
           per_qsort_ns,
           1e9 / per_qsort_ns,
           per_qsort_ns / per_network_ns);

    free(arr);
    free(tmp);
  }

  return 0;
}
