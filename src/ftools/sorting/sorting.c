/*
 * Optimized sorting networks for small arrays
 *
 * This file contains specialized sorting routines for common window sizes
 * used in image filtering operations. These sorting networks are significantly
 * faster than generic sorting algorithms for small, fixed-size arrays.
 */

/* Include all sorting network implementations */
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

/* Insertion sort for small arrays (much faster than qsort for n < ~40) */
static void insertion_sort(double *values, int count)
{
  for (int i = 1; i < count; i++)
  {
    double key = values[i];
    int j = i - 1;

    /* Move elements greater than key one position ahead */
    while (j >= 0 && values[j] > key)
    {
      values[j + 1] = values[j];
      j--;
    }
    values[j + 1] = key;
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

/* Hybrid sort: specialized sorting networks for common sizes, fallback to generic sorts */
static void sort_doubles_fast(double *values, int count)
{
  if (count <= 1)
  {
    return;
  }

  /* Use specialized sorting networks for common window sizes */
  switch (count)
  {
  case 2:
    SWAP(values[0], values[1]);
    break;
  case 3:
    sort3(values);
    break;
  case 4:
    sort4(values);
    break;
  case 5:
    sort5(values);
    break;
  case 6:
    sort6(values);
    break;
  case 7:
    sort7(values);
    break;
  case 8:
    sort8(values);
    break;
  case 9:
    sort9(values);
    break;
  case 11:
    sort11(values);
    break;
  case 12:
    sort12(values);
    break;
  case 13:
    sort13(values);
    break;
  case 14:
    sort14(values);
    break;
  case 15:
    sort15(values);
    break;
  case 16:
    sort16(values);
    break;
  case 17:
    sort17(values);
    break;
  case 18:
    sort18(values);
    break;
  case 19:
    sort19(values);
    break;
  case 20:
    sort20(values);
    break;
  case 21:
    sort21(values);
    break;
  case 22:
    sort22(values);
    break;
  case 23:
    sort23(values);
    break;
  case 24:
    sort24(values);
    break;
  case 25:
    sort25b(values);
    break;
  case 26:
    sort26(values);
    break;
  case 27:
    sort27b(values);
    break;
  case 124:
    sort124(values);
    break;
  case 125:
    sort125(values);
    break;
  default:
    /* For other sizes, use insertion sort or qsort */
    if (count < 40)
    {
      insertion_sort(values, count);
    }
    else
    {
      qsort(values, count, sizeof(double), compare_double);
    }
    break;
  }
}

static void sort_doubles_safe(double *values, int count)
{
  qsort(values, count, sizeof(double), compare_double);
}

static void sort_doubles(double *values, int count)
{
  if (1)
  {
    sort_doubles_fast(values, count);
  }
  else
  {
    sort_doubles_safe(values, count);
  }
}