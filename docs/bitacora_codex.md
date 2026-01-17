# Bitacora Codex

## Table of Contents
- TBD

## 2026-01-16 11:04 (America/Bogota) — micromamba missing on PATH
**Context:** hosts: all; playbook: site.yml; tags: llm; branch: codex
**Symptom:** bash: micromamba: command not found
**Root cause:** micromamba binary is installed under /opt/micromamba/bin but not on shell PATH.
**Fix:** add an Ansible task to symlink /opt/micromamba/bin/micromamba to /usr/local/bin/micromamba.
**Files changed:** roles/llm_env/tasks/main.yml, docs/bitacora_codex.md
**Validation:** run `which micromamba` (expect `/usr/local/bin/micromamba`), then `micromamba --version` (expect version output); fallback ` /opt/micromamba/bin/micromamba --version`.
**Rollback:** remove symlink (`rm /usr/local/bin/micromamba`) and revert the task in `roles/llm_env/tasks/main.yml`.
**Notes:** none.

## 2026-01-16 11:29 (America/Bogota) — llm env missing in micromamba
**Context:** hosts: all; playbook: site.yml; tags: llm; branch: codex
**Symptom:** `micromamba env list` shows only `base`; `micromamba run -n llm ...` fails because env does not exist.
**Root cause:** llm env creation was not enforced with a root prefix and idempotent check, so env was never created on the expected root.
**Fix:** add an idempotent env creation task using `MAMBA_ROOT_PREFIX=/opt/micromamba`, plus a pip install step gated by a marker file; set the same root prefix for validate's torch check.
**Files changed:** roles/llm_env/tasks/main.yml, roles/validate/tasks/main.yml, docs/bitacora_codex.md
**Validation:** run `micromamba env list` (expect `llm` present), `micromamba run -n llm python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"` (expect torch import and CUDA boolean), and `ansible-playbook -i inventario.ini site.yml --tags llm`.
**Rollback:** remove the new tasks from `roles/llm_env/tasks/main.yml` and the env prefix from `roles/validate/tasks/main.yml`, then remove the env with `/opt/micromamba/bin/micromamba env remove -n llm` if needed.
**Notes:** fallback commands: `/opt/micromamba/bin/micromamba env list` and `/opt/micromamba/bin/micromamba run -n llm ...`.

## 2026-01-16 12:01 (America/Bogota) — conda changed status + pip hash marker
**Context:** hosts: all; playbook: site.yml; tags: llm; branch: codex
**Symptom:** "Install/update conda packages in existing env" reports changed even when micromamba prints "All requested packages already installed"; pip install is skipped due to a static marker.
**Root cause:** command module marks changed unless overridden; pip marker used a fixed filename, so it never re-runs when the package list changes.
**Fix:** set `changed_when` to false when micromamba reports no changes; compute a sha1 hash of `llm_pip_packages` and use a hashed marker file so pip installs re-run only when the package list changes.
**Files changed:** roles/llm_env/tasks/main.yml, docs/bitacora_codex.md
**Validation:** `ansible-playbook -i inventario.ini site.yml --limit hpc_master --tags llm` (expect conda task OK when no changes; pip install skips unless package list changes).
**Rollback:** revert the `changed_when` and hash marker edits in `roles/llm_env/tasks/main.yml`, then remove any `/.llm_pip_installed_*` marker files if needed.
**Notes:** none.

## 2026-01-16 17:57 (America/Bogota) — master LLM smoke test (non-destructive)
**Context:** host: master; playbook: site.yml; tags: llm; branch: codex
**Symptom:** N/A (smoke test)
**Root cause:** N/A
**Fix:** N/A (read-only verification)
**Files changed:** docs/bitacora_codex.md
**Validation:** commands and outputs captured below.

`git status -sb`
```
## codex...origin/codex/inicial
```

`micromamba env list`
```
  Name  Active  Path                    
──────────────────────────────────────────
  base  *       /opt/micromamba         
  llm           /opt/micromamba/envs/llm
```

