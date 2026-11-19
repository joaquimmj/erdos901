#!/usr/bin/env python3
"""Exact optimisation of "join" constructions (generalised Abbott-Hanson).

Take a base B: an (n-r)-uniform non-2-colourable hypergraph with c edges on its
own vertices, and a fresh vertex set W.  Choose R, r-subsets of W, and F,
n-subsets of W.  Edges: e + s for every e in B, s in R; plus F.  Cost c|R|+|F|.
It is non-2-colourable as soon as, for every I subset of W (the red part):
    some s in R lies inside I,  or  some f in F is monochromatic.
(B has a monochromatic edge, say red; then e + s is red.  Sufficient, and
necessary when B has colourings with monochromatic edges of one colour only.)
Abbott-Hanson for n=5: B = Fano, r=2, R = 5 disjoint pairs, F = 16 transversals.

The ILP is solved with HiGHS, optionally on orbits of a group acting on W.
Usage: python3 search/join.py --n 5 --r 2 --w 10 --target 50 --time 600
"""
import argparse, os, sys, time
from itertools import combinations
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hg
from orbits import load_group, orbits

BASES = {1: lambda: [frozenset([0])], 2: hg.triangle, 3: hg.fano,
         4: lambda: hg.read_edges(os.path.join(hg.ROOT, "constructions/seymour_toft.txt")),
         5: lambda: hg.read_edges(os.path.join(hg.ROOT, "constructions/aht51.txt"))}

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, required=True)
ap.add_argument("--r", type=int, required=True, help="size of the part taken in W")
ap.add_argument("--w", type=int, required=True, help="|W|")
ap.add_argument("--group-file", help="group on W: R and F are unions of its orbits")
ap.add_argument("--target", type=int, help="only accept cost <= target")
ap.add_argument("--time", type=float, default=600)
ap.add_argument("--out", default="out/join")
a = ap.parse_args()
n, r, w = a.n, a.r, a.w
base = BASES[n - r](); c = len(base)
gens = load_group(a.group_file)[1] if a.group_file else []
I = np.arange(1 << w, dtype=np.uint32)
cols, cost = [], []          # one boolean column over all I per orbit
orbs = [(o, c) for o in orbits(w, r, gens)] + [(o, 1) for o in orbits(w, n, gens)]
for o, unit in orbs:
    col = np.zeros(1 << w, bool)
    for s in o:
        m = np.uint32(sum(1 << x for x in s))
        col |= ((I & m) == m) if len(s) == r else (((I & m) == m) | ((I & m) == 0))
    cols.append(col); cost.append(unit * len(o))
A = np.unique(np.array(cols).T, axis=0)                 # distinct rows only
A = A[np.lexsort(A.T[::-1])]
print(f"n={n} r={r} base={c} edges, |W|={w}, columns={len(cols)}, rows={len(A)}", flush=True)
assert A.any(axis=1).all(), "some colouring of W cannot be handled at all"
cons = [LinearConstraint(csr_matrix(A.astype(float)), lb=1, ub=np.inf)]
cost = np.array(cost, float)
if a.target:
    cons.append(LinearConstraint(cost.reshape(1, -1), lb=0, ub=a.target))
t0 = time.time()
res = milp(cost, constraints=cons, integrality=np.ones(len(cost)), bounds=Bounds(0, 1),
           options={"time_limit": a.time, "disp": False})
if res.x is None:
    print("infeasible (proved)" if res.status == 2 else "no solution within the time limit"); sys.exit(1)
nR = len(orbits(w, r, gens))
R = [frozenset(s) for i in range(nR) if res.x[i] > 0.5 for s in orbs[i][0]]
F = [frozenset(s) for i in range(len(orbs)) if res.x[i] > 0.5 and i >= nR for s in orbs[i][0]]
vb = max(map(max, base)) + 1
H = [frozenset(set(e) | {vb + x for x in s}) for e in base for s in R] + [frozenset(vb + x for x in f) for f in F]
assert len(set(H)) == c * len(R) + len(F) and hg.proper_coloring(hg.relabel(H)) is None
os.makedirs(a.out, exist_ok=True)
path = os.path.join(a.out, f"join_n{n}_r{r}_w{w}_E{len(H)}.txt")
hg.write_edges(hg.relabel(H), path)
print(f"[{time.time()-t0:.0f}s] cost {len(H)} = {c}*{len(R)} + {len(F)}, optimal={res.status == 0}, "
      f"lower bound {res.mip_dual_bound:.1f} -> {path}")
