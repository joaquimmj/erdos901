#!/usr/bin/env python3
"""Third independent verifier: shape checks + Glucose, with a different
encoding from make_cnf.py (two variables per vertex, no symmetry breaking).
Usage: check_pysat.py edges.txt   -> exit 0 iff well-formed and non-2-colourable
"""
import sys
from pysat.solvers import Glucose4

edges = [sorted(int(t) for t in l.replace(",", " ").split())
         for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
v = max(map(max, edges)) + 1
n = len(edges[0])
assert all(len(set(e)) == len(e) == n for e in edges), "not uniform"
assert len({tuple(e) for e in edges}) == len(edges), "duplicate edge"
assert set().union(*edges) == set(range(v)), "vertices are not exactly 0..v-1"
red, blue = (lambda x: 2 * x + 1), (lambda x: 2 * x + 2)
with Glucose4() as s:
    for x in range(v):
        s.add_clause([red(x), blue(x)])
        s.add_clause([-red(x), -blue(x)])
    for e in edges:
        s.add_clause([red(x) for x in e])    # not all blue
        s.add_clause([blue(x) for x in e])   # not all red
    sat = s.solve()
print(f"{'2-COLORABLE' if sat else 'NON-2-COLORABLE'} v={v} E={len(edges)} n={n} (glucose)")
sys.exit(1 if sat else 0)
