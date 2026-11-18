#!/usr/bin/env python3
"""Calibration: for n-uniform hypergraphs on v vertices, run CEGAR with the
a-priori block groups S_{b1} x ... x S_{bk} (partitions of v into <= 4 parts)
and their diagonal variants, and report the optimum each group reaches.

Usage: python3 search/calibrate.py --n 4 --v 11 --time 300 --out out/calib
"""
import argparse, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from math import factorial, prod
from orbits import block_group


def partitions(v, k, lo=1):
    if k == 1:
        return [[v]] if v >= lo else []
    return [[a] + p for a in range(lo, v // k + 1) for p in partitions(v - a, k - 1, a)]


ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=4)
ap.add_argument("--v", type=int, default=11)
ap.add_argument("--time", type=float, default=300)
ap.add_argument("--record", type=int, help="only look for hypergraphs with fewer edges than this")
ap.add_argument("--jobs", type=int, default=os.cpu_count())
ap.add_argument("--out", default="out/calib")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)

jobs = []
for k in range(1, 5):
    for parts in partitions(a.v, k):
        variants = [()]
        for b in sorted(set(parts)):
            js = [j for j, x in enumerate(parts) if x == b]
            if b > 1:
                variants += [tuple(js[:m]) for m in range(2, len(js) + 1)]
        for diag in variants:
            name = "blocks_" + "_".join(("d" if j in diag[1:] else "") + str(x) for j, x in enumerate(parts))
            name = name.replace("_d", "d")   # 4d4_3 = one S_4 acting on both 4-blocks
            v, gens = block_group(parts, diag)
            json.dump({"v": v, "generators": gens}, open(f"{a.out}/{name}.json", "w"))
            order = prod(factorial(x) for j, x in enumerate(parts) if j not in diag[1:])
            jobs.append((name, order))


def run(job):
    name, order = job
    p = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "cegar.py"), "--n", str(a.n),
                    "--v", str(a.v), "--group-file", f"{a.out}/{name}.json", "--time", str(a.time),
                    "--iter-time", str(a.time), "--out", a.out] + (["--record", str(a.record)] if a.record else []), capture_output=True, text=True)
    assert p.returncode == 0, name + ": " + p.stderr[-500:]
    r = json.load(open(f"{a.out}/n{a.n}_v{a.v}_{name}_s0.json"))
    print(f"| `{name}` | {order} | {r['status']} | {r.get('edges', '')} | "
          f"{r.get('last_master_cost', '')} | {r['iterations']} | {r['seconds']} |", flush=True)


print("| group | order | status | edges found | last master cost | iterations | seconds |\n|---|---|---|---|---|---|---|")
with ThreadPoolExecutor(a.jobs) as ex:
    list(ex.map(run, jobs))