`micromamba run -n llm python -c "import torch; print('torch', torch.__version__); print('cuda', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no-gpu')"`
```
torch <version>
cuda False
no-gpu
```

`nvidia-smi`
```
bash: nvidia-smi: command not found
```

**Rollback:** N/A
**Notes:** CUDA not available on this host (`cuda False`, `no-gpu`); `nvidia-smi` is not available. Next step: proceed with CPU-only path or identify a GPU-capable node for CUDA validation.

## 2026-01-16 18:05 (America/Bogota) — NVIDIA driver/module diagnosis (master)
**Context:** host: master; playbook: site.yml; tags: cuda; branch: codex
**Symptom:** torch reports `cuda False` and `nvidia-smi` is missing, despite NVIDIA GPU present.
**Root cause:** NVIDIA driver stack is not installed/loaded; nouveau kernel module is active.
**Fix:** N/A (diagnosis only).
**Files changed:** docs/bitacora_codex.md
**Validation:** commands and outputs captured below.

`which nvidia-smi || true`
```
/usr/bin/which: no nvidia-smi in (/usr/lib64/openmpi/bin:/opt/micromamba/bin:/home/sistemas/.codex/tmp/path/codex-arg0LDEZNR:/usr/lib/node_modules/@openai/codex/vendor/x86_64-unknown-linux-musl/path:/usr/lib64/openmpi/bin:/home/sistemas/.local/bin:/home/sistemas/bin:/opt/micromamba/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin)
```

`rpm -qa | grep -Ei 'nvidia|cuda' || true`
```
```

`lsmod | grep -Ei 'nvidia|nouveau' || true`
```
nouveau              3624960  1
drm_ttm_helper         16384  1 nouveau
gpu_sched              69632  1 nouveau
drm_gpuvm              49152  1 nouveau
drm_exec               16384  2 drm_gpuvm,nouveau
mxm_wmi                12288  1 nouveau
drm_client_lib         16384  2 i915,nouveau
ttm                   126976  3 drm_ttm_helper,i915,nouveau
drm_display_helper    319488  2 i915,nouveau
drm_kms_helper        266240  5 drm_display_helper,drm_ttm_helper,drm_client_lib,i915,nouveau
drm                   843776  14 gpu_sched,drm_kms_helper,drm_exec,drm_gpuvm,drm_display_helper,drm_buddy,drm_ttm_helper,drm_client_lib,i915,ttm,nouveau
video                  77824  3 dell_wmi,i915,nouveau
i2c_algo_bit           20480  3 igb,i915,nouveau
wmi                    45056  10 dell_wmi_sysman,video,intel_wmi_thunderbolt,dell_wmi,dell_wmi_aio,wmi_bmof,dell_smbios,dell_wmi_descriptor,mxm_wmi,nouveau
```

`ls -la /dev/nvidia* 2>/dev/null || true`
```
```

`uname -r`
```
5.14.0-611.16.1.el9_7.x86_64
```

**Rollback:** N/A
**Notes:** Driver stack appears missing and nouveau is loaded. Minimal next step: run the `nvidia_cuda` role (with nouveau blacklisting and driver install) on the master, then reboot if needed.

## 2026-01-16 18:12 (America/Bogota) — harden nvidia_cuda install path (nouveau + validation)
**Context:** host: master; playbook: site.yml; tags: cuda; branch: codex
**Symptom:** `nvidia-smi` missing, `nouveau` loaded, torch reports `cuda False`.
**Root cause:** nouveau driver active and proprietary NVIDIA driver stack not installed/loaded.
**Fix:** add tasks to detect nouveau, trigger reboot when needed, and validate `nvidia-smi` plus kernel module state after install; keep repo-based driver install unchanged.
**Files changed:** roles/nvidia_cuda/tasks/main.yml, docs/bitacora_codex.md
**Validation:** run `ansible-playbook -i inventario.ini site.yml --tags cuda` (expect nouveau blacklisted, drivers installed, and `nvidia-smi` available); verify `lsmod | grep -i nvidia` and `nvidia-smi` output post-reboot if auto reboot is enabled.
**Rollback:** revert the added tasks in `roles/nvidia_cuda/tasks/main.yml`; if needed, remove the blacklist file `/etc/modprobe.d/blacklist-nouveau.conf` and rebuild initramfs manually.
**Notes:** reboot only occurs when `nvidia_cuda_auto_reboot` is true and nouveau was loaded or initramfs/drivers changed.

