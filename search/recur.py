#!/usr/bin/env python3
"""Best upper bound on m(n) obtainable from the published recurrences, all parameters.

Recurrences as stated in Aglave, Amarnath, Shannigrahi, Singh (arXiv:1602.00218v4):
Lemma 1 (Abbott-Moser), Lemma 2 (Abbott-Hanson / Toft), Lemmas 3-4 (Mathews et al.),
Results 1-3 and the general block construction of Section 5.
Usage: python3 search/recur.py [N]     (prints n, bound, rule; '<' marks a value below Table 2)
"""
import sys
from math import comb
TABLE2 = {5: 51, 6: 147, 7: 421, 8: 1212, 9: 2401, 10: 7803, 11: 25449, 12: 55223, 13: 200889,
          14: 528218, 15: 857157, 16: 3308499, 17: 10375782}

m = {1: 1, 2: 3, 3: 7, 4: 23}; why = {}
half = lambda n: comb(n, n // 2) // 2 if n % 2 == 0 else 0
aht = lambda n, core: 2 ** (n - 1) + n * core + half(n)          # Lemma 2 with a core of `core` edges

def partitions(s, lo):                       # multisets of parts >= lo summing to s
    if s == 0: yield (); return
    for p in range(lo, s + 1):
        for rest in partitions(s - p, p): yield (p,) + rest

def candidates(n):
    for a in range(2, n):
        if n % a == 0: yield m[a] * m[n // a] ** a, f"Abbott-Moser a={a} b={n//a}"
    yield aht(n, m[n - 2]), "Abbott-Hanson-Toft"
    ev = n % 2 == 0
    yield ((n + 1) * 2 ** (n - 2) + half(n) + (n - 1) * (m[n - 2] + (comb(n - 2, (n - 2) // 2) if ev else 0)),
           "Mathews et al. (Lemma 3)")
    yield ((n + 4) * 2 ** (n - 3) + (n - 2) * m[n - 2] + (n * comb(n - 2, (n - 2) // 2) // 2 if ev else 0) + half(n),
           "Mathews et al. (Lemma 4)")
    for k in range(1, (n - 1) // 2 + 1):
        yield (comb(n + k - 1, k) * m[n - 2 * k] + comb(n + k - 1, k - 1) * (2 ** (n - 1) + half(n)),
               f"Result 1 k={k}")
        for ks in [p for p in partitions(n, k) if len(p) > 1] + [(k,) * -(-n // k)]:
            t = len(ks); prod = 1
            for q in ks: prod *= m[q]
            yield (m[n - 2 * k] * sum(m[q] ** 2 for q in ks) + (2 ** (t - 1) + half(t)) * prod,
                   f"block k={k} blocks={ks}")
    for k in range(1, n):
        w, x = divmod(n, k); c = m[n - k]
        if x == 0: yield w * c * m[k] + m[k] ** w, f"Result 2 k={k}"; continue
        y, z = divmod(k, x); v = w * c * m[k] + y * m[k] ** w * m[x]
        if z == 0: yield v + c * m[x] ** y, f"Result 2 k={k}"
        else: yield v + comb(x + z - 1, z) * c * m[x] ** y + comb(x + z - 1, x) * m[k] ** w, f"Result 2 k={k}"
    if n % 3 == 1 and n >= 7:
        k = n // 3
        yield ((m[k - 1] + 2 ** (k - 1)) * m[k + 1] ** 2 + 2 * aht(k + 1, m[k - 1]) * m[k] ** 2
               + 4 * m[k + 1] * m[k] ** 2, f"Result 3 k={k}")

if __name__ == "__main__":
  for n in range(5, (int(sys.argv[1]) if len(sys.argv) > 1 else 20) + 1):
    m[n], why[n] = min(candidates(n))
    ref = TABLE2.get(n)
    assert ref is None or m[n] <= ref, (n, m[n], ref)      # every Table 2 value must be reproduced
    print(n, m[n], why[n], f"< {ref}" if ref and m[n] < ref else "", sep="\t")
