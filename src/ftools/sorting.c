/*
 * Optimized sorting networks for small arrays
 *
 * This file contains specialized sorting routines for common window sizes
 * used in image filtering operations. These sorting networks are significantly
 * faster than generic sorting algorithms for small, fixed-size arrays.
 */

/* Inline swap macro for sorting networks */
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

/* Sorting network for 25 elements (5x5 window) */
static inline void sort25(double *d)
{
  /* This is a simplified 25-element sorting network */
  /* Using a hybrid approach: partial network + insertion sort for remaining */

  /* First pass: sort groups of 5 */
  for (int i = 0; i < 25; i += 5)
  {
    SWAP(d[i], d[i + 1]);
    SWAP(d[i + 3], d[i + 4]);
    SWAP(d[i], d[i + 2]);
    SWAP(d[i + 1], d[i + 2]);
    SWAP(d[i], d[i + 1]);
    SWAP(d[i + 2], d[i + 3]);
    SWAP(d[i + 1], d[i + 2]);
    SWAP(d[i + 3], d[i + 4]);
    SWAP(d[i + 2], d[i + 3]);
  }

  /* Second pass: merge sorted groups using insertion sort */
  for (int i = 1; i < 25; i++)
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

/* Sorting network for 27 elements (3x3x3 window) */
static inline void sort27(double *d)
{
  /* Optimized sorting network for 27 elements using hierarchical approach */
  /* Stage 1: Sort 9 groups of 3 elements each */
  sort3(&d[0]);
  sort3(&d[3]);
  sort3(&d[6]);
  sort3(&d[9]);
  sort3(&d[12]);
  sort3(&d[15]);
  sort3(&d[18]);
  sort3(&d[21]);
  sort3(&d[24]);

  /* Stage 2: Sort 3 groups of 9 elements each */
  sort9(&d[0]);
  sort9(&d[9]);
  sort9(&d[18]);

  /* Stage 3: Merge three sorted groups of 9 */
  /* Use odd-even merge network for final merging */

  /* Compare across the three groups */
  SWAP(d[0], d[9]);
  SWAP(d[1], d[10]);
  SWAP(d[2], d[11]);
  SWAP(d[3], d[12]);
  SWAP(d[4], d[13]);
  SWAP(d[5], d[14]);
  SWAP(d[6], d[15]);
  SWAP(d[7], d[16]);
  SWAP(d[8], d[17]);

  SWAP(d[9], d[18]);
  SWAP(d[10], d[19]);
  SWAP(d[11], d[20]);
  SWAP(d[12], d[21]);
  SWAP(d[13], d[22]);
  SWAP(d[14], d[23]);
  SWAP(d[15], d[24]);
  SWAP(d[16], d[25]);
  SWAP(d[17], d[26]);

  SWAP(d[0], d[9]);
  SWAP(d[1], d[10]);
  SWAP(d[2], d[11]);
  SWAP(d[3], d[12]);
  SWAP(d[4], d[13]);
  SWAP(d[5], d[14]);
  SWAP(d[6], d[15]);
  SWAP(d[7], d[16]);
  SWAP(d[8], d[17]);

  /* Fine-grained merging within overlapping regions */
  SWAP(d[1], d[9]);
  SWAP(d[2], d[10]);
  SWAP(d[3], d[11]);
  SWAP(d[4], d[12]);
  SWAP(d[5], d[13]);
  SWAP(d[6], d[14]);
  SWAP(d[7], d[15]);
  SWAP(d[8], d[16]);

  SWAP(d[10], d[18]);
  SWAP(d[11], d[19]);
  SWAP(d[12], d[20]);
  SWAP(d[13], d[21]);
  SWAP(d[14], d[22]);
  SWAP(d[15], d[23]);
  SWAP(d[16], d[24]);
  SWAP(d[17], d[25]);

  /* Additional comparisons for complete sorting */
  SWAP(d[2], d[9]);
  SWAP(d[3], d[10]);
  SWAP(d[4], d[11]);
  SWAP(d[5], d[12]);
  SWAP(d[6], d[13]);
  SWAP(d[7], d[14]);
  SWAP(d[8], d[15]);

  SWAP(d[11], d[18]);
  SWAP(d[12], d[19]);
  SWAP(d[13], d[20]);
  SWAP(d[14], d[21]);
  SWAP(d[15], d[22]);
  SWAP(d[16], d[23]);
  SWAP(d[17], d[24]);

  /* Fine adjustments */
  SWAP(d[3], d[9]);
  SWAP(d[4], d[10]);
  SWAP(d[5], d[11]);
  SWAP(d[6], d[12]);
  SWAP(d[7], d[13]);
  SWAP(d[8], d[14]);

  SWAP(d[12], d[18]);
  SWAP(d[13], d[19]);
  SWAP(d[14], d[20]);
  SWAP(d[15], d[21]);
  SWAP(d[16], d[22]);
  SWAP(d[17], d[23]);

  SWAP(d[4], d[9]);
  SWAP(d[5], d[10]);
  SWAP(d[6], d[11]);
  SWAP(d[7], d[12]);
  SWAP(d[8], d[13]);

  SWAP(d[13], d[18]);
  SWAP(d[14], d[19]);
  SWAP(d[15], d[20]);
  SWAP(d[16], d[21]);
  SWAP(d[17], d[22]);

  SWAP(d[5], d[9]);
  SWAP(d[6], d[10]);
  SWAP(d[7], d[11]);
  SWAP(d[8], d[12]);

  SWAP(d[14], d[18]);
  SWAP(d[15], d[19]);
  SWAP(d[16], d[20]);
  SWAP(d[17], d[21]);

  SWAP(d[6], d[9]);
  SWAP(d[7], d[10]);
  SWAP(d[8], d[11]);
  SWAP(d[15], d[18]);
  SWAP(d[16], d[19]);
  SWAP(d[17], d[20]);

  SWAP(d[7], d[9]);
  SWAP(d[8], d[10]);
  SWAP(d[16], d[18]);
  SWAP(d[17], d[19]);

  SWAP(d[8], d[9]);
  SWAP(d[17], d[18]);
}
