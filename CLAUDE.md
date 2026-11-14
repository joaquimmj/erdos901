# Instructions for Claude Code sessions on this repository

- Full brief: `docs/PROMPT.md`. Follow its Phase 0 (live novelty check) before any new claim.
- **Heavy compute does NOT run in the Claude session.** Write or improve the code, push it to a branch, then have the `search` workflow run it on GitHub Actions (with `gh workflow run search.yml -f n=6 -f v_list=...` if gh is available, otherwise ask Joaquim to launch it). Read the results on the `results` branch.
- Before every launch, state the minutes cost (number of v values × number of seeds × minutes). The quota is 2,000 min/month on a private repo. Never launch more than 600 min without approval.
- Commits are made under Joaquim's name only. No `Co-Authored-By: Claude` line and no mention of Claude in commit messages.
- Never name his university on public material: "Paris" only. His personal e-mail never appears anywhere.
- Never post anything publicly (erdosproblems.com, OEIS, arXiv, issues, e-mails). Write drafts in `drafts/`.
- Work on a `dev` branch, and merge into `main` once validated.

## Suggested next steps
1. Add groups other than Z_v (affine Z_p ⋊ Z_k, Z_a × Z_b, PSL(2,q)) to `search/cegar.py`. Pure cyclic symmetry seems too restrictive (see the 33 vs 23 result for n=4, v=11).
2. Seed the master with structured colourings (balanced, block-structured) to speed up convergence.
3. Add local search (simulated annealing on the number of surviving colourings) from the Abbott–Moser product, with vertex-swap moves (not just deletion: the 147 construction is edge-critical).
4. For v > 32, the oracle switches to PySAT/CaDiCaL (`pysat_oracle`), which is installed in CI.
