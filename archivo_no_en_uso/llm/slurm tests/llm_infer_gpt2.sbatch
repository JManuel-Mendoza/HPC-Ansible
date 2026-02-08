#!/bin/bash
#SBATCH -J llm-infer
#SBATCH -p debug
#SBATCH --nodelist=master
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH -t 00:10:00
#SBATCH -o /srv/nfs/llm-express/logs/%x-%j.out
#SBATCH -e /srv/nfs/llm-express/logs/%x-%j.err

set -euo pipefail

BASE="/srv/nfs/llm-express"
##CKPT="$BASE/checkpoints/gpt2-tinystories-express/checkpoint-2000"

CKPT=/srv/nfs/llm-express/models/gpt2-tinystories-ckpt2000

echo "JobID: ${SLURM_JOB_ID}"
echo "Node:  ${SLURM_NODELIST}"

nvidia-smi

# Opcional: caches (no debería bajar nada si ya está todo local)
export HF_HOME="$BASE/hf_cache"
export TRANSFORMERS_CACHE="$BASE/hf_cache/transformers"
export HF_DATASETS_CACHE="$BASE/hf_cache/datasets"

# Ejecuta inferencia
CKPT="$CKPT" micromamba run -n llm python "$BASE/code/infer_gpt2.py"
