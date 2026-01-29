#!/bin/bash
#SBATCH -J mpi_allreduce
#SBATCH -N 2
#SBATCH -n 8
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-core=1
#SBATCH -o logs/%x_%j.out
#SBATCH -e logs/%x_%j.err

set -euo pipefail

export PATH=/usr/lib64/mpich/bin:$PATH
export LD_LIBRARY_PATH=/usr/lib64/mpich/lib:$LD_LIBRARY_PATH

MPI_TYPE="${MPI_TYPE:-pmi2}"

echo "JobID=$SLURM_JOB_ID NodeList=$SLURM_NODELIST NNodes=$SLURM_JOB_NUM_NODES NTasks=$SLURM_NTASKS"
echo "Using srun --mpi=${MPI_TYPE}"
srun --mpi="${MPI_TYPE}" --cpu-bind=cores ./02_mpi_allreduce