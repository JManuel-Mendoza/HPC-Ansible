#!/bin/bash
#SBATCH -J llm-clm-end
#SBATCH -p debug
#SBATCH --nodelist=master
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=24G
#SBATCH -t 03:00:00
#SBATCH -o /srv/nfs/llm-express/logs/%x-%j.out
#SBATCH -e /srv/nfs/llm-express/logs/%x-%j.err

set -euo pipefail

BASE="/srv/nfs/llm-express"

# Punto de arranque: usa el checkpoint-2000 (o cámbialo a tu artefacto congelado)
START_MODEL="${START_MODEL:-$BASE/checkpoints/gpt2-tinystories-express/checkpoint-2000}"

# Nuevo output para esta fase (no pisa el anterior)
OUTDIR="$BASE/checkpoints/gpt2-tinystories-endings"

mkdir -p "$BASE/logs" "$OUTDIR"

echo "=== SLURM ==="
echo "JobID: ${SLURM_JOB_ID}"
echo "Node:  ${SLURM_NODELIST}"
echo "START_MODEL: $START_MODEL"
echo "OUTDIR: $OUTDIR"
echo "CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES-<unset>}"

echo "=== NVIDIA-SMI (before) ==="
nvidia-smi || true

# Caches en /srv/nfs
export HF_HOME="$BASE/hf_cache"
export TRANSFORMERS_CACHE="$BASE/hf_cache/transformers"
export HF_DATASETS_CACHE="$BASE/hf_cache/datasets"
export TOKENIZERS_PARALLELISM=false

# Red / NCCL (single-node: no crítico, pero consistente)
export NCCL_IB_DISABLE=1
export NCCL_SOCKET_IFNAME=enp3s0f0
export NCCL_DEBUG=WARN

# Terminar antes del timelimit de Slurm (170m = 2h50m)
timeout 170m micromamba run -n llm python "$BASE/code/train_clm_with_end.py" \
  --model_name_or_path "$START_MODEL" \
  --output_dir "$OUTDIR" \
  --cache_dir "$BASE/hf_cache" \
  --block_size 256 \
  --max_steps 5000 \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 8 \
  --learning_rate 5e-5 \
  --warmup_steps 50 \
  --logging_steps 25 \
  --save_steps 200 \
  --save_total_limit 2 \
  --preproc_workers 4 \
  --seed 42

echo "=== NVIDIA-SMI (after) ==="
nvidia-smi || true
echo "DONE"
