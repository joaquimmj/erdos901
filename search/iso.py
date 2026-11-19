#!/usr/bin/env python3
"""Isomorphism classes of hypergraph files, via the vertex-edge incidence graph
and igraph's BLISS canonical form.  usage: iso.py a.txt b.txt ...  (same label = isomorphic)"""
import os, sys
import igraph
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hg import read_edges, relabel


def canon(edges):
    edges = relabel(edges); v = max(map(max, edges)) + 1
    g = igraph.Graph(v + len(edges), [(x, v + i) for i, e in enumerate(edges) for x in e])
    color = [0] * v + [1] * len(edges)
    p = g.canonical_permutation(color=color)
    return (v, len(edges), tuple(sorted(g.permute_vertices(p).get_edgelist())))


if __name__ == "__main__":
    seen = {}
    for f in sys.argv[1:]:
        k = canon(read_edges(f))
        print(seen.setdefault(k, len(seen)), f"v={k[0]} E={k[1]}", f)
