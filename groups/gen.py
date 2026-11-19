#!/usr/bin/env python3
"""Write classical groups as generator files: python3 groups/gen.py outdir
frob_p_d: Z_p x| Z_d on p points (d = p-1 is AGL(1,p)); psl_p: PSL(2,p) on p+1 points;
suffix _fK: K extra fixed points; A_x_B: direct product on disjoint point sets."""
import json, os, sys

def root(p):
    return next(g for g in range(2, p) if len({pow(g, k, p) for k in range(p - 1)}) == p - 1)

def frob(p, d):
    m = pow(root(p), (p - 1) // d, p)
    return p, [[(x + 1) % p for x in range(p)], [m * x % p for x in range(p)]]

def psl(p):   # points 0..p-1 and infinity = p
    g2 = pow(root(p), 2, p)
    inv = [p] + [(-pow(x, -1, p)) % p for x in range(1, p)] + [0]
    return p + 1, [[(x + 1) % p for x in range(p)] + [p], [g2 * x % p for x in range(p)] + [p], inv]

def pad(G, k):
    v, gens = G
    return v + k, [g + list(range(v, v + k)) for g in gens]

def prod(A, B):
    (va, ga), (vb, gb) = A, B
    return va + vb, [g + list(range(va, va + vb)) for g in ga] + [list(range(va)) + [va + x for x in g] for g in gb]

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    fano = (7, json.load(open(os.path.join(os.path.dirname(__file__), "fano_psl27.json")))["generators"])
    G = {}
    for p in (11, 13, 17, 19):
        for d in range(2, p):
            if (p - 1) % d == 0:
                G[f"frob_{p}_{d}"] = frob(p, d)
        G[f"psl_{p}"] = psl(p)
    for name in list(G):
        if name.startswith("psl") or name.endswith(f"_{int(name.split('_')[1]) - 1}"):
            for k in (1, 2):
                G[f"{name}_f{k}"] = pad(G[name], k)
    G["psl_7"] = psl(7)
    for k in (8, 9, 10, 11, 12, 13):
        G[f"fano_f{k}"] = pad(fano, k)
    for p, d in ((11, 10), (11, 5), (13, 12), (13, 6)):
        G[f"fano_x_frob_{p}_{d}"] = prod(fano, frob(p, d))
    G["fano_x_psl_7"] = prod(fano, psl(7)); G["fano_x_psl_11"] = prod(fano, psl(11))
    G["psl_7_x_psl_7"] = prod(psl(7), psl(7)); G["fano_x_fano"] = prod(fano, fano)
    G["fano_x_fano_f3"] = pad(G["fano_x_fano"], 3); G["psl_7_x_psl_7_f1"] = pad(G["psl_7_x_psl_7"], 1)
    for name, (v, gens) in G.items():
        if v <= 21:
            json.dump({"v": v, "generators": gens}, open(os.path.join(out, name + ".json"), "w"))
    print(len(G), "groups")
