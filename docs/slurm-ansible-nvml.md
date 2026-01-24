# Slurm + NVML (AutoDetect=nvml) - Reporte detallado

## 1) Objetivo y alcance
Este reporte documenta el proceso completo para que Slurm funcione con
AutoDetect=nvml, priorizando estabilidad y deteccion automatica de GPUs sin
plantillas manuales. El nombre exacto de GPU queda como formalidad posterior;
el objetivo principal es que slurmd detecte NVML, reporte GRES correctos y
permita ejecutar jobs GPU sin DRAIN/INVALID_REG.

Alcance:
- Hosts: master, worker1, worker2.
- Roles involucrados: nvidia_cuda, slurm_facts, slurm_install, slurm_compute,
  slurm_controller, slurm_validate.
- Inventario principal: inventario.ini.

## 2) Flujo operativo de Slurm en el repo (preparacion, instalacion, configuracion)
Resumen del flujo (segun `site.yml`):
1. `nvidia_cuda`: instala driver/stack CUDA y valida `nvidia-smi`.
2. `slurm_identities`: crea usuario/grupo slurm.
3. `slurm_facts`: recolecta facts CPU/MEM y GPU (NVML via `nvidia-smi`).
4. `slurm_rpm_build`: construye RPMS de Slurm.
5. `slurm_install`: instala paquetes y genera `slurm.conf`/`gres.conf`.
6. `slurm_controller`: habilita/inicia `slurmctld` y `slurmdbd`.
7. `slurm_compute`: habilita/inicia `slurmd` y reinicia si cambia config/NVML.
8. `slurm_validate`: validaciones no destructivas (sinfo/srun/sbatch).

Responsabilidades clave:
- `slurm_facts`: deriva `slurm_node_gres` desde NVML.
- `slurm_install`: genera plantillas y replica `slurm.conf` a workers.
- `slurm_compute`: reinicia slurmd cuando cambia GRES o NVML.

## 3) Manejo de variables y plantillas (puntos clave)
Variables principales (definidas en `group_vars/all.yml`):
- `slurm_control_machine`: host del controller (master).
- `slurm_partitions`: particiones CPU/GPU.
- `slurm_mem_reserve_mb`: reserva de RAM para SO.
- puertos y paths: `slurmctld_port`, `slurmd_port`, `slurm_etc_dir`, etc.

Derivacion automatica:
- `slurm_facts` ejecuta `nvidia-smi --query-gpu=name` y genera:
  - `slurm_gpu_names`
  - `slurm_gpu_count`
  - `slurm_gpu_type_nvml` (normalizado a `lower` y `snake_case`)
  - `slurm_node_gres = gpu:<tipo_nvml>:<count>`
- `slurm_install` incluye fallback si `slurm_facts` no corrio.

Plantillas relevantes:
- `roles/slurm_install/templates/gres.conf.j2`:
  - Solo `AutoDetect=nvml` (sin Name/Type manual).
- `roles/slurm_install/templates/slurm.conf.j2`:
  - `GresTypes=gpu`
  - `NodeName=... Gres={{ slurm_node_gres }}` cuando hay GPU.
  - `SelectTypeParameters=CR_Core_Memory` (CR_GPU no soportado en este build).

## 4) Problemas observados y diagnosticos
### 4.1 Sintomas
- Nodos en `DRAIN/INVALID_REG`.
- Mensaje: `Reason=gres/gpu count reported lower than configured (0 < 1)`.
- `sinfo` mostraba `gpu:1(S:0)` sin tipo.
- `slurmd` reportaba fallas NVML / normalizacion de GRES.

### 4.2 Evidencia
Diagnosticos clave (salidas resumidas):
- `slurmd -G` (en master/worker1/worker2):
  - `Type=quadro_p1000 Count=1` (NVML OK una vez corregido).
- `scontrol show node -d`:
  - `Gres=gpu:quadro_p1000:1(S:0)`
  - `GresUsed=gpu:quadro_p1000:0(IDX:N/A)`
- `scontrol show config | egrep 'Gres|SelectType'`:
  - `GresTypes = gpu`
  - `SelectType = select/cons_tres`
  - `SelectTypeParameters = CR_Core_Memory`
