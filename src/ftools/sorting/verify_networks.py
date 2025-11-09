#!/usr/bin/env python3
"""
Verify that all sorting networks in sorting_networks_generated.c match
the definitions in generate_sorting_networks.py
"""

import re
from generate_sorting_networks import networks, parse_network_stage, generate_sort_function

def extract_c_sort_function(c_code, func_name, n):
    """Extract a sort function from C code."""
    # Find the function starting with "static inline void sortN" or "static inline void sortNb"
    # More flexible pattern that captures the function regardless of the comment
    pattern = rf'static inline void {func_name}\(double \*d\)\n{{.*?\n}}'
    match = re.search(pattern, c_code, re.DOTALL)
    if match:
        return match.group(0)
    return None

def normalize_whitespace(code):
    """Normalize whitespace for comparison."""
    # Replace multiple spaces with single space
    code = re.sub(r' +', ' ', code)
    # Remove spaces around punctuation
    code = re.sub(r' *([,();[\]]) *', r'\1', code)
    return code.strip()

def extract_swaps_from_c(c_func):
    """Extract all SWAP calls from C function."""
    swaps = []
    for match in re.finditer(r'SWAP\(d\[(\d+)\]\s*,\s*d\[(\d+)\]\)', c_func):
        a, b = int(match.group(1)), int(match.group(2))
        swaps.append((a, b))
    return swaps

def extract_swaps_from_stages(stages):
    """Extract all swaps from stage definitions."""
    swaps = []
    for stage in stages:
        swaps.extend(stage)
    return swaps

# Read the C file
with open('sorting_networks_generated.c', 'r') as f:
    c_code = f.read()

print("=" * 80)
print("Verifying Sorting Networks Against Python Definitions")
print("=" * 80)
print()

all_match = True
total_checked = 0

for n in sorted(networks.keys()):
    info = networks[n]
    stages = [parse_network_stage(s) for s in info['stages']]
    suffix = info.get('suffix', '')
    function_name = f"sort{n}{suffix}"
    
    # Extract from C file
    c_func = extract_c_sort_function(c_code, function_name, n)
    
    if not c_func:
        print(f"? sort{n}{suffix}: NOT FOUND in C file")
        all_match = False
        continue
    
    # Extract swaps from both
    c_swaps = extract_swaps_from_c(c_func)
    py_swaps = extract_swaps_from_stages(stages)
    
    total_checked += 1
    
    if c_swaps == py_swaps:
        print(f"? sort{n}{suffix}: MATCH ({len(c_swaps)} comparators)")
    else:
        print(f"? sort{n}{suffix}: MISMATCH")
        all_match = False
        
        if len(c_swaps) != len(py_swaps):
            print(f"   C has {len(c_swaps)} comparators, Python has {len(py_swaps)}")
        
        # Find differences
        for i, (c_swap, py_swap) in enumerate(zip(c_swaps, py_swaps)):
            if c_swap != py_swap:
                print(f"   Comparator {i}: C has {c_swap}, Python has {py_swap}")
        
        # Show extra comparators
        if len(c_swaps) > len(py_swaps):
            print(f"   Extra in C: {c_swaps[len(py_swaps):]}")
        elif len(py_swaps) > len(c_swaps):
            print(f"   Missing in C: {py_swaps[len(c_swaps):]}")

print()
print("=" * 80)
if all_match:
    print(f"? ALL {total_checked} SORTING NETWORKS MATCH!")
else:
    print(f"? SOME SORTING NETWORKS DO NOT MATCH")
print("=" * 80)
