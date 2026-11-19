#!/usr/bin/env python3
"""Local search for a non-2-colourable n-uniform hypergraph with exactly K
edges on v vertices, minimising the exact number of proper 2-colourings.

State: K edges.  cover[c] = number of edges monochromatic under colouring c
(all 2^(v-1) colourings, vertex v-1 fixed to colour 0).  Cost = #{c: cover[c]=0}.
Move: take a random uncovered colouring, add the best of a few random n-sets
monochromatic under it, then drop the edge whose removal uncovers the fewest
colourings (plus noise).  Cost 0 = no proper colouring.

shortcut: memory and time are O(K * 2^v), fine up to v ~ 20; beyond that
sample colourings and confirm with the SAT oracle.

Usage: python3 search/anneal.py --n 4 --v 11 --edges 23 --time 600 --out out/anneal
"""
import argparse, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hg import read_edges, write_edges

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, required=True)
ap.add_argument("--v", type=int, required=True)
ap.add_argument("--edges", type=int, required=True, help="K, number of edges")
ap.add_argument("--start", help="edge file to start from (truncated or padded at random to K edges)")
ap.add_argument("--cands", type=int, default=8, help="candidate edges tried per move")
ap.add_argument("--noise", type=float, default=2.0, help="noise on the choice of the edge to drop")
ap.add_argument("--time", type=float, default=600)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--out", default="out/anneal")
a = ap.parse_args()
n, v, K = a.n, a.v, a.edges
assert 2 * n - 1 <= v <= 26
rng = np.random.default_rng(a.seed)
C = np.arange(1 << (v - 1), dtype=np.uint32)
full = (1 << v) - 1


def mono(m):
    x = C & np.uint32(m)
    return (x == 0) | (x == m)


def rand_edge(pool):
    return sum(1 << int(x) for x in rng.choice(pool, size=n, replace=False))


E = [sum(1 << x for x in e) for e in read_edges(a.start)][:K] if a.start else []
while len(E) < K:
    m = rand_edge(np.arange(v))
    if m not in E:
        E.append(m)
M = np.array([mono(m) for m in E])          # K x 2^(v-1) booleans
cover = M.sum(axis=0, dtype=np.int32)
best, t0, it = None, time.time(), 0
os.makedirs(a.out, exist_ok=True)
state = os.path.join(a.out, f"state_n{n}_v{v}_K{K}_s{a.seed}.txt")   # best state so far, usable as --start
saved, Ebest = t0, list(E)
unmask = lambda ms: [[x for x in range(v) if m >> x & 1] for m in ms]
while time.time() - t0 < a.time:
    it += 1
    bad = np.flatnonzero(cover == 0)
    if best is None or len(bad) < best:
        best, Ebest = len(bad), list(E)
        print(f"[{time.time()-t0:7.1f}s] it={it} proper colourings: {best}", flush=True)
    if len(bad) == 0:
        break
    if time.time() - saved > 600:
        saved = time.time()
        write_edges(unmask(Ebest), state)
    c = int(rng.choice(bad))
    red = [x for x in range(v) if c >> x & 1]
    blue = [x for x in range(v) if not c >> x & 1]
    pools = [p for p in (red, blue) if len(p) >= n]
    cand = {rand_edge(pools[rng.integers(len(pools))]) for _ in range(a.cands)} - set(E)
    if not cand:
        continue
    gains = {m: int(mono(m)[bad].sum()) for m in cand}
    m = max(gains, key=gains.get)
    row = mono(m)
    cover += row
    loss = (M & (cover == 1)).sum(axis=1) + a.noise * rng.random(K) * np.sqrt(len(bad))
    j = int(np.argmin(loss))
    cover -= M[j]
    M[j], E[j] = row, m

write_edges(unmask(Ebest), state)
edges = unmask(E)
if best == 0:
    assert len(set(E)) == K and int((np.array([mono(m) for m in E]).sum(axis=0) == 0).sum()) == 0
    path = os.path.join(a.out, f"anneal_n{n}_v{v}_s{a.seed}_E{K}.txt")
    write_edges(edges, path)
    print(f"non-2-colourable with {K} edges -> {path} (run verify/certify.sh before believing it)")
else:
    print(f"no success: best had {best} proper colourings after {it} moves")
