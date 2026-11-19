#!/usr/bin/env python3
"""Independent check of weighted-product bounds (does not import the optimiser).

Reads lines "... n=N best C (published P) weights (u...) sets [(i...), ...] ..." and checks,
from the definition: every set has total weight >= n; the family of sets is non-2-colourable
on the components (all 2^p colourings tried); C = sum over sets of prod m(u_i), with m taken
from the published table and from the lines already checked above.
Usage: python3 verify/check_wprod.py results/wprod/chain.txt
"""
import re, sys, ast
m = {1: 1, 2: 3, 3: 7, 4: 23, 5: 51, 6: 147, 7: 421, 8: 1212, 9: 2401, 10: 7803, 11: 25449,
     12: 55223, 13: 200889, 14: 528218, 15: 857157, 16: 3308499, 17: 10375782}
bad = 0
for line in open(sys.argv[1]):
    g = re.search(r"n=(\d+) best (\d+) .*?weights (\(.*?\)) sets (\[.*\])", line)
    if not g: continue
    n, c = int(g[1]), int(g[2]); u = ast.literal_eval(g[3]); sets = ast.literal_eval(g[4]); p = len(u)
    heavy = all(sum(u[i] for i in s) >= n for s in sets)
    masks = [sum(1 << i for i in s) for s in sets]
    full = (1 << p) - 1
    proper = [x for x in range(1 << p) if not any(x & k == k or (x ^ full) & k == k for k in masks)]
    cost = 0
    for s in sets:
        t = 1
        for i in s: t *= m[u[i]]
        cost += t
    ok = heavy and not proper and cost == c and c < m.get(n, 10 ** 30)
    bad += not ok
    print(f"n={n}: m({n}) <= {c} (table {m.get(n)}) components {p}, sets {len(sets)}: "
          f"weights>={n} {heavy}, non-2-colourable {not proper}, cost recomputed {cost} -> {'OK' if ok else 'FAIL'}")
    if ok: m[n] = c
sys.exit(1 if bad else 0)
