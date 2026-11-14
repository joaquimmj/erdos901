#!/usr/bin/env python3
"""Greedy edge deletion with random orders: shrink a known non-2-colourable
hypergraph while it stays non-2-colourable.

Usage: python3 search/reduce.py --start product63 --tries 20 --out results/
       python3 search/reduce.py --file some_edges.txt
"""
import argparse, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hg import (proper_coloring, write_edges, read_edges, relabel, fano,
                triangle, abbott_moser_product, complete)

STARTS = {
    "fano": lambda: fano(),
    "product63": lambda: abbott_moser_product(triangle(), fano()),   # n=6, 147 edges
    "product93": lambda: abbott_moser_product(fano(), fano()),       # n=9, 2401 edges
    "complete5": lambda: complete(5),
}


def reduce_once(edges, rng):
    edges = list(edges)
    order = list(range(len(edges)))
    rng.shuffle(order)
    keep = set(range(len(edges)))
    for i in order:
        trial = [edges[j] for j in keep if j != i]
        if proper_coloring(trial) is None:
            keep.discard(i)
    return relabel([edges[j] for j in keep])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", choices=STARTS)
    ap.add_argument("--file")
    ap.add_argument("--tries", type=int, default=10)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    H = read_edges(a.file) if a.file else STARTS[a.start]()
    assert proper_coloring(H) is None, "start hypergraph is 2-colourable!"
    print(f"start: {len(H)} edges, v={len(set().union(*H))}", flush=True)
    rng = random.Random(a.seed)
    best = H
    for t in range(a.tries):
        R = reduce_once(H, rng)
        print(f"try {t}: {len(R)} edges", flush=True)
        if len(R) < len(best):
            best = R
    os.makedirs(a.out, exist_ok=True)
    name = a.start or os.path.basename(a.file)
    path = os.path.join(a.out, f"reduce_{name}_E{len(best)}.txt")
    write_edges(best, path)
    print(f"best: {len(best)} edges -> {path}")


if __name__ == "__main__":
    main()
