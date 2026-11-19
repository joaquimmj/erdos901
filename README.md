# erdos901: searching for smaller hypergraphs without Property B

A hypergraph has **Property B** if its vertices can be coloured red and blue so that no edge is all one colour.
Let m(n) be the smallest number of edges of an n-uniform hypergraph **without** Property B.
[Erdős problem #901](https://www.erdosproblems.com/901) asks how m(n) grows.

Only three values are known exactly: m(2) = 3, m(3) = 7 (the Fano plane) and m(4) = 23.
The best known upper bounds are m(5) ≤ 51, **m(6) ≤ 147**, m(7) ≤ 421 and m(9) ≤ 2401.

This repository searches for a 6-uniform hypergraph without Property B with **fewer than 147 edges**, and certifies
everything it claims.

## Status

- **No construction below 147 edges found so far.** A first search for n = 6 over 22 to 26 vertices found none.
- The 147-edge Abbott–Moser construction (3 · 7², on 21 vertices) is reproduced, verified to have no 2-colouring,
  and is **edge-critical**: removing any single edge makes it 2-colourable.
- Sanity check: the search rediscovers m(3) = 7 (the Fano plane), with and without symmetry.
- For n = 4 on 11 vertices, the smallest construction invariant under cyclic shifts has 33 edges, well above
  m(4) = 23. Cyclic symmetry alone is too restrictive.
- The search now takes any permutation group (`--group-file`). With S_4 acting on two blocks of 4 vertices at once
  and S_3 on a block of 3, chosen without looking at the known witness, it rediscovers m(4) = 23 in under a second.
  See `REPORT.md` (in French) for the full calibration.

The problem stays open.

## How it works

**Search (CEGAR).** An integer program proposes a set of edges, invariant under a symmetry group, that blocks every
2-colouring found so far. An oracle (brute force or a SAT solver) then looks for a 2-colouring that the proposed set
does not block. If it finds one, the colouring is added as a new constraint and the loop starts again. If it finds
none, the set has no 2-colouring and is a candidate.

**Certification.** A candidate counts only if it passes three independent checks:
1. a brute-force checker in C that tries all 2^(v−1) colourings, and
2. a SAT encoding (UNSAT means no 2-colouring) solved by CaDiCaL, whose DRAT proof is checked by drat-trim, and
3. shape checks plus a second SAT encoding solved by Glucose (`verify/check_pysat.py`).

## Layout

| Path | Role |
|---|---|
| `verify/check2col.c` | brute-force checker over all 2^(v−1) colourings (OpenMP) |
| `verify/make_cnf.py` | hypergraph to DIMACS CNF |
| `verify/certify.sh` | brute force + CaDiCaL DRAT proof + drat-trim + Glucose |
| `verify/check_pysat.py` | third verifier: shape checks and Glucose, different encoding |
| `verify/tests.sh` | sanity tests: triangle, Fano plane, Fano minus an edge, complete hypergraphs, the 147-edge product |
| `hg.py` | constructions (Fano, complete, Abbott–Moser product) |
| `search/cegar.py` | CEGAR search for constructions invariant under a group (`--group-file`), resumable (`--state`) |
| `search/orbits.py` | group files, orbits of n-sets, automorphisms of a hypergraph, block groups |
| `search/calibrate.py` | runs the search over all block groups for a given n and v |
| `groups/` | permutation groups as JSON generators |
| `constructions/seymour_toft.txt` | the 23-edge witness for m(4), from OEIS A392185 |
| `search/anneal.py` | direct local search on the number of proper 2-colourings, no symmetry; finds 23 edges for n = 4 in seconds |
| `search/lns.py` | large-neighbourhood search around a known construction |
| `search/reduce.py` | greedy edge deletion from a known construction |
| `.github/workflows/` | tests on every push, and a parallel search launched by hand |

## Run it

```bash
make test
python3 search/cegar.py --n 3 --v 7 --group none --record 8      # rediscovers the Fano plane
python3 search/cegar.py --n 6 --v 21 --group cyclic --record 147 --time 600
python3 search/cegar.py --n 4 --v 11 --group-file groups/blocks_3_4d4.json    # rediscovers m(4) = 23
```

Larger searches run on GitHub Actions: **Actions → search → Run workflow**, with n, the vertex counts, the record
to beat and the minutes per job. Each vertex count runs as a parallel job, any record-breaker is certified at the
end, and a summary is written to the `results` branch.

## References

- H. L. Abbott and L. Moser, On a combinatorial problem of Erdős and Hajnal, *Canad. Math. Bull.* 7 (1964), 177–181.
- Erdős problem #901: <https://www.erdosproblems.com/901>

Joaquim Manji-Jung, Paris.
