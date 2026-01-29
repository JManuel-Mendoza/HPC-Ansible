#!/bin/bash
#SBATCH -J torch-gloo
#SBATCH -p debug
#SBATCH -N 2
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH -t 00:05:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

set -euo pipefail

# Activa entorno
source /nfs-hpc/slurm-tests/env_llm.sh

# Recomendado para evitar oversubscription de hilos
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

# Master para env://
export MASTER_ADDR=192.168.34.1 
export MASTER_PORT=$((15000 + SLURM_JOB_ID % 20000))

export TORCH_DISTRIBUTED_DEBUG=DETAIL
export GLOO_LOG_LEVEL=DEBUG

srun bash -lc '
IFACE=$(ip -o -4 addr show | awk '"'"'$4 ~ /^192\.168\.34\./ {print $2; exit}'"'"')
echo "host=$(hostname) iface=$IFACE ip=$(hostname -I) rank=${SLURM_PROCID}/${SLURM_NTASKS}"
export GLOO_SOCKET_IFNAME=$IFACE
python ./04_torch_gloo_allreduce.py
'
