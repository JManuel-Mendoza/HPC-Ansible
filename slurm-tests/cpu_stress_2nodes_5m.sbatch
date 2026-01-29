#!/bin/bash
#SBATCH -J cpu_stress_2nodes_5m
#SBATCH -p debug
#SBATCH -N 2
#SBATCH -n 2
#SBATCH --ntasks-per-node=1
#SBATCH -w worker1,worker2
#SBATCH -c 8
#SBATCH --time=00:10:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

echo "=== CPU STRESS 2 NODES (stress-ng) ==="
date
echo "JobID=$SLURM_JOB_ID"
echo "NodeList=$SLURM_NODELIST"
echo "Tasks=$SLURM_NTASKS  CpusPerTask=$SLURM_CPUS_PER_TASK"

srun -N2 -n2 --ntasks-per-node=1 -c "$SLURM_CPUS_PER_TASK" bash -lc '
  echo "--- host=$(hostname) start=$(date) ---"
  echo "Cpus_allowed_list=$(grep Cpus_allowed_list /proc/self/status | awk "{print \$2}")"
  taskset -p $$
  stress-ng --cpu "$SLURM_CPUS_PER_TASK" --cpu-method matrixprod --timeout 5m --metrics-brief
#  stress-ng --cpu "$SLURM_CPUS_PER_TASK" --cpu-method matrixprod --timeout 1m --metrics-brief --taskset 0
  echo "--- host=$(hostname) end=$(date) ---"
'

echo "DONE"
date
