#!/usr/bin/env python3
from generate_sorting_networks import networks, parse_network_stage, generate_sort_function

# Get the sort11 definition
n = 11
spec = networks[n]
stages = [parse_network_stage(s) for s in spec['stages']]

# Generate the function
code = generate_sort_function(n, stages)
print(code)
