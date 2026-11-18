#!/usr/bin/env python3
"""Large-neighbourhood search from a known non-2-colourable hypergraph.

Repeat: pick a small vertex set W, free every edge meeting W, and ask CEGAR
(no symmetry) for strictly fewer replacement edges meeting W that keep the
hypergraph non-2-colourable.  Each step is exact when CEGAR ends with
"infeasible_at_target": no such replacement exists for that W.

Usage: python3 search/lns.py --file constructions/aht51.txt --time 3000 --out out/lns
"""
import argparse, glob, json, os, random, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hg import read_edges, write_edges, proper_coloring

ap = argparse.ArgumentParser()
ap.add_argument("--file", required=True)
ap.add_argument("--wmin", type=int, default=2)
ap.add_argument("--wmax", type=int, default=4)
ap.add_argument("--step-time", type=float, default=300, help="seconds per neighbourhood")
ap.add_argument("--time", type=float, default=3000)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--out", default="out/lns")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
rng = random.Random(a.seed)
H = read_edges(a.file)
n, v = len(H[0]), max(map(max, H)) + 1
assert proper_coloring(H) is None, "start hypergraph is 2-colourable!"
t0 = time.time()
while time.time() - t0 < a.time:
    W = set(rng.sample(range(v), rng.randint(a.wmin, a.wmax)))
    fixed = [e for e in H if not e & W]
    free = len(H) - len(fixed)
    d = os.path.join(a.out, f"step_s{a.seed}")
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(d + "/*"):
        os.unlink(f)
    write_edges(fixed, d + "/fixed.txt")
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "cegar.py"), "--n", str(n), "--v", str(v),
                    "--group", "none", "--fixed", d + "/fixed.txt", "--touch", ",".join(map(str, sorted(W))),
                    "--target", str(free - 1), "--init", "0", "--time", str(a.step_time),
                    "--iter-time", str(a.step_time), "--out", d], capture_output=True)
    r = json.load(open(glob.glob(d + "/n*.json")[0]))
    print(f"[{time.time()-t0:7.0f}s] W={sorted(W)} free={free} -> {r['status']} {r.get('edges', '')}", flush=True)
    if r.get("edges", len(H)) < len(H):
        H = read_edges(glob.glob(d + "/n*_E*.txt")[0])
        assert proper_coloring(H) is None and len(H) == r["edges"]
        write_edges(H, os.path.join(a.out, f"lns_s{a.seed}_E{len(H)}.txt"))
        print(f"!!! improved to {len(H)} edges — run verify/certify.sh before believing it", flush=True)
