# Runbook: GPU/CUDA (NVIDIA + PyTorch)

Este repo gestiona GPU/CUDA principalmente con:
- `roles/nvidia_cuda/*` (driver, módulos, validación NVML)
- `roles/llm_env/*` (micromamba + PyTorch CUDA)

Vars reales usadas por validaciones (ver `roles/llm_env/defaults/main.yml` y `docs/audit/vars-map.md`):
- `llm_micromamba_bin` (default: `/opt/micromamba/bin/micromamba`)
- `llm_micromamba_root` (default: `/opt/micromamba`)
- `llm_env_name` (default: `llm`)

## Checklist rápida (5 min)

1) ¿Existe `nvidia-smi` y funciona?
```bash
command -v nvidia-smi || echo "nvidia-smi NO existe"
nvidia-smi -L || true
nvidia-smi || true
```

2) ¿Módulos cargados?
```bash
lsmod | grep -E '^nvidia|nvidia_' || true
```

3) Señales de kernel/driver:
```bash
dmesg | tail -n 200
journalctl -k -n 200 --no-pager
```

4) ¿Se ve la GPU por PCI?
```bash
lspci -nn -d 10de: || true
```

## PyTorch CUDA (micromamba)

Si el entorno LLM está instalado (por defecto `llm`):
```bash
/opt/micromamba/bin/micromamba run -n llm python -c "import torch; print('torch', torch.__version__); print('cuda_available', torch.cuda.is_available()); print('device', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no-gpu')"
```

Si se sobreescribieron vars, ajusta el comando usando:
- `llm_micromamba_bin`
- `llm_env_name`

## Problemas comunes

### 1) `nvidia-smi` no existe

Causa típica: driver no instalado (o no se ejecutó la etapa `cuda`).

1. Confirmar GPU presente:
```bash
lspci -nn -d 10de: || true
```
2. Confirmar paquetes/driver (RHEL/Rocky):
```bash
rpm -qa | grep -Ei 'nvidia|cuda' || true
```
3. Evidencia para escalar:
- `lspci -nn -d 10de:`
- `rpm -qa | grep -Ei 'nvidia|cuda'`
- `uname -r`

### 2) `nvidia-smi` falla (errores NVML / “Driver/library version mismatch”)

1. Capturar salida:
```bash
nvidia-smi
```
2. Revisar kernel logs:
```bash
dmesg | tail -n 200
journalctl -k -n 200 --no-pager
```
3. Revisar módulos:
```bash
lsmod | grep -E '^nvidia|nvidia_' || true
modinfo nvidia | head || true
```

Acción típica (si el rol `nvidia_cuda` programó reboot):
- Reiniciar el nodo en ventana controlada y revalidar.

Evidencia para escalar:
- salida completa de `nvidia-smi`
- `dmesg`/`journalctl -k`
- `uname -r`

### 3) Torch no ve CUDA (pero `nvidia-smi` sí funciona)

1. Verificar que el env existe:
```bash
ls -la /opt/micromamba/envs || true
```
2. Ejecutar el check de torch:
```bash
/opt/micromamba/bin/micromamba run -n llm python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available())"
```
3. Si falla por librerías, recopilar:
- stdout/stderr del comando anterior
- `ldconfig -p | grep -Ei 'libcuda|nvidia-ml' || true`
