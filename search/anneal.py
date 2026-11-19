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
import numba
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
C = np.arange(1 << (v - 1), dtype=np.uint32)   # bit x = 1: vertex x red; vertex v-1 always blue


def mono(m):
    x = C & np.uint32(m)
    return (x == 0) | (x == m)


def rand_edge(pool):
    return sum(1 << int(x) for x in rng.choice(pool, size=n, replace=False))


@numba.njit(cache=True)
def touch(E, cover, uniq, K, j, d, v):
    """Add (d=1) or remove (d=-1) the edge in slot j.  Keeps cover[c] (edges
    monochromatic under c) and uniq[i] (colourings covered by edge i alone).
    Returns the change in the number of uncovered colourings."""
    m = E[j]; full = (1 << (v - 1)) - 1; comp = full & ~m; nb = 0
    for base in (0, m):                    # all blue, then all red
        if base and m >> (v - 1):
            break                          # the top vertex is blue: no all-red colouring
        s = comp
        while True:
            c = base | s
            cover[c] += d
            k = cover[c]
            if d == 1 and k == 1:
                uniq[j] += 1; nb -= 1
            elif d == -1 and k == 0:
                uniq[j] -= 1; nb += 1
            elif k == (3 + d) // 2:        # c now has two owners (add) or one (remove): fix the other owner
                for i in range(K + 1):
                    if i != j and E[i] >= 0 and ((c & E[i]) == 0 or (c & E[i]) == E[i]):
                        uniq[i] -= d
                        break
            if s == 0:
                break
            s = (s - 1) & comp
    return nb


@numba.njit(cache=True)
def run(E, cover, uniq, K, n, v, cands, noise, iters, seed, nbad):
    """iters moves; E has K+1 slots, the last one free (-1)."""
    if seed >= 0:
        np.random.seed(seed)
    full = (1 << (v - 1)) - 1
    best = nbad; Ebest = E[:K].copy(); pick = np.zeros(v, np.int64)
    for it in range(iters):
        if nbad == 0:
            break
        c = np.random.randint(full + 1)
        while cover[c] != 0:
            c = (c + 1) & full
        bm = -1; bg = -1
        for _ in range(cands):
            red = np.random.randint(2)
            k = 0
            for x in np.random.permutation(v):
                if (c >> x) & 1 == red:
                    pick[k] = x; k += 1
            if k < n:
                continue
            m = 0
            for i in range(n):
                m |= 1 << pick[i]
            dup = False
            for i in range(K):
                dup |= E[i] == m
            if dup:
                continue
            g = 0; comp = full & ~m
            for base in (0, m):
                if base and m >> (v - 1):
                    break
                s = comp
                while True:
                    g += cover[base | s] == 0
                    if s == 0:
                        break
                    s = (s - 1) & comp
            if g > bg:
                bg = g; bm = m
        if bm < 0:
            continue
        E[K] = bm
        nbad += touch(E, cover, uniq, K, K, 1, v)
        j = 0; lo = 1e18; sq = noise * np.sqrt(nbad + 1.0)
        for i in range(K):
            l = uniq[i] + sq * np.random.random()
            if l < lo:
                lo = l; j = i
        nbad += touch(E, cover, uniq, K, j, -1, v)
        E[j] = bm; uniq[j] = uniq[K]; uniq[K] = 0; E[K] = -1
        if nbad < best:
            best = nbad; Ebest = E[:K].copy()
    return nbad, best, Ebest


E = [sum(1 << x for x in e) for e in read_edges(a.start)][:K] if a.start else []
while len(E) < K:
    m = rand_edge(np.arange(v))
    if m not in E:
        E.append(m)
E = np.array(E + [-1], dtype=np.int64)
cover = np.zeros(1 << (v - 1), np.int32); uniq = np.zeros(K + 1, np.int64)
saveE = E.copy(); E[:K] = -1
nbad = len(cover)
for j in range(K):
    E[j] = saveE[j]; nbad += touch(E, cover, uniq, K, j, 1, v)
assert nbad == int((cover == 0).sum()) == int((sum(mono(int(m)).astype(np.int32) for m in E[:K]) == 0).sum())
best, t0, it = nbad, time.time(), 0
os.makedirs(a.out, exist_ok=True)
state = os.path.join(a.out, f"state_n{n}_v{v}_K{K}_s{a.seed}.txt")   # best state so far, usable as --start
saved, Ebest, chunk = t0, E[:K].copy(), 200
unmask = lambda ms: [[x for x in range(v) if int(m) >> x & 1] for m in ms]
print(f"[{0.0:7.1f}s] it=0 proper colourings: {best}", flush=True)
while time.time() - t0 < a.time and nbad:
    t1 = time.time()
    nbad, b, Eb = run(E, cover, uniq, K, n, v, a.cands, a.noise, chunk, a.seed if it == 0 else -1, nbad)
    it += chunk
    chunk = max(50, min(10**6, int(chunk * 5 / (time.time() - t1 + 1e-3))))   # about 5 s per call
    if b < best:
        best, Ebest = b, Eb
        print(f"[{time.time()-t0:7.1f}s] it={it} proper colourings: {best}", flush=True)
    if time.time() - saved > 600:
        saved = time.time()
        write_edges(unmask(Ebest), state)
E = [int(m) for m in (E[:K] if nbad == 0 else Ebest)]; best = min(best, nbad)
write_edges(unmask(Ebest), state)
edges = unmask(E)
if best == 0:
    assert len(set(E)) == K and int((np.array([mono(m) for m in E]).sum(axis=0) == 0).sum()) == 0
    path = os.path.join(a.out, f"anneal_n{n}_v{v}_s{a.seed}_E{K}.txt")
    write_edges(edges, path)
    print(f"non-2-colourable with {K} edges -> {path} (run verify/certify.sh before believing it)")
else:
    print(f"no success: best had {best} proper colourings after {it} moves")
