#!/bin/bash
#SBATCH -J mn_sanity
#SBATCH -p debug
#SBATCH -N 2
#SBATCH -n 8
#SBATCH -t 00:02:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

set -euo pipefail
echo "JobID=$SLURM_JOB_ID"
echo "NodeList=$SLURM_NODELIST"
echo "NNodes=$SLURM_NNODES NTasks=$SLURM_NTASKS"

echo "---- task map ----"
srun --ntasks=$SLURM_NTASKS bash -lc 'printf "rank=%s host=%s cpus=%s\n" "$SLURM_PROCID" "$(hostname -s)" "$(nproc)"'

echo "---- CPU binding (si aplica) ----"
srun --ntasks=2 bash -lc 'echo "rank=$SLURM_PROCID"; grep -E "Cpus_allowed_list|Mems_allowed_list" /proc/self/status | sed "s/^/  /"'
