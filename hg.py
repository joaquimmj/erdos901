"""Hypergraph helpers and classical constructions for Property B (Erdős #901).

Edge = frozenset of ints. Hypergraph = list of edges on vertices 0..v-1.
"""
from itertools import combinations, product
import os, subprocess, tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(ROOT, "verify", "check2col")


def write_edges(edges, path):
    with open(path, "w") as f:
        for e in edges:
            f.write(" ".join(map(str, sorted(e))) + "\n")


def read_edges(path):
    out = []
    for line in open(path):
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(frozenset(int(t) for t in line.replace(",", " ").split()))
    return out


def relabel(edges):
    """Compact vertex labels to 0..v-1."""
    vs = sorted(set().union(*edges))
    m = {x: i for i, x in enumerate(vs)}
    return [frozenset(m[x] for x in e) for e in edges]


def proper_coloring(edges):
    """Return a proper 2-colouring mask (int) or None if non-2-colourable.
    Uses the independent C brute-force checker (v <= 40)."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        path = f.name
    write_edges(edges, path)
    try:
        r = subprocess.run([CHECK, path], capture_output=True, text=True)
    finally:
        os.unlink(path)
    if r.returncode == 0:
        return None
    if r.returncode == 1:
        return int(r.stdout.split()[1])
    raise RuntimeError(r.stderr)


# ---------- constructions ----------

def triangle():
    return [frozenset(e) for e in combinations(range(3), 2)]


def fano():
    return [frozenset({i % 7, (i + 1) % 7, (i + 3) % 7}) for i in range(7)]


def complete(n):
    """All n-subsets of a (2n-1)-set: trivially non-2-colourable."""
    return [frozenset(e) for e in combinations(range(2 * n - 1), n)]


def abbott_moser_product(A, B):
    """m(ab) <= m(a) * m(b)^a.
    Vertices: (x, y) for x in V(A), y in V(B).  For each edge {x1..xa} of A and
    each choice of edges B1..Ba of B, the edge U_i {x_i} x B_i (size a*b).
    Non-2-colourable: colour x by the colour of a monochromatic B-edge in its
    copy; A has a monochromatic edge in that induced colouring."""
    vA = sorted(set().union(*A)); vB = sorted(set().union(*B))
    idx = {(x, y): i for i, (x, y) in enumerate(product(vA, vB))}
    out = []
    for ea in A:
        ea = sorted(ea)
        for choice in product(B, repeat=len(ea)):
            out.append(frozenset(idx[(x, y)] for x, Bi in zip(ea, choice) for y in Bi))
    return out


def abbott_hanson(H, n):
    """m(n) <= 2^(n-1) + n*m(n-2) for odd n, from an (n-2)-uniform H.
    New vertices a_1..a_n, b_1..b_n.  Edges: e + {a_i, b_i} for every edge e of
    H and every i; and {a_i: i in I} + {b_j: j not in I} for every I of even size.
    Non-2-colourable: H has a monochromatic edge, say red, so every pair
    {a_i, b_i} has a blue vertex; pick one blue vertex per pair with an even
    number of a's (possible if some pair is all blue); otherwise the pairs are
    red/blue and the red transversal has even size because n is odd."""
    assert n % 2 == 1 and all(len(e) == n - 2 for e in H)
    v = max(map(max, H)) + 1
    a = lambda i: v + i
    b = lambda i: v + n + i
    out = [frozenset(e | {a(i), b(i)}) for e in H for i in range(n)]
    for k in range(0, n + 1, 2):
        for I in combinations(range(n), k):
            out.append(frozenset([a(i) for i in I] + [b(j) for j in range(n) if j not in I]))
    return out
