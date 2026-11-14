# erdos901 — Property B search (Erdős problem #901)

m(n) = minimum number of edges of an n-uniform hypergraph that is **not 2-colourable**.
Known: m(2)=3, m(3)=7, m(4)=23. Upper bounds to beat (verify the current table first, see `docs/PROMPT.md` Phase 0):
m(5) ≤ 51, **m(6) ≤ 147** (Abbott–Moser product 3·7², reproduced here), m(7) ≤ 421, m(9) ≤ 2401.

Everything runs **in the cloud, for free**: on GitHub Actions (CPU runners). Your Mac does nothing.

## Layout
| path | role |
|---|---|
| `verify/check2col.c` | independent brute-force checker (all 2^(v−1) colourings, OpenMP) |
| `verify/make_cnf.py` | hypergraph → DIMACS CNF (UNSAT ⇔ non-2-colourable) |
| `verify/certify.sh` | brute force + CaDiCaL DRAT proof + drat-trim |
| `verify/tests.sh` | sanity tests: triangle, Fano, Fano−e, complete, 147-edge product… |
| `hg.py` | constructions (Fano, complete, Abbott–Moser product) |
| `search/cegar.py` | exact CEGAR search for Z_v-invariant constructions (ILP master + SAT/brute-force oracle) |
| `search/reduce.py` | greedy edge deletion from a known construction |
| `.github/workflows/ci.yml` | tests on each push |
| `.github/workflows/search.yml` | **parallel cloud search** (manual launch) → results on the `results` branch |

## Run a search in the cloud
GitHub → **Actions** → **search** → **Run workflow**. Fill in n, the vertex counts, the record, and the minutes per job.
Each v value becomes a parallel job. At the end, the `collect` job certifies any record-breaker. It then writes `SUMMARY.md` to the `results` branch.

**Budget:** a private repo on GitHub Free gets 2,000 free minutes per month. One launch costs (number of v values) × (number of seeds) × minutes.
The spending limit defaults to $0, so GitHub stops the runs instead of charging.
A public repo has unlimited minutes, but makes the work visible before publication.

## Run locally (optional)
```
make test
python3 search/cegar.py --n 3 --v 7 --group none --record 8     # rediscovers Fano
python3 search/cegar.py --n 6 --v 21 --group cyclic --record 147 --time 600
```

## Status (checked so far)
- Tests pass. The CEGAR rediscovers m(3) = 7 (Fano), with or without symmetry.
- The Abbott–Moser product (21 vertices, 147 edges) is verified non-2-colourable, and it is **edge-critical**: greedy deletion removes nothing.
- The minimum Z_11-invariant non-2-colourable 4-uniform hypergraph on 11 vertices has 33 edges, which is above m(4) = 23. Cyclic symmetry alone is too restrictive there.

## Rules
Nothing is claimed without `certify.sh` (brute force + DRAT verified). Nothing is posted publicly without the author's validation.

Author: Joaquim Manji-Jung, Paris.
