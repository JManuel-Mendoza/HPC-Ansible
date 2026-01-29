#!/bin/bash
#SBATCH -J cpu_stress_5m
#SBATCH -p debug
#SBATCH -N 1
#SBATCH -w worker1
#SBATCH -c 8
#SBATCH --time=00:06:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

echo "=== CPU STRESS (stress-ng) ==="
date
hostname
echo "SLURM_JOB_ID=$SLURM_JOB_ID"
echo "CPUS_ON_NODE=$SLURM_CPUS_ON_NODE"
echo "CPUS_PER_TASK=$SLURM_CPUS_PER_TASK"

# Carga CPU fija a los CPUs solicitados
stress-ng --cpu "$SLURM_CPUS_PER_TASK" --cpu-method matrixprod --timeout 5m --metrics-brief

echo "DONE"
date
