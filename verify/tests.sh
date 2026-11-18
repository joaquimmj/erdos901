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
Q = abbott_hanson(fano(), 5)
assert len(set(Q)) == 51 and all(len(e) == 5 for e in Q) and set(Q) == set(read_edges("constructions/aht51.txt"))
check("Abbott-Hanson 5 from Fano (m(5)<=51)", Q, True)
check("Abbott-Hanson minus an edge", Q[:-1], False)
# S(5,6,12)-like sanity: a 6-set and its complement as the only edges -> 2-colourable
check("two complementary 6-sets", [frozenset(range(6)), frozenset(range(6,12))], False)
# groups: automorphisms of the 23-edge witness, and CEGAR with given groups
import json, subprocess, tempfile
sys.path.insert(0, "search")
from orbits import automorphisms, load_group, elements
ST = read_edges("constructions/seymour_toft.txt")
check("Seymour-Toft (m(4)=23)", ST, True)
A = automorphisms(ST, 11)
assert len(A) == 144
assert sorted({tuple(sorted({g[x] for g in A})) for x in range(11)}) == [(0,1,2,3), (4,5,6), (7,8,9,10)]
assert set(elements(*load_group("groups/seymour_toft_144.json"))) == set(A)
assert len(elements(*load_group("groups/fano_psl27.json"))) == 168
print("ok  Aut(Seymour-Toft) has order 144, orbits 4+3+4")
for n, v, g, want in [(3, 7, "fano_psl27", 7), (4, 11, "seymour_toft_144", 23), (4, 11, "blocks_3_4d4", 23)]:
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([sys.executable, "search/cegar.py", "--n", str(n), "--v", str(v), "--group-file",
                        f"groups/{g}.json", "--time", "120", "--out", d], check=True, capture_output=True)
        r = json.load(open(f"{d}/n{n}_v{v}_{g}_s0.json"))
    assert r["status"] == "optimal" and r["edges"] == want, r
    print(f"ok  CEGAR n={n} v={v} group {g}: optimum {want}")
# LNS must remove a redundant edge added to Fano
with tempfile.TemporaryDirectory() as d:
    write_edges(fano() + [frozenset({0, 1, 2})], d + "/h.txt")
    subprocess.run([sys.executable, "search/lns.py", "--file", d + "/h.txt", "--wmin", "3", "--wmax", "5",
                    "--time", "5", "--step-time", "10", "--out", d], check=True, capture_output=True)
    assert proper_coloring(read_edges(d + "/lns_s0_E7.txt")) is None
print("ok  LNS reduces Fano + 1 edge back to 7 edges")
print("ALL TESTS PASSED")
EOF