## 2026-01-16 18:22 (America/Bogota) — ensure cuda role handles nouveau + driver install
**Context:** host: master; playbook: site.yml; tags: cuda; branch: codex
**Symptom:** `nvidia-smi` missing; `lsmod` shows `nouveau` loaded; torch reports `cuda False`; no NVIDIA/CUDA RPMs installed.
**Root cause:** nouveau driver active and proprietary NVIDIA driver stack not installed.
**Fix:** ensure nvidia_cuda role blacklists nouveau, rebuilds initramfs when the blacklist changes, triggers reboot when needed, installs drivers from the NVIDIA CUDA repo, and validates `nvidia-smi` plus kernel modules.
**Files changed:** roles/nvidia_cuda/tasks/main.yml, docs/bitacora_codex.md
**Validation:** run `ansible-playbook -i inventario.ini site.yml --tags cuda --limit hpc_master` (expect `nvidia-smi` available after reboot if triggered; `lsmod | grep -i nvidia` shows modules).
**Rollback:** revert the added tasks in `roles/nvidia_cuda/tasks/main.yml`; remove `/etc/modprobe.d/blacklist-nouveau.conf` and rebuild initramfs manually if needed.
**Notes:** reboot only occurs when `nvidia_cuda_auto_reboot` is true and nouveau was loaded or initramfs/drivers changed.

## 2026-01-16 18:33 (America/Bogota) — fix modular filtering for cuda-drivers on RHEL9
**Context:** host: master; playbook: site.yml; tags: cuda; branch: codex
**Symptom:** `cuda-drivers` install fails with "All matches were filtered out by modular filtering for argument: cuda-drivers"; CUDA repo is enabled and `nvidia-driver` module exists.
**Root cause:** DNF module streams for `nvidia-driver`/`cuda` filter the CUDA repo packages unless modules are reset/disabled or module_hotfixes is set.
**Fix:** add module reset/disable steps for `nvidia-driver` and `cuda`, enable `module_hotfixes=1` for the CUDA repo stanza, and refresh DNF cache only when these settings change.
**Files changed:** roles/nvidia_cuda/tasks/main.yml, docs/bitacora_codex.md
**Validation:** `dnf module list --enabled | grep -Ei 'nvidia|cuda' || true`, then `ansible-playbook -i inventario.ini site.yml --limit hpc_master --tags cuda --diff` (expect driver install succeeds).
**Rollback:** revert the module reset/disable and repo hotfix edits in `roles/nvidia_cuda/tasks/main.yml`.
**Notes:** no changes to driver package names; install still uses `{{ nvidia_cuda_driver_pkg }}` and `{{ nvidia_cuda_toolkit_pkg }}`.

## 2026-01-16 18:58 (America/Bogota) — nvidia-smi rc=9 after install
**Context:** host: master; playbook: site.yml; tags: cuda; branch: codex
**Symptom:** `nvidia-smi` returns rc=9 with "NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver."
**Root cause:** kernel driver not loaded yet; reboot pending after nouveau blacklist/initramfs rebuild and driver install.
**Fix:** N/A (requires reboot, no code changes in this step).
**Files changed:** docs/bitacora_codex.md
**Validation:** post-reboot checklist:
  - `lsmod | grep -Ei 'nouveau|nvidia'` (expect `nvidia` modules loaded, `nouveau` absent)
  - `ls -la /dev/nvidia*` (expect device nodes present)
  - `nvidia-smi` (expect GPU details without error)
  - `micromamba run -n llm python -c "import torch; print('cuda', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no-gpu')"` (expect `cuda True` and GPU name)
**Rollback:** N/A
**Notes:** reboot is required after blacklist/dracut and driver install, before validation tasks.
