#!/usr/bin/env python3
"""CEGAR search for the cheapest G-invariant non-2-colourable n-uniform
hypergraph on v vertices (G = Z_v cyclic, trivial, or any group from a JSON
file of generators, see search/orbits.py).

Master: 0/1 ILP (scipy.optimize.milp / HiGHS) choosing G-orbits of n-sets,
        minimising the number of edges, subject to: every colouring seen so
        far has a monochromatic chosen edge.
Oracle: find a proper 2-colouring of the master's hypergraph
        (C brute force for v <= 32, PySAT/CaDiCaL otherwise).
        If none exists, the master's solution is OPTIMAL among G-invariant
        hypergraphs on v vertices (the master solves a relaxation).
        Otherwise add the colouring and its G-images as new constraints.

Usage:
  python3 search/cegar.py --n 6 --v 21 --group cyclic --record 147 \
          --time 3000 --out results/
"""
import argparse, json, os, sys, time
from itertools import combinations
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hg import proper_coloring, write_edges
from orbits import load_group, builtin, orbits, elements
import subprocess, tempfile
ORACLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oracle")


def many_colorings(edges, k):
    """Up to k diverse proper 2-colourings (brute force helper, v <= 32)."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        path = f.name
    write_edges(edges, path)
    try:
        out = subprocess.run([ORACLE, path, str(k)], capture_output=True, text=True).stdout
    finally:
        os.unlink(path)
    return [int(x) for x in out.split()]


def masks(edges):
    return np.array([sum(1 << x for x in e) for e in edges], dtype=np.uint64)


def pysat_oracle(edges, v):
    from pysat.solvers import Cadical153
    with Cadical153() as s:
        s.add_clause([v])  # vertex v-1 (var v) fixed true
        for e in edges:
            s.add_clause([x + 1 for x in e]); s.add_clause([-(x + 1) for x in e])
        if not s.solve():
            return None
        m = s.get_model()
        return sum(1 << (abs(l) - 1) for l in m if l > 0 and abs(l) <= v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--v", type=int, required=True)
    ap.add_argument("--group", default="cyclic", choices=["cyclic", "none"])
    ap.add_argument("--group-file", help="JSON group (see search/orbits.py); overrides --group")
    ap.add_argument("--state", help="JSON file of colourings seen: loaded at start, saved as we go")
    ap.add_argument("--record", type=int, default=10**9, help="known upper bound")
    ap.add_argument("--time", type=float, default=3000, help="seconds budget")
    ap.add_argument("--init", type=int, default=300, help="random initial colourings")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--per-iter", type=int, default=50,
                    help="proper colourings added per CEGAR iteration")
    ap.add_argument("--iter-time", type=float, default=120,
                    help="max seconds per master ILP (incumbent used if not optimal)")
    ap.add_argument("--target", type=int, default=None,
                    help="only accept hypergraphs with <= target edges (default record-1)")
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    if a.target is None and a.record < 10**9:
        a.target = a.record - 1   # only look for record-breakers
    t0 = time.time()
    rng = np.random.default_rng(a.seed)
    n, v = a.n, a.v
    if a.group_file:
        gv, gens = load_group(a.group_file)
        assert gv == v, f"group file is on {gv} vertices, not {v}"
        a.group = os.path.splitext(os.path.basename(a.group_file))[0]
    else:
        gens = builtin(a.group, v)
    orbs = orbits(v, n, gens)
    group = elements(v, gens)
    sizes = np.array([len(o) for o in orbs], dtype=float)
    em = [masks(o) for o in orbs]
    allm = np.concatenate(em)
    owner = np.concatenate([np.full(len(o), i) for i, o in enumerate(orbs)])
    log = lambda *x: print(f"[{time.time()-t0:7.1f}s]", *x, flush=True)
    log(f"n={n} v={v} group={a.group} orbits={len(orbs)} n-sets={len(allm)}")

    rows = []          # list of arrays of orbit indices hit by each colouring
    seen = set()

    def add_coloring(c):
        bits = [i for i in range(v) if c >> i & 1]
        for g in group:
            r = sum(1 << g[i] for i in bits)
            if r in seen or ((1 << v) - 1 - r) in seen:
                continue
            seen.add(r)
            x = allm & np.uint64(r)
            mono = (x == 0) | (x == allm)
            hit = np.unique(owner[mono])
            if len(hit) == 0:
                return False  # no n-set mono: impossible to kill (v too small)
            rows.append(hit)
        return True

    def save_state():
        if a.state:
            json.dump(sorted(seen), open(a.state + ".tmp", "w"))
            os.replace(a.state + ".tmp", a.state)

    if a.state and os.path.exists(a.state):
        for c in json.load(open(a.state)):
            add_coloring(c)
        log(f"resumed {len(rows)} colourings from {a.state}")
    # balanced random initial colourings (the hardest ones)
    for _ in range(a.init):
        k = v // 2 + int(rng.integers(0, 2))
        S = rng.choice(v, size=k, replace=False)
        if not add_coloring(int(sum(1 << int(s) for s in S))):
            log("v too small: a colouring has no monochromatic n-set"); return
    best = None
    last = {}
    it = 0
    status = "timeout"
    while time.time() - t0 < a.time:
        it += 1
        data = np.concatenate([np.ones(len(h)) for h in rows])
        ri = np.concatenate([np.full(len(h), i) for i, h in enumerate(rows)])
        ci = np.concatenate(rows)
        A = csr_matrix((data, (ri, ci)), shape=(len(rows), len(orbs)))
        left = max(5.0, min(a.iter_time, a.time - (time.time() - t0)))
        cons = [LinearConstraint(A, lb=1, ub=np.inf)]
        if a.target is not None:
            cons.append(LinearConstraint(sizes.reshape(1, -1), lb=0, ub=a.target))
        res = milp(sizes, constraints=cons,
                   integrality=np.ones(len(orbs)), bounds=Bounds(0, 1),
                   options={"time_limit": left, "disp": False})
        if res.x is None:
            if res.status == 2:
                # infeasible with the target: proven no G-invariant hypergraph <= target
                status = "infeasible_at_target"; break
            status = "master_no_incumbent"; continue  # time-limited, retry while budget remains
        chosen = [i for i in range(len(orbs)) if res.x[i] > 0.5]
        cost = int(sum(sizes[i] for i in chosen))
        lb = int(np.ceil(res.fun - 1e-6)) if res.status == 0 else None
        edges = [e for i in chosen for e in orbs[i]]
        last = {"last_master_cost": cost, "last_master_optimal": res.status == 0,
                "lower_bound_this_v": cost if res.status == 0 else None}
        if v <= 32:
            cs = many_colorings(edges, a.per_iter)
            c = cs[0] if cs else None
        else:
            c = pysat_oracle(edges, v); cs = [c] if c is not None else []
        if it % 10 == 0 or c is None:
            log(f"it={it} rows={len(rows)} master_cost={cost} optimal={res.status==0}")
        if c is None:
            if best is None or cost < best[0]:
                best = (cost, edges)
                log(f"non-2-colourable hypergraph with {cost} edges (optimal={res.status==0})")
            if res.status == 0:
                status = "optimal"; break
            # incumbent only (time limit): demand something strictly cheaper and continue
            a.target = cost - 1
            status = "feasible"
            continue
        for cc in cs:
            add_coloring(cc)
        if it % 10 == 0:
            save_state()
    save_state()

    os.makedirs(a.out, exist_ok=True)
    tag = f"n{n}_v{v}_{a.group}_s{a.seed}"
    rep = {"n": n, "v": v, "group": a.group, "seed": a.seed, "status": status,
           "iterations": it, "constraints": len(rows), "seconds": round(time.time() - t0, 1),
           "record": a.record, **last}
    if best:
        rep["edges"] = best[0]
        rep["beats_record"] = best[0] < a.record
        write_edges(best[1], os.path.join(a.out, f"{tag}_E{best[0]}.txt"))
        if status == "optimal":
            rep["claim"] = (f"min edges of a {a.group}-invariant non-2-colourable "
                            f"{n}-uniform hypergraph on {v} vertices = {best[0]}")
    json.dump(rep, open(os.path.join(a.out, f"{tag}.json"), "w"), indent=1)
    log(json.dumps(rep))
    if best and best[0] < a.record:
        log("!!! CANDIDATE BEATS RECORD — run verify/certify.sh before believing it")


if __name__ == "__main__":
    main()
