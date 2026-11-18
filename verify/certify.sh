#!/usr/bin/env bash
# Certify that edges.txt is a non-2-colourable uniform hypergraph.
#   1. brute force (verify/check2col)          -- independent C code
#   2. SAT: CNF -> cadical (DRAT proof) -> drat-trim
#   3. shape checks + Glucose with another encoding (verify/check_pysat.py)
# Usage: verify/certify.sh path/to/edges.txt  [outdir]
set -euo pipefail
H="$1"; OUT="${2:-$(dirname "$H")/cert_$(basename "$H" .txt)}"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"
cp "$H" "$OUT/edges.txt"
echo "== 1. brute force"
"$HERE/check2col" "$OUT/edges.txt" | tee "$OUT/bruteforce.log"
grep -q NON-2-COLORABLE "$OUT/bruteforce.log"
echo "== 2. SAT + DRAT"
python3 "$HERE/make_cnf.py" "$OUT/edges.txt" "$OUT/H.cnf"
if command -v cadical >/dev/null && command -v drat-trim >/dev/null; then
  set +e; cadical -q "$OUT/H.cnf" "$OUT/proof.drat" > "$OUT/cadical.log"; rc=$?; set -e
  [ "$rc" = 20 ] || { echo "cadical did not report UNSAT (rc=$rc)"; exit 1; }
  drat-trim "$OUT/H.cnf" "$OUT/proof.drat" | tee "$OUT/drat-trim.log"
  grep -q "s VERIFIED" "$OUT/drat-trim.log"
else
  echo "cadical/drat-trim not installed: SAT step skipped (CI installs them)"
  SKIP=1
fi
echo "== 3. shape + Glucose"
python3 "$HERE/check_pysat.py" "$OUT/edges.txt" | tee "$OUT/pysat.log"
grep -q NON-2-COLORABLE "$OUT/pysat.log"
( cd "$OUT" && sha256sum edges.txt H.cnf > SHA256SUMS )
if [ "${SKIP:-0}" = 1 ]; then echo "PARTIAL (no DRAT): $OUT"; else echo "CERTIFIED (brute force + DRAT + Glucose): $OUT"; fi
