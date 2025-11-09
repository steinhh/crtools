/*
 * Optimized sorting networks for small arrays
 *
 * This file contains specialized sorting routines for common window sizes
 * used in image filtering operations. These sorting networks are significantly
 * faster than generic sorting algorithms for small, fixed-size arrays.
 */

/* Include all sorting network implementations */
#include "sorting_networks_generated.c"

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
static void sort_doubles(double *values, int count)
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
    sort25(values);
    break;
  case 26:
    sort26(values);
    break;
  case 27:
    sort27(values);
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
