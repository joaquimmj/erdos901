#!/usr/bin/env python3
"""Weighted products: one family that contains the published recursive constructions.

Take components C_1..C_p, where C_i is a u_i-uniform non-2-colourable hypergraph with m(u_i)
edges (u_i = 1: a single vertex).  Choose a family G of subsets S of {1..p} with
sum of u_i over S >= n.  Edges: for every S in G, all unions of one edge from each C_i, i in S
(cut down to n vertices).  Cost: sum over S of prod m(u_i).
Any 2-colouring gives each component a colour in which it has a monochromatic edge; the
hypergraph is non-2-colourable as soon as G is non-2-colourable on {1..p}.
Abbott-Moser, Abbott-Hanson-Toft, the multi-core and block constructions of Aglave et al. are
special cases.  The optimal G for given weights is an exact covering ILP (HiGHS).

Usage: wprod.py --n 5 --weights 3,1,1,1,1,1,1,1,1,1,1          (one weight vector)
       wprod.py --n 6 --sweep 9 [--target 146] [--time 20]     (all multisets of <= 9 weights)
"""
import argparse, sys, time
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix

M = {1: 1, 2: 3, 3: 7, 4: 23, 5: 51, 6: 147, 7: 421, 8: 1212, 9: 2401, 10: 7803, 11: 25449,
     12: 55223, 13: 200889, 14: 528218, 15: 857157, 16: 3308499, 17: 10375782}   # published (Aglave et al., Table 2)

def solve(n, u, target=None, tl=20):
    """min cost of a non-2-colourable G on weights u; returns (cost or None, proved, sets)"""
    p = len(u); u = np.array(u); S = np.arange(1, 1 << p)
    bits = (S[:, None] >> np.arange(p)) & 1
    tot = bits @ u
    S = S[(tot >= n) & (tot - np.where(bits == 1, u, 99).min(axis=1) < n)]   # minimal sets only
    cost = np.array([np.prod([M[x] for x in u[(s >> np.arange(p)) & 1 == 1]], dtype=float) for s in S])
    if target: S, cost = S[cost <= target], cost[cost <= target]
    sig = np.arange(1 << (p - 1))                       # colourings, last component red
    full = (1 << p) - 1
    A = ((sig[:, None] & S) == S) | (((sig[:, None] ^ full) & S) == S)
    if not A.any(axis=1).all(): return None, True, []
    cons = [LinearConstraint(csr_matrix(A).astype(float), lb=1, ub=np.inf)]
    if target: cons.append(LinearConstraint(cost.reshape(1, -1), lb=0, ub=target))
    r = milp(cost, constraints=cons, integrality=np.ones(len(S)), bounds=Bounds(0, 1),
             options={"time_limit": tl, "disp": False})
    if r.x is None: return None, r.status == 2, []
    x = r.x > .5
    return int(round(cost[x].sum())), r.status == 0, [[i for i in range(p) if s >> i & 1] for s in S[x]]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--weights"); ap.add_argument("--sweep", type=int)
    ap.add_argument("--out", help="with --weights (all <= 5): write the explicit hypergraph")
    ap.add_argument("--chain", type=int, help="run n = --n .. CHAIN with --heavy/--ones shapes")
    ap.add_argument("--heavy", type=int, default=4); ap.add_argument("--ones", type=int, default=8)
    ap.add_argument("--target", type=int); ap.add_argument("--time", type=float, default=20)
    ap.add_argument("--known", default="", help="bounds to use instead of the published ones, e.g. 8:1163,13:182064")
    a = ap.parse_args(); n = a.n
    M.update({int(k): int(v) for k, v in (x.split(":") for x in a.known.split(",") if x)})
    if a.weights:
        c, ok, sets = solve(n, [int(x) for x in a.weights.split(",")], a.target, a.time)
        u = [int(x) for x in a.weights.split(",")]
        print("cost", c, "proved optimal/infeasible:", ok)
        for s in sorted(map(tuple, sets)): print(" ", s, [u[i] for i in s])
        if a.out and c:               # explicit hypergraph, components on disjoint vertices
            import os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            import hg; from itertools import product
            base = {1: lambda: [frozenset([0])], 2: hg.triangle, 3: hg.fano,
                    4: lambda: hg.read_edges(os.path.join(hg.ROOT, "constructions/seymour_toft.txt")),
                    5: lambda: hg.read_edges(os.path.join(hg.ROOT, "constructions/aht51.txt"))}
            comp, off = [], 0
            for x in u:
                e = base[x](); comp.append([frozenset(v + off for v in f) for f in e]); off += max(map(max, e)) + 1
            H = {frozenset(sorted(frozenset().union(*t))[:n]) for s in sets for t in product(*(comp[i] for i in s))}
            assert len(H) == c and all(len(e) == n for e in H)
            hg.write_edges(hg.relabel(sorted(H, key=sorted)), a.out); print("written", a.out, "vertices", off)
        sys.exit(0)
    if a.chain:      # n = a.n .. a.chain in order; each improved bound feeds the next ones
        import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import recur
        t0 = time.time()
        for n in range(a.n, a.chain + 1):
            recur.m.update(M); known = M.get(n, 10 ** 30)
            best, how = min(recur.candidates(n)); best = min(best, known)
            how = how if best < known else "known"
            for h in range(1, a.heavy + 1):
                for hv in combinations_with_replacement(range(n - 1, 1, -1), h):
                    for ones in range(0, a.ones + 1):
                        u = hv + (1,) * ones
                        if len(u) < 3 or sum(u) < n: continue
                        c, ok, sets = solve(n, u, best - 1, a.time)
                        if c is not None:
                            best, how = c, f"weights {u} sets {sorted(map(tuple, sets))} proved={ok}"
                            print(f"   [{time.time()-t0:.0f}s] n={n} -> {c}  {how}", flush=True)
            M[n] = best
            print(f"[{time.time()-t0:.0f}s] n={n} best {best} (published {recur.TABLE2.get(n)}) {how}", flush=True)
        sys.exit(0)
    best, t0, unknown = a.target or M[n], time.time(), 0
    for p in range(3, a.sweep + 1):
        for u in combinations_with_replacement(range(n - 1, 0, -1), p):
            c, ok, sets = solve(n, u, best, a.time)
            unknown += not ok
            if c is not None and c <= best:
                tag = "RECORD" if c < M[n] else "ties"
                print(f"[{time.time()-t0:.0f}s] n={n} cost {c} ({tag}; known {M[n]}) weights {u} proved={ok}", flush=True)
                if c < best: best = c
        print(f"[{time.time()-t0:.0f}s] n={n}: all multisets of {p} weights done, best {best}, unresolved {unknown}", flush=True)
