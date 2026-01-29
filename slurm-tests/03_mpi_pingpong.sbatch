#!/bin/bash
#SBATCH -J mpi-pingpong
#SBATCH -p debug
#SBATCH -N 2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH -t 00:05:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

set -euo pipefail

export PATH=/usr/lib64/mpich/bin:$PATH
export LD_LIBRARY_PATH=/usr/lib64/mpich/lib:$LD_LIBRARY_PATH

echo "JobID=$SLURM_JOB_ID NodeList=$SLURM_NODELIST"
srun --mpi=pmi2 ./03_mpi_pingpong $((1<<20)) 200
srun --mpi=pmi2 ./03_mpi_pingpong $((64<<10)) 500
srun --mpi=pmi2 ./03_mpi_pingpong $((1<<10)) 2000
