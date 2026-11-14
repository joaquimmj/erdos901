#!/usr/bin/env python3
"""edges.txt -> DIMACS CNF that is UNSAT iff the hypergraph is not 2-colourable.

Variable x_i (1-based: vertex i -> var i+1) is true iff vertex i is red.
Each edge e gives two clauses: (OR of x_i, i in e) and (OR of -x_i, i in e).
Symmetry breaking: vertex 0 is red (unit clause). Independent of search code.
"""
import sys

edges = []
for line in open(sys.argv[1]):
    line = line.strip()
    if line and not line.startswith("#"):
        edges.append([int(t) for t in line.replace(",", " ").split()])
v = max(max(e) for e in edges) + 1
clauses = [[1]]
for e in edges:
    clauses.append([i + 1 for i in e])
    clauses.append([-(i + 1) for i in e])
out = open(sys.argv[2], "w") if len(sys.argv) > 2 else sys.stdout
out.write(f"p cnf {v} {len(clauses)}\n")
for c in clauses:
    out.write(" ".join(map(str, c)) + " 0\n")
