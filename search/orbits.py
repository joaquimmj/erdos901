"""Permutation groups given by generators, and orbits of n-subsets.

Group file (JSON): {"v": 11, "generators": [[image of 0, image of 1, ...], ...]}
"""
import hashlib, json, os
from itertools import combinations
import numpy as np

CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".cache")


def load_group(path):
    g = json.load(open(path))
    for p in g["generators"]:
        assert sorted(p) == list(range(g["v"])), f"not a permutation of 0..{g['v']-1}: {p}"
    return g["v"], g["generators"]


def builtin(name, v):
    return {"cyclic": [[(i + 1) % v for i in range(v)]], "none": []}[name]


def orbits(v, n, gens):
    """Orbits of n-subsets of 0..v-1 under <gens>: list of sorted lists of tuples.
    Union-find; one pass per generator is enough for the generated group."""
    sets = list(combinations(range(v), n))
    key = hashlib.sha256(json.dumps([v, n, gens]).encode()).hexdigest()[:16]
    path = os.path.join(CACHE, f"orbits_{key}.npy")
    if os.path.exists(path):
        root = np.load(path)
    else:
        idx = {s: i for i, s in enumerate(sets)}
        parent = list(range(len(sets)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i
        for p in gens:
            for i, s in enumerate(sets):
                a, b = find(i), find(idx[tuple(sorted(p[x] for x in s))])
                if a != b:
                    parent[a] = b
        root = np.array([find(i) for i in range(len(sets))])
        os.makedirs(CACHE, exist_ok=True)
        np.save(path, root)
    out = {}
    for s, r in zip(sets, root):
        out.setdefault(int(r), []).append(s)
    return list(out.values())


def elements(v, gens, cap=500):
    """Group elements by breadth-first closure, at most `cap` of them.
    shortcut: for groups larger than cap this is a subset near the identity
    (still sound: any image of a colouring is a valid constraint); switch to
    random products if big groups converge slowly."""
    ident = tuple(range(v))
    seen, queue = {ident}, [ident]
    for g in queue:
        for p in gens:
            h = tuple(p[x] for x in g)
            if h not in seen:
                if len(seen) >= cap:
                    return queue
                seen.add(h)
                queue.append(h)
    return queue


def automorphisms(edges, v):
    """All vertex permutations mapping the edge set to itself (backtracking)."""
    E = {frozenset(e) for e in edges}
    at = [[e for e in E if k in e] for k in range(v)]
    part = {frozenset(s) for e in E for r in range(len(e) + 1) for s in combinations(e, r)}
    out, img, used = [], [None] * v, [False] * v

    def rec(k):
        if k == v:
            out.append(tuple(img))
            return
        for y in range(v):
            if used[y]:
                continue
            img[k] = y
            # the image of the already-mapped part of each edge must lie inside an edge
            if all(frozenset(img[x] for x in e if x <= k) in part for e in at[k]):
                used[y] = True
                rec(k + 1)
                used[y] = False
    rec(0)
    return out


def generators(v, group):
    """Small generating set of a group given by all its elements (greedy)."""
    gens, span = [], {tuple(range(v))}
    for g in group:
        if g not in span:
            gens.append(list(g))
            span = set(elements(v, gens, cap=len(group)))
    return gens


def block_group(parts, diag=()):
    """S_{b1} x ... x S_{bk} on consecutive blocks.  `diag` = indices of
    equal-size blocks on which a single S_b acts simultaneously."""
    starts = [sum(parts[:i]) for i in range(len(parts))]
    v = sum(parts)
    gens = []

    def add(blocks, b):
        if b == 1:
            return
        for cyc in ([1, 0] + list(range(2, b)), [(i + 1) % b for i in range(b)]):
            p = list(range(v))
            for j in blocks:
                for i in range(b):
                    p[starts[j] + i] = starts[j] + cyc[i]
            if p != list(range(v)) and p not in gens:
                gens.append(p)
    if diag:
        assert len({parts[j] for j in diag}) == 1
        add(list(diag), parts[diag[0]])
    for j, b in enumerate(parts):
        if j not in diag:
            add([j], b)
    return v, gens


if __name__ == "__main__":
    # python3 search/orbits.py aut edges.txt out.json    -> automorphism group of a hypergraph
    # python3 search/orbits.py blocks out.json 4 4 3 [--diag 0 1]
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from hg import read_edges
    if sys.argv[1] == "aut":
        H = read_edges(sys.argv[2])
        v = max(map(max, H)) + 1
        A = automorphisms(H, v)
        gens = generators(v, A)
        orb = sorted({tuple(sorted({g[x] for g in A})) for x in range(v)})
        print(f"order {len(A)}, {len(gens)} generators, vertex orbits {orb}")
        out = sys.argv[3]
    else:
        out, rest = sys.argv[2], sys.argv[3:]
        d = rest.index("--diag") if "--diag" in rest else len(rest)
        v, gens = block_group([int(x) for x in rest[:d]], tuple(int(x) for x in rest[d + 1:]))
    json.dump({"v": v, "generators": gens}, open(out, "w"))