- Jobs GPU:
  - `srun -N1 -w worker1 -p gpu --gres=gpu:1 nvidia-smi -L` OK
  - `srun -N1 -w worker2 -p gpu --gres=gpu:1 nvidia-smi -L` OK

Nota sobre el sufijo `(S:0)`:
- El sufijo aparece en `Gres=` y no en `GresUsed=`.
- No se observaron fallos; los jobs GPU funcionan.
- Se intento activar `CR_GPU`, pero el build no lo soporta y se revirtio.

### 4.3 Outputs completos (capturados)
`ansible -i inventario.ini hpc_master -m shell -a "set -euo pipefail; ..."`
```text
master | CHANGED | rc=0 >>
## sinfo -N -h -o %N %t %G
master idle gpu:quadro_p1000:1(S:0)
worker1 idle gpu:quadro_p1000:1(S:0)
worker1 idle gpu:quadro_p1000:1(S:0)
worker2 idle gpu:quadro_p1000:1(S:0)
worker2 idle gpu:quadro_p1000:1(S:0)
## scontrol show node -d
NodeName=master Arch=x86_64 CoresPerSocket=10 
   CPUAlloc=0 CPUEfctv=20 CPUTot=20 CPULoad=0.04
   AvailableFeatures=(null)
   ActiveFeatures=(null)
   Gres=gpu:quadro_p1000:1(S:0)
   GresDrain=N/A
   GresUsed=gpu:quadro_p1000:0(IDX:N/A)
   NodeAddr=master NodeHostName=master Version=23.11.3
   OS=Linux 5.14.0-611.20.1.el9_7.x86_64 #1 SMP PREEMPT_DYNAMIC Thu Jan 15 13:21:39 UTC 2026 
   RealMemory=62715 AllocMem=0 FreeMem=56761 Sockets=1 Boards=1
   State=IDLE ThreadsPerCore=2 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
   Partitions=debug 
   BootTime=2026-01-23T11:37:06 SlurmdStartTime=2026-01-24T11:08:56
   LastBusyTime=2026-01-24T11:08:56 ResumeAfterTime=None
   CfgTRES=cpu=20,mem=62715M,billing=20
   AllocTRES=
   CapWatts=n/a
   CurrentWatts=0 AveWatts=0
   ExtSensorsJoules=n/a ExtSensorsWatts=0 ExtSensorsTemp=n/a

NodeName=worker1 Arch=x86_64 CoresPerSocket=10 
   CPUAlloc=0 CPUEfctv=20 CPUTot=20 CPULoad=0.01
   AvailableFeatures=(null)
   ActiveFeatures=(null)
   Gres=gpu:quadro_p1000:1(S:0)
   GresDrain=N/A
   GresUsed=gpu:quadro_p1000:0(IDX:N/A)
   NodeAddr=worker1 NodeHostName=worker1 Version=23.11.3
   OS=Linux 5.14.0-611.20.1.el9_7.x86_64 #1 SMP PREEMPT_DYNAMIC Thu Jan 15 13:21:39 UTC 2026 
   RealMemory=62715 AllocMem=0 FreeMem=60823 Sockets=1 Boards=1
   State=IDLE ThreadsPerCore=2 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
   Partitions=debug,gpu 
   BootTime=2026-01-23T12:37:22 SlurmdStartTime=2026-01-24T11:35:30
   LastBusyTime=2026-01-24T11:29:05 ResumeAfterTime=None
   CfgTRES=cpu=20,mem=62715M,billing=20
   AllocTRES=
   CapWatts=n/a
   CurrentWatts=0 AveWatts=0
   ExtSensorsJoules=n/a ExtSensorsWatts=0 ExtSensorsTemp=n/a

NodeName=worker2 Arch=x86_64 CoresPerSocket=10 
   CPUAlloc=0 CPUEfctv=20 CPUTot=20 CPULoad=0.00
   AvailableFeatures=(null)
   ActiveFeatures=(null)
   Gres=gpu:quadro_p1000:1(S:0)
   GresDrain=N/A
   GresUsed=gpu:quadro_p1000:0(IDX:N/A)
   NodeAddr=worker2 NodeHostName=worker2 Version=23.11.3
   OS=Linux 5.14.0-611.20.1.el9_7.x86_64 #1 SMP PREEMPT_DYNAMIC Thu Jan 15 13:21:39 UTC 2026 
   RealMemory=62715 AllocMem=0 FreeMem=61448 Sockets=1 Boards=1
   State=IDLE ThreadsPerCore=2 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
   Partitions=debug,gpu 
   BootTime=2026-01-21T17:48:15 SlurmdStartTime=2026-01-24T11:35:30
   LastBusyTime=2026-01-24T11:29:22 ResumeAfterTime=None
   CfgTRES=cpu=20,mem=62715M,billing=20
   AllocTRES=
   CapWatts=n/a
   CurrentWatts=0 AveWatts=0
   ExtSensorsJoules=n/a ExtSensorsWatts=0 ExtSensorsTemp=n/a

## scontrol show node -o
NodeName=master Arch=x86_64 CoresPerSocket=10  CPUAlloc=0 CPUEfctv=20 CPUTot=20 CPULoad=0.04 AvailableFeatures=(null) ActiveFeatures=(null) Gres=gpu:quadro_p1000:1(S:0) NodeAddr=master NodeHostName=master Version=23.11.3 OS=Linux 5.14.0-611.20.1.el9_7.x86_64 #1 SMP PREEMPT_DYNAMIC Thu Jan 15 13:21:39 UTC 2026  RealMemory=62715 AllocMem=0 FreeMem=56761 Sockets=1 Boards=1 State=IDLE ThreadsPerCore=2 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A Partitions=debug  BootTime=2026-01-23T11:37:06 SlurmdStartTime=2026-01-24T11:08:56 LastBusyTime=2026-01-24T11:08:56 ResumeAfterTime=None CfgTRES=cpu=20,mem=62715M,billing=20 AllocTRES= CapWatts=n/a CurrentWatts=0 AveWatts=0 ExtSensorsJoules=n/a ExtSensorsWatts=0 ExtSensorsTemp=n/a
NodeName=worker1 Arch=x86_64 CoresPerSocket=10  CPUAlloc=0 CPUEfctv=20 CPUTot=20 CPULoad=0.01 AvailableFeatures=(null) ActiveFeatures=(null) Gres=gpu:quadro_p1000:1(S:0) NodeAddr=worker1 NodeHostName=worker1 Version=23.11.3 OS=Linux 5.14.0-611.20.1.el9_7.x86_64 #1 SMP PREEMPT_DYNAMIC Thu Jan 15 13:21:39 UTC 2026  RealMemory=62715 AllocMem=0 FreeMem=60823 Sockets=1 Boards=1 State=IDLE ThreadsPerCore=2 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A Partitions=debug,gpu  BootTime=2026-01-23T12:37:22 SlurmdStartTime=2026-01-24T11:35:30 LastBusyTime=2026-01-24T11:29:05 ResumeAfterTime=None CfgTRES=cpu=20,mem=62715M,billing=20 AllocTRES= CapWatts=n/a CurrentWatts=0 AveWatts=0 ExtSensorsJoules=n/a ExtSensorsWatts=0 ExtSensorsTemp=n/a
NodeName=worker2 Arch=x86_64 CoresPerSocket=10  CPUAlloc=0 CPUEfctv=20 CPUTot=20 CPULoad=0.00 AvailableFeatures=(null) ActiveFeatures=(null) Gres=gpu:quadro_p1000:1(S:0) NodeAddr=worker2 NodeHostName=worker2 Version=23.11.3 OS=Linux 5.14.0-611.20.1.el9_7.x86_64 #1 SMP PREEMPT_DYNAMIC Thu Jan 15 13:21:39 UTC 2026  RealMemory=62715 AllocMem=0 FreeMem=61448 Sockets=1 Boards=1 State=IDLE ThreadsPerCore=2 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A Partitions=debug,gpu  BootTime=2026-01-21T17:48:15 SlurmdStartTime=2026-01-24T11:35:30 LastBusyTime=2026-01-24T11:29:22 ResumeAfterTime=None CfgTRES=cpu=20,mem=62715M,billing=20 AllocTRES= CapWatts=n/a CurrentWatts=0 AveWatts=0 ExtSensorsJoules=n/a ExtSensorsWatts=0 ExtSensorsTemp=n/a
## scontrol show config (Gres|SelectType)
GresTypes               = gpu
SelectType              = select/cons_tres
SelectTypeParameters    = CR_CORE_MEMORY
```

