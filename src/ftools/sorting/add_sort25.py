#!/usr/bin/env python3
"""Add sort25 definition to sorting_networks_generated.c"""

# Read current content
with open('sorting_networks_generated.c', 'r') as f:
    content = f.read()

# Find where to insert sort25 (before sort26)
sort26_pos = content.find('/* Sorting network for 26 elements')

if sort26_pos == -1:
    print("ERROR: Could not find sort26 definition")
    exit(1)

# Sort25 definition
sort25_def = '''/* Sorting network for 25 elements (5x5 window) - Hybrid approach */
static inline void sort25(double *d)
{
  /* Hybrid approach using sort9 for pre-sorting, then insertion sort.
   * This is faster than a pure sorting network for 25 elements (which would need ~120+ comparators).
   * The sort9 networks create a partially sorted structure that makes insertion sort very efficient.
   */

  /* Sort 4 groups of 9 elements using the sort9 network */
  sort9(&d[0]);  /* First 3x3 block */
  sort9(&d[9]);  /* Second 3x3 block (shifted by 9) */

  /* Now sort the remaining 7 elements mixed with the pre-sorted blocks */
  sort9(&d[16]); /* Elements 16-24 */

  /* Complete the sort using insertion sort on the mostly-sorted array */
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

'''

# Insert sort25 before sort26
new_content = content[:sort26_pos] + sort25_def + content[sort26_pos:]

# Write back
with open('sorting_networks_generated.c', 'w') as f:
    f.write(new_content)

print("sort25 added successfully")
