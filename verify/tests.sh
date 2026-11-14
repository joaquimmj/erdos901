#!/usr/bin/env bash
# Sanity tests for the checker and constructions. Must all pass before any search.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 - <<'EOF'
import sys; sys.path.insert(0, ".")
from hg import *
from itertools import combinations
def check(name, H, expect_non2col):
    r = proper_coloring(H) is None
    assert r == expect_non2col, f"FAIL {name}"
    print(f"ok  {name:32s} E={len(H):5d} non-2-col={r}")
check("triangle (m(2)=3)", triangle(), True)
check("triangle minus edge", triangle()[:2], False)
check("Fano (m(3)=7)", fano(), True)
for i in range(7):
    check(f"Fano minus edge {i}", fano()[:i] + fano()[i+1:], False)
check("K_9^(5) all 5-sets of 9", complete(5), True)
check("all 5-sets of 8 (v too small)", [frozenset(e) for e in combinations(range(8),5)], False)
P = abbott_moser_product(triangle(), fano())
assert len(P) == 147 and all(len(e) == 6 for e in P)
check("Abbott-Moser 2x3 (m(6)<=147)", P, True)
# S(5,6,12)-like sanity: a 6-set and its complement as the only edges -> 2-colourable
check("two complementary 6-sets", [frozenset(range(6)), frozenset(range(6,12))], False)
print("ALL TESTS PASSED")
EOF
