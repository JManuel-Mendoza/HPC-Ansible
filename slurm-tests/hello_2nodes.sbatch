#!/bin/bash
#SBATCH -J hello_2nodes
#SBATCH -p debug
#SBATCH -N 2
#SBATCH -n 2
#SBATCH --ntasks-per-node=1
#SBATCH -w worker1,worker2
#SBATCH -c 1
#SBATCH --time=00:01:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

echo "=== HELLO 2 NODES ==="
date
echo "JobID=$SLURM_JOB_ID NodeList=$SLURM_NODELIST ntasks=$SLURM_NTASKS ntasks_per_node=$SLURM_NTASKS_PER_NODE"
echo

srun -N2 -n2 --ntasks-per-node=1 -l hostname

echo
echo "DONE"
date
