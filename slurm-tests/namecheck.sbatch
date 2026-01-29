#!/bin/bash
#SBATCH -J namecheck
#SBATCH -p debug
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --time=00:03:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

echo "=== NAMECHECK ==="
date
echo "host=$(hostname)"
echo "NodeList=$SLURM_NODELIST"

echo
echo "---- /etc/hosts (relevante) ----"
grep -nE '^(#|$)|\b(master|worker1|worker2)\b' /etc/hosts || true

echo
echo "---- nsswitch.conf (hosts) ----"
grep -nE '^hosts:' /etc/nsswitch.conf || true

echo
echo "---- getent hosts ----"
for h in master worker1 worker2; do
  echo "getent hosts $h:"
  getent hosts "$h" || echo "(NOT FOUND) exit=$?"
done

echo
echo "---- ping corto ----"
ping -c 1 -W 1 worker1 >/dev/null 2>&1 && echo "ping worker1 OK" || echo "ping worker1 FAIL"
ping -c 1 -W 1 worker2 >/dev/null 2>&1 && echo "ping worker2 OK" || echo "ping worker2 FAIL"

echo
echo "DONE"
date