`ansible -i inventario.ini slurm_all -m shell -a "set -euo pipefail; ... sudo -n slurmd -G"`
```text
worker1 | CHANGED | rc=0 >>
## host: masterslurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
slurmd: Gres Name=gpu Type=quadro_p1000 Count=1 Index=0 ID=7696487 File=/dev/nvidia0 Cores=0-9 CoreCnt=20 Links=-1 Flags=HAS_FILE,HAS_TYPE,ENV_NVML
worker2 | CHANGED | rc=0 >>
## host: masterslurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
slurmd: Gres Name=gpu Type=quadro_p1000 Count=1 Index=0 ID=7696487 File=/dev/nvidia0 Cores=0-9 CoreCnt=20 Links=-1 Flags=HAS_FILE,HAS_TYPE,ENV_NVML
master | CHANGED | rc=0 >>
## host: masterslurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
slurmd: Gres Name=gpu Type=quadro_p1000 Count=1 Index=0 ID=7696487 File=/dev/nvidia0 Cores=0-9 CoreCnt=20 Links=-1 Flags=HAS_FILE,HAS_TYPE,ENV_NVML
```

`ansible -i inventario.ini hpc_master -m shell -a "set -euo pipefail; srun ... nvidia-smi -L"`
```text
master | CHANGED | rc=0 >>
## srun worker1 nvidia-smi -L
GPU 0: Quadro P1000 (UUID: GPU-8507f1ec-9a14-d72f-d41b-513b9a8790cf)
## srun worker2 nvidia-smi -L
GPU 0: Quadro P1000 (UUID: GPU-d9ef07cd-20d1-1c99-fda1-c80d6c1d8702)
```

