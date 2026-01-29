#!/bin/bash
#SBATCH -J gpu_stress_10m_w1
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH -w worker1
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --time=00:15:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

echo "=== GPU STRESS 10m (torch) ==="
date
hostname
echo "SLURM_JOB_ID=$SLURM_JOB_ID"
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
echo

# Activa entorno
source /nfs-hpc/slurm-tests/env_llm.sh

# Control de recursos
sudo nvidia-smi -i 0 -pm 1
sudo nvidia-smi -i 0 -ac 2504,1101

# Monitoreo GPU cada 2s (queda en el mismo log)
echo "---- nvidia-smi dmon (2s) ----"
nvidia-smi dmon -s pucm -d 2 -o DT &
DMON_PID=$!

python3 - <<'PY'
import time, torch, os
assert torch.cuda.is_available(), "CUDA no disponible dentro del job"
dev = torch.device("cuda:0")
print("torch:", torch.__version__)
print("gpu:", torch.cuda.get_device_name(0))

# Quadro P1000 ~4GB: tamaños seguros para stress sostenido
# Si quieres más carga, sube N poco a poco (4096->5120) y/o usa float32.
N = 4096
dtype = torch.float16

a = torch.randn((N, N), device=dev, dtype=dtype)
b = torch.randn((N, N), device=dev, dtype=dtype)

# Warmup
for _ in range(20):
    _ = a @ b
torch.cuda.synchronize()

t0 = time.time()
t_end = t0 + 600  # 10 min
iters = 0
last = t0

while time.time() < t_end:
    _ = a @ b
    iters += 1
    if iters % 50 == 0:
        torch.cuda.synchronize()
        now = time.time()
        print(f"iters={iters} elapsed_s={now - t0:.1f} step_s={(now-last):.2f}")
        last = now

torch.cuda.synchronize()
print("DONE iters=", iters, "total_s=", time.time()-t0)
PY

# Detener dmon
kill $DMON_PID 2>/dev/null || true
echo
echo "---- nvidia-smi final ----"
nvidia-smi || true

echo "DONE"
date

# Restablecer control de recursos
sudo nvidia-smi -i 0 -rac
