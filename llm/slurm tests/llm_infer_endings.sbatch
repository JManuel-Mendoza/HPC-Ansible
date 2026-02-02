#!/bin/bash
#SBATCH -J llm-infer-end
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
CKPT="${CKPT:-$BASE/checkpoints/gpt2-tinystories-express/checkpoint-2000}"

echo "JobID: ${SLURM_JOB_ID}"
echo "Node:  ${SLURM_NODELIST}"
nvidia-smi

export HF_HOME="$BASE/hf_cache"
export TRANSFORMERS_CACHE="$BASE/hf_cache/transformers"
export HF_DATASETS_CACHE="$BASE/hf_cache/datasets"
export TOKENIZERS_PARALLELISM=false

CKPT="$CKPT" micromamba run -n llm python "$BASE/code/infer_gpt2.py"