## 5) Causas raiz
1. **NVML no disponible para Slurm**:
   - Faltaba el symlink `libnvidia-ml.so` (existe `libnvidia-ml.so.1`).
2. **slurmd no reiniciado tras reparar NVML**:
   - Sin reinicio, Slurm mantiene datos viejos y sigue marcando mismatch.
3. **GRES en slurm.conf sin tipo NVML**:
   - `Gres=gpu:1` no coincidia con el tipo detectado por NVML.
4. **Intento de CR_GPU no soportado**:
   - `SelectTypeParameters=CR_Core_Memory,CR_GPU` fallo con "Bad SelectTypeParameter".

## 6) Soluciones aplicadas (cambios Ansible)
### 6.1 `roles/nvidia_cuda/tasks/main.yml`
Objetivo: garantizar NVML disponible para Slurm.
- Buscar `libnvidia-ml.so.1` en rutas comunes.
- Crear symlink `libnvidia-ml.so` (force true).
- Si se creo symlink, ejecutar `ldconfig`.
- Marcar `slurm_nvml_symlink_changed` para reinicio de slurmd.

### 6.2 `roles/slurm_facts/tasks/main.yml`
Objetivo: derivar GRES desde NVML.
- `nvidia-smi --query-gpu=name` => `slurm_gpu_names`, `slurm_gpu_count`.
- Normalizar `slurm_gpu_type_nvml` a lowercase y snake_case.
- Definir `slurm_node_gres = gpu:<tipo_nvml>:<count>`.
- Advertir si hay GPUs mixtas.

### 6.3 `roles/slurm_install/tasks/main.yml`
Objetivo: fallback si no hay facts.
- Si faltan `slurm_gpu_count`/`slurm_gpu_type_short`, recalcula con `nvidia-smi`.
- Repite normalizacion y define `slurm_node_gres`.

### 6.4 `roles/slurm_install/templates/gres.conf.j2`
Objetivo: usar AutoDetect sin datos manuales.
- Solo `AutoDetect=nvml`.

### 6.5 `roles/slurm_install/templates/slurm.conf.j2`
Objetivo: reflejar GRES real por nodo.
- `Gres={{ slurm_node_gres }}` por nodo.
- Se intento agregar `CR_GPU` pero se revirtio por incompatibilidad.

### 6.6 `roles/slurm_compute/tasks/main.yml`
Objetivo: aplicar cambios de GRES/NVML.
- Reinicia `slurmd` si cambia `slurm.conf`, `gres.conf` o NVML symlink.
- Verifica que `slurmd` quede `active`.

