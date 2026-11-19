#!/bin/bash
# Upper bounds for m(n, v): lower K one by one while anneal.py still succeeds.
# usage: descend.sh n v K0 seed seconds outdir
n=$1; v=$2; K=$3; seed=$4; end=$(( $(date +%s) + $5 )); out=$6; start=""
mkdir -p "$out"
while left=$(( end - $(date +%s) )); [ $left -gt 60 ]; do
  python3 "$(dirname "$0")/anneal.py" --n $n --v $v --edges $K --seed $seed --time $left $start --out "$out" | tail -n 1
  f="$out/anneal_n${n}_v${v}_s${seed}_E${K}.txt"
  [ -f "$f" ] || break
  start="--start $f"; K=$((K - 1))     # anneal truncates the start file to K edges
done
echo "m($n,$v) <= $((K + 1)) (seed $seed)"
