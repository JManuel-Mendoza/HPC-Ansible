#!/bin/bash
#SBATCH -J mn_sanity2
#SBATCH -p debug
#SBATCH -N 2
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-core=1
#SBATCH --hint=nomultithread

#SBATCH -t 00:02:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

set -euo pipefail
echo "JobID=$SLURM_JOB_ID NodeList=$SLURM_NODELIST"
echo "NNodes=$SLURM_NNODES NTasks=$SLURM_NTASKS cpus-per-task=$SLURM_CPUS_PER_TASK"

srun --cpu-bind=verbose,cores --distribution=block:block bash -lc '
echo "rank=$SLURM_PROCID host=$(hostname) nproc=$(nproc)"
grep -E "Cpus_allowed_list|Mems_allowed_list" /proc/self/status
taskset -pc $$
'