## 7) Estado actual
- `slurmd -G` muestra `Type=quadro_p1000 Count=1` en master/worker1/worker2.
- `sinfo` muestra `gpu:quadro_p1000:1(S:0)` y los nodos estan `IDLE`.
- Jobs GPU corren correctamente en particion `gpu`.
- El sufijo `(S:0)` persiste pero no afecta la ejecucion.

## 8) Registro detallado de comandos utilizados
Listado por fuente y orden aproximado (solo comandos realmente usados):

### 8.1 Comandos ejecutados por Codex en esta sesion
- `ls docs`
- `git status --short`
- `rg -n "slurm|slurmd|slurmctld|gres|nvml|nvidia|AutoDetect" roles group_vars host_vars site.yml base.yml inventario.ini inventario_glob.ini playbooks* llm-project*`
- `rg -n "nvml|libnvidia" roles/nvidia_cuda/tasks/main.yml`
- `sed -n '600,690p' roles/nvidia_cuda/tasks/main.yml`
- `sed -n '1,140p' roles/slurm_facts/tasks/main.yml`
- `sed -n '200,380p' roles/slurm_install/tasks/main.yml`
- `sed -n '1,260p' roles/slurm_install/templates/slurm.conf.j2`
- `sed -n '1,120p' roles/slurm_install/templates/gres.conf.j2`
- `sed -n '1,140p' roles/slurm_compute/tasks/main.yml`
- `rg -n "slurm|scontrol|sinfo|slurmd|nvidia-smi|ansible-playbook|ansible -i" docs/codex-log.md`
- `git log --oneline -n 5`
- `ansible -i inventario.ini hpc_master -m shell -a "set -euo pipefail; scontrol show node -d | egrep 'NodeName=|Gres=|GresUsed='"`
- `ansible -i inventario.ini hpc_master -m shell -a "set -euo pipefail; scontrol show node -o"`
- `ansible -i inventario.ini hpc_master -m shell -a "set -euo pipefail; scontrol show config | egrep 'Gres|SelectType'"`

### 8.2 Comandos reportados en la bitacora del proceso Slurm+NVML
(ejecutados durante la resolucion y documentados en `docs/bitacora_codex.md`)
- `slurmd -G`
- `sinfo -N -h -o "%N %t %G"`
- `srun -N1 -w worker1 -p gpu --gres=gpu:1 nvidia-smi -L`
- `srun -N1 -w worker2 -p gpu --gres=gpu:1 nvidia-smi -L`
- `scontrol reconfigure`
- `scontrol update NodeName=<node> State=resume` (usuario)

## 9) Cambios en archivos Ansible (detalle)
Archivos modificados para soportar NVML y AutoDetect:
- `roles/nvidia_cuda/tasks/main.yml`
  - Agregado manejo de symlink NVML y `ldconfig`.
  - Nuevo flag `slurm_nvml_symlink_changed`.
- `roles/slurm_facts/tasks/main.yml`
  - Normalizacion `slurm_gpu_type_nvml`.
  - GRES basado en NVML (`slurm_node_gres`).
- `roles/slurm_install/tasks/main.yml`
  - Fallback de NVML si faltan facts.
- `roles/slurm_install/templates/gres.conf.j2`
  - Solo `AutoDetect=nvml`.
- `roles/slurm_compute/tasks/main.yml`
  - Reinicio `slurmd` al cambiar NVML/configs.

Commits relacionados (segun `git log --oneline -n 5`):
- `7c84976 Fix NVML AutoDetect GRES integration`
- `9810da5 AutoDetect nvml not using GPU references Slurm not working`
- `e8c4b22 AutoDetect nvml (not working)`

## 10) Riesgos residuales y recomendaciones
- El sufijo `(S:0)` persiste; no bloquea jobs.
- No usar `CR_GPU` en este build por incompatibilidad.
- Mantener `gres.conf` solo con `AutoDetect=nvml`.
- Si reaparece DRAIN/INVALID_REG:
  1) Verificar `libnvidia-ml.so` y ejecutar `ldconfig`.
  2) Reiniciar `slurmd`.
  3) `scontrol reconfigure` y validar `slurmd -G`.
