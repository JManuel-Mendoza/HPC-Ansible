# Manual facts — Servicios detallados

## 0) Contexto mínimo del despliegue
- Playbook de entrada principal: `site.yml` (ruta: `site.yml`).
- Inventario activo por `ansible.cfg`: `inventario.ini` (`inventory = inventario.ini`).
- Grupos principales en `inventario.ini`: `hpc_master`, `workers_r`, `workers_u`, `workers`, `slurm_all`, `slurm_compute`, `slurm_gpu`.
- Estado visible del inventario actual (hosts no comentados): `master` y `worker2`.
- Orden general de ejecución: `site.yml` define 15 plays secuenciales (no usa `import_playbook`), desde baseline/red hasta validaciones finales.

---

## 1) Servicio: Red
### 1.1 Roles implicados
- `network_internal` (`roles/network_internal`)  
- `cluster_routing` (`roles/cluster_routing`)  
- `firewall` (`roles/firewall`)

### 1.2 Plays en site.yml relacionados
- `site.yml` — **Etapa 2 | Red interna + ruteo + firewall** (hosts: `all`; roles: `network_internal`, `cluster_routing`, `firewall`).
- Relacionado a verificación de conectividad/firewall de Slurm: `site.yml` **Etapa 14** (`validate`) y **Etapa 15** (`slurm_validate`).

### 1.3 Variables y parámetros críticos
| variable | dónde vive | propósito | ejemplo no sensible |
|---|---|---|---|
| `network_internal_keep_if` | `group_vars/all/vars.yml` (override de `roles/network_internal/defaults/main.yml`) | Interfaz que no se debe tocar al limpiar conexiones NM | `eno1` |
| `network_internal_exclude_ifaces` | `group_vars/all/vars.yml` | Exclusión de interfaces al limpiar conexiones | `['tailscale0']` |
| `network_internal_exclude_conn_regex` | `group_vars/all/vars.yml` | Exclusión por regex de nombres de conexión NM | `.*tailscale.*` |
| `network_internal_links` | `group_vars/all/vars.yml` | Topología master-worker (if/ip por extremo) | `worker2.master_ip: 192.168.34.17/28` |
| `hpc_router_internal_ifaces` | `group_vars/hpc_master.yml` | NICs internas del master para zona trusted | `['enp3s0f1', ...]` |
| `hpc_internal_supernet` | `group_vars/all/vars.yml` | Superred interna para confianza firewall en workers | `192.168.34.0/24` |
| `hpc_internal_subnets` | `group_vars/all/vars.yml` | Subredes /28 para cálculo de rutas persistentes | `192.168.34.16/28` |
| `slurm_firewalld_zone` | `group_vars/all/vars.yml` | Zona firewalld para reglas Slurm | `public` |
| `slurm_internal_cidr` | `group_vars/all/vars.yml` | CIDR origen permitido para puertos Slurm | `192.168.34.0/24` |
| `slurmctld_port`, `slurmd_port` | `group_vars/all/vars.yml` | Puertos de control/daemon usados también en firewall | `6817`, `6818` |

Fragmento útil (gating de topología obligatoria):
```yaml
- name: Red Interna | Assert variables definidas
  ansible.builtin.assert:
    that:
      - network_internal_links is defined
      - network_internal_links is mapping
      - network_internal_links | length > 0
      - network_internal_keep_if is defined
      - network_internal_keep_if | length > 0
```

### 1.4 Archivos y templates relevantes
- `roles/network_internal/defaults/main.yml`
- `roles/network_internal/tasks/main.yml`
- `roles/network_internal/tasks/master_link.yml`
- `roles/cluster_routing/tasks/main.yml`
- `roles/firewall/tasks/main.yml`
- `roles/firewall/handlers/main.yml`
- Templates de red dedicados: **no se encontraron** en estos roles.
- Mecanismo de red detectado:
  - `nmcli` vía `ansible.builtin.command` / `ansible.builtin.shell` (NetworkManager).
  - `ansible.posix.sysctl` para `net.ipv4.ip_forward`.
  - `ansible.posix.firewalld` y `firewall-cmd` para reglas.

### 1.5 Reglas de firewall asociadas (si aplica en fase red)
- SSH habilitado (`service: ssh`) en `roles/firewall/tasks/main.yml`.
- Regla rica `6817/tcp` (slurmctld) desde `slurm_internal_cidr` en master (`hpc_master`) en `roles/firewall/tasks/main.yml`.
- Regla rica `6818/tcp` (slurmd) desde `slurm_internal_cidr` en `workers_r + workers` en `roles/firewall/tasks/main.yml`.
- Zona `trusted` para interfaces internas del master (`hpc_router_internal_ifaces`) y para `source: hpc_internal_supernet` en workers en `roles/cluster_routing/tasks/main.yml`.

### 1.6 Criterios de verificación existentes en repo
- `roles/network_internal/tasks/main.yml`: consulta de estado activo con `nmcli -t -f NAME,DEVICE,TYPE,STATE ...` y salida `debug` de conexiones `int-*`.
- `roles/cluster_routing/tasks/main.yml`: lectura de rutas actuales NM (`nmcli -g ipv4.routes ...`) y comparación con rutas deseadas.
- Validación dedicada de red tipo `ping/ip a/nmcli assert` en rol `validate`: **no encontrada**.
- Validación indirecta de conectividad de puertos Slurm (`wait_for`) en `roles/validate/tasks/slurm.yml`.

---

## 2) Servicio: GPU (drivers / CUDA / NVML)
### 2.1 Roles implicados
- Primario de instalación/driver: `nvidia_cuda` (`roles/nvidia_cuda`).
- Consumo posterior de facts GPU/NVML para Slurm: `slurm_facts` (`roles/slurm_facts`), `slurm_install` (`roles/slurm_install`), `slurm_compute` (`roles/slurm_compute`).
- Verificación: `validate` (`roles/validate`) y `slurm_validate` (`roles/slurm_validate`).

### 2.2 Plays en site.yml relacionados
- `site.yml` — **Etapa 3 | CUDA/Driver NVIDIA (solo nodos con GPU)**.
- Relacionados en fases posteriores:
  - **Etapa 10** (`slurm_facts`) usa `nvidia-smi` para GRES/facts.
  - **Etapa 11/12** (`slurm_install`) genera `gres.conf` y fallback GPU.
  - **Etapa 14** (`validate`) valida `nvidia-smi` y opcional Torch.
  - **Etapa 15** (`slurm_validate`) ejecuta `srun ... nvidia-smi -L` y smoke GPU.

### 2.3 Variables críticas (driver version, cuda version, flags)
| variable | dónde vive | propósito | ejemplo no sensible |
|---|---|---|---|
| `nvidia_driver_stream` | `roles/nvidia_cuda/defaults/main.yml` | Stream objetivo de driver | `580-dkms` |
| `nvidia_cuda_reboot` | `roles/nvidia_cuda/defaults/main.yml` | Permite reboot automático si cambios lo requieren | `false` |
| `nvidia_cuda_repo_enabled` | `roles/nvidia_cuda/defaults/main.yml` | Activa repo CUDA oficial | `true` |
| `nvidia_cuda_validate` | `roles/nvidia_cuda/defaults/main.yml` | Activa validaciones posinstalación | `true` |
| `nvidia_cuda_hold_drivers` | `roles/nvidia_cuda/defaults/main.yml` | Activa congelación de paquetes NVIDIA tras instalación/validación | `true` |
| `nvidia_cuda_hold_package_regex_redhat` | `roles/nvidia_cuda/defaults/main.yml` | Regex para descubrir RPMs NVIDIA a congelar con versionlock | `^(nvidia|kmod-nvidia|dkms-nvidia)` |
| `nvidia_cuda_hold_package_regex_debian` | `roles/nvidia_cuda/defaults/main.yml` | Regex para descubrir paquetes Debian a poner en hold | `^(nvidia|libnvidia|cuda-drivers)` |
| `nvidia_cuda_versionlock_plugin_package` | `roles/nvidia_cuda/defaults/main.yml` | Plugin DNF requerido para `versionlock` en RHEL | `python3-dnf-plugin-versionlock` |
| `nvidia_cuda_versionlock_file` | `roles/nvidia_cuda/defaults/main.yml` | Archivo persistente de locks DNF | `/etc/dnf/plugins/versionlock.list` |
| `nvidia_cuda_repo_url` | `roles/nvidia_cuda/defaults/main.yml` | URL repo CUDA RHEL | `.../cuda-rhel9.repo` |
| `slurm_node_gres` | derivada en `roles/slurm_facts/tasks/main.yml` o override en `host_vars/group_vars` | GRES por nodo (GPU scheduling) | `gpu:quadro_p1000:1` (ejemplo comentado) |
| `slurm_validate_torch.*` | `group_vars/all/vars.yml` | Política de test Torch en etapa `slurm_validate` | `enabled: auto` |

### 2.4 Archivos/templates relevantes
- `roles/nvidia_cuda/defaults/main.yml`
- `roles/nvidia_cuda/tasks/main.yml`
- `roles/nvidia_cuda/handlers/main.yml`
- `roles/slurm_facts/tasks/main.yml` (detección GPU para GRES)
- `roles/slurm_install/templates/gres.conf.j2`

### 2.5 Detección de GPU y gating
Fragmento útil (detección + corte de host sin GPU):
```yaml
- name: NVIDIA/CUDA | Detectar GPU NVIDIA
  ansible.builtin.command: "lspci -nn -d 10de:"
  register: _nvidia_lspci
  changed_when: false
  failed_when: false

- name: NVIDIA/CUDA | Saltar host sin GPU
  ansible.builtin.meta: end_host
  when: not _nvidia_gpu_present
```

Fragmento útil (gating de reboot obligatorio):
```yaml
- name: NVIDIA/CUDA | Fallar si requiere reinicio y esta deshabilitado
  ansible.builtin.fail:
    msg: >-
      Se requieren cambios ... pero nvidia_cuda_reboot=false.
  when:
    - _nvidia_reboot_required | bool
    - not nvidia_cuda_reboot | bool
```

### 2.6 Validaciones (nvidia-smi, nvcc, modules, etc.)
- `roles/nvidia_cuda/tasks/main.yml` valida:
  - `lsmod` (falla si `nouveau` sigue cargado o faltan módulos `nvidia`).
  - existencia/ejecución de `nvidia-smi`.
  - nodos `/dev/nvidia*`.
  - normalización NVML (`libnvidia-ml.so` symlink) + `ldconfig`.
  - disponibilidad del plugin `dnf versionlock` si `nvidia_cuda_hold_drivers=true` en RHEL.
- `roles/validate/tasks/main.yml`:
  - `stat /usr/bin/nvidia-smi`, `nvidia-smi -L`, asserts según pertenencia `slurm_gpu`.
  - check Torch CUDA opcional (`validate_llm`, por defecto `false`).
- `roles/slurm_validate/tasks/main.yml`:
  - `srun ... --gres=gpu:1 nvidia-smi -L`.
  - smoke GPU con `sbatch` y `sacct` (`COMPLETED|0:0`).
- Validación explícita de `nvcc` en el repo: **no encontrada**.

### 2.7 Freeze / versionlock de drivers
- `roles/nvidia_cuda/tasks/main.yml` aplica la congelación **después** de instalar/validar el driver:
  - RHEL/Rocky:
    - instala `python3-dnf-plugin-versionlock`,
    - comprueba `dnf -q versionlock list`,
    - obtiene RPMs instalados con regex `nvidia_cuda_hold_package_regex_redhat`,
    - escribe las NEVRAs resultantes en `nvidia_cuda_versionlock_file`.
  - Debian/Ubuntu:
    - obtiene paquetes instalados con regex `nvidia_cuda_hold_package_regex_debian`,
    - aplica `dpkg_selections: selection=hold`.
- Remoción automatizada de locks/holds en el rol: **no encontrada**.

---

## 3) Servicio: NFS
### 3.1 Roles implicados (server/client separados si existen)
- Rol único con comportamiento por flags server/client: `nfs_hpc` (`roles/nfs_hpc`).
- No hay roles separados `nfs_server`/`nfs_client`.

### 3.2 Plays en site.yml relacionados
- `site.yml` — **Etapa 4 | NFS HPC (server export)** (`hosts: hpc_master`).
- `site.yml` — **Etapa 5 | NFS HPC (clientes mount)** (`hosts: all:!hpc_master`).

### 3.3 Variables críticas (export path, mountpoint, options, network allowlist)
| variable | dónde vive | propósito | ejemplo no sensible |
|---|---|---|---|
| `nfs_export_path` | `group_vars/all/vars.yml` | Directorio exportado por master | `/srv/nfs/llm` |
| `nfs_client_mountpoint` | `group_vars/all/vars.yml` | Punto de montaje cliente | `/mnt/llm` |
| `nfs_server_ip` | `group_vars/all/vars.yml` | IP NFS resuelta por `network_internal_links` | `192.168.34.17` |
| `nfs_hpc_server_enabled` | `group_vars/hpc_master.yml` (override de defaults) | Habilita modo server en master | `true` |
| `nfs_hpc_client_enabled` | `roles/nfs_hpc/defaults/main.yml` | Habilita modo cliente por defecto | `true` |
| `nfs_hpc_allowed_clients` | `roles/nfs_hpc/defaults/main.yml` (usa `slurm_internal_cidr`) | allowlist de export | `192.168.34.0/24` |
| `nfs_hpc_export_opts` | `roles/nfs_hpc/defaults/main.yml` | opciones de export NFS | `rw,sync,no_subtree_check` |
| `nfs_hpc_mount_opts` | `roles/nfs_hpc/defaults/main.yml` | opciones de mount cliente | `rw,relatime,vers=4.2,_netdev` |

Fragmento útil (bifurcación server/client):
```yaml
- name: NFS | Instalar paquetes del servidor
  ansible.builtin.package:
    name: "{{ nfs_hpc_server_packages.get(...) }}"
  when: nfs_hpc_server_enabled | bool

- name: NFS | Instalar paquetes del cliente
  ansible.builtin.package:
    name: "{{ nfs_hpc_client_packages.get(...) }}"
  when:
    - nfs_hpc_client_enabled | bool
    - not (nfs_hpc_server_enabled | bool)
```

### 3.4 Archivos/templates relevantes (exports, fstab, systemd mounts)
- `roles/nfs_hpc/defaults/main.yml`
- `roles/nfs_hpc/tasks/main.yml`
- `roles/nfs_hpc/handlers/main.yml`
- `roles/nfs_hpc/templates/exports.j2` (genera `nfs_hpc_export_file`, por defecto `/etc/exports.d/hpc-nfs.exports`)
- Gestión de montaje persistente: `ansible.builtin.mount state: mounted` (actualiza montaje y `fstab`).
- Unidades systemd `.mount` dedicadas: **no encontradas**.

### 3.5 Firewall asociado (rpcbind/2049/etc.) y dónde se define
- En `roles/nfs_hpc/tasks/main.yml`:
  - consulta y apertura de `2049/tcp` vía `firewall-cmd --permanent ...`.
  - handler `NFS | Recargar firewalld` en `roles/nfs_hpc/handlers/main.yml`.
- Reglas explícitas para `rpcbind`/`mountd`/`111` en este rol: **no encontradas**.

### 3.6 Validaciones (mount, write test) existentes en repo
- Validación local incluida en rol:
  - `mountpoint -q {{ nfs_hpc_mount_point }}` antes de crear/montar.
- Validación separada en `roles/validate` para NFS: **no encontrada**.
- Prueba de escritura/read-back NFS en repo: **no encontrada**.

---

## 4) Servicio: Slurm (incluye Munge/DB si aplica)
### 4.1 Roles implicados (munge, mariadb, slurmctld, slurmd, slurmdbd, facts, validate, etc.)
- `mariadb_server` (`roles/mariadb_server`) — etapa DB base.
- `slurm_db_prep` (`roles/slurm_db_prep`) — DB/usuarios/permisos Slurm accounting.
- `slurm_identities` (`roles/slurm_identities`) — usuarios/grupos `munge` y `slurm`.
- `munge` (`roles/munge`) — clave compartida y servicio.
- `slurm_facts` (`roles/slurm_facts`) — facts HW/GPU para templates.
- `slurm_rpm_build` (`roles/slurm_rpm_build`) — build RPM Slurm (RHEL).
- `slurm_install` (`roles/slurm_install`) — instalación paquetes, `slurm.conf`, `gres.conf`, firewall srun range, higiene `slurmdbd`.
- `slurm_controller` (`roles/slurm_controller`) — `slurmdbd`, `slurmctld`, `scontrol reconfigure`, autoresume.
- `slurm_compute` (`roles/slurm_compute`) — `slurmd` en nodos compute.
- `validate` (`roles/validate/tasks/slurm.yml`) — checks de puertos/conectividad/firewall.
- `slurm_validate` (`roles/slurm_validate`) — validación read-only y smoke jobs.

### 4.2 Plays en site.yml relacionados (orden)
1. `Etapa 6 | MariaDB en master` (`mariadb_server`)  
2. `Etapa 7 | Preparar SlurmDB en MariaDB` (`slurm_db_prep`)  
3. `Etapa 8 | Configuración de identidades SLURM` (`slurm_identities`)  
4. `Etapa 9 | Configuración de Munge` (`munge`)  
5. `Etapa 10 | Recopilación de hechos SLURM` (`slurm_facts`)  
6. `Etapa 11 | Configuración de SLURM en nodo master` (`slurm_rpm_build`, `slurm_install`, `slurm_controller`)  
7. `Etapa 12 | Configuración de SLURM en nodos compute` (`slurm_install`, `slurm_compute`)  
8. `Etapa 14 | Validación general` (`validate`, incluye `validate_slurm`)  
9. `Etapa 15 | Validación Slurm` (`slurm_validate`)  

### 4.3 Variables críticas
| variable | dónde vive | propósito | ejemplo no sensible |
|---|---|---|---|
| `munge_uid`, `munge_gid`, `slurm_uid`, `slurm_gid` | `group_vars/all/vars.yml` | IDs de cuentas de servicio | `1011`, `1012` |
| `munge_key_host`, `munge_key_size_mb` | `group_vars/all/vars.yml` | nodo fuente de key y tamaño | `master`, `4` |
| `slurm_version`, `slurm_tarball_url` | `group_vars/all/vars.yml` | versión/build source | `23.11.3` |
| `slurm_etc_dir`, `slurm_log_dir` | `group_vars/all/vars.yml` | rutas de configuración/logs | `/etc/slurm`, `/var/log/slurm` |
| `slurm_control_machine` | `group_vars/all/vars.yml` | controlador en `slurm.conf` | `master` |
| `slurm_partitions` | `group_vars/all/vars.yml` | definición declarativa de particiones | `debug`, `gpu` |
| `slurm_srun_port_range` | `group_vars/all/vars.yml` | rango TCP retorno srun | `60001-60100` |
| `slurm_cgroup_conf` | `group_vars/all/vars.yml` | contenido `cgroup.conf` | `ConstrainDevices=yes` |
| `slurmdb_mysql_db`, `slurmdb_mysql_user`, `slurmdb_mysql_hosts` | `group_vars/hpc_master.yml` | DB y grants de accounting | `slurm_acct_db`, `slurm`, `localhost/master` |
| `slurmdb_mysql_password` | `group_vars/hpc_master.yml` | password DB Slurm | **sensible (definido en claro en repo)** |
| `slurmdbd_port`, `slurmdbd_host`, `slurmdbd_storage_*` | `group_vars/hpc_master.yml` | parámetros `slurmdbd.conf` | `6819`, `localhost` |
| `slurm_controller_reconfigure_*`, `slurm_controller_autoresume_*` | `roles/slurm_controller/defaults/main.yml` | política reconfigure/autoresume | `true`, estados `DRAIN/INVALID_REG` |
| `slurm_node_gres`, `slurm_cpus`, `slurm_real_memory` | facts en `slurm_facts` + posibles overrides host/group | recursos por nodo para `slurm.conf` | `gpu:...:1` |

### 4.4 Archivos/templates relevantes
- **slurm.conf template**: `roles/slurm_install/templates/slurm.conf.j2`.
- **slurmdbd.conf template**: `roles/slurm_controller/templates/slurmdbd.conf.j2`.
- Archivo legacy en repo: `roles/slurm_install/files/slurm.conf` (no referenciado por tasks actuales).
- **Munge key management**:
  - generación en key host (`/etc/munge/munge.key`) en `roles/munge/tasks/main.yml` (`creates:`).
  - `slurp` delegado al key host y distribución por `copy` a todos los nodos.
- **systemd/service management**:
  - `roles/munge/tasks/main.yml` (servicio `munge`).
  - `roles/slurm_controller/tasks/main.yml` (`slurmdbd`, `slurmctld`).
  - `roles/slurm_compute/tasks/main.yml` (`slurmd`).
  - `roles/slurm_install/handlers/main.yml` (reinicios y `daemon_reload`).

### 4.5 Puertos y firewall
| servicio | puerto | nodo | dónde se abre |
|---|---|---|---|
| `slurmctld` | `6817/tcp` | `hpc_master` | `roles/firewall/tasks/main.yml` (rich rule desde `slurm_internal_cidr`) |
| `slurmd` | `6818/tcp` | `workers_r + workers` | `roles/firewall/tasks/main.yml` (rich rule desde `slurm_internal_cidr`) |
| `srun` return range | `60001-60100/tcp` (default) | `hpc_master` | `roles/slurm_install/tasks/main.yml` (`firewall-cmd --add-port={{ slurm_srun_port_range }}/tcp`) |
| `slurmdbd` | `6819/tcp` | `hpc_master` | Regla explícita firewalld en roles: **no encontrada** |

### 4.6 Generación de configuración basada en facts
- `roles/slurm_facts/tasks/main.yml` calcula `slurm_cpus`, `slurm_real_memory`, `slurm_gpu_count`, `slurm_node_gres` por host.
- `roles/slurm_install/templates/slurm.conf.j2` consume `hostvars[*].slurm_*` para construir `NodeName=...` y usa `slurm_partitions` para `PartitionName=...`.
- `roles/slurm_install/tasks/main.yml` contiene fallback de facts GPU (`nvidia-smi`) si faltan facts previos.

Fragmento útil (render dinámico por host):
```jinja
{% for h in (_slurm_host_list | sort) -%}
{% set hn = hostvars[h].get('slurm_node_name', h) -%}
{% set cpus = hostvars[h].get('slurm_cpus', 1) -%}
{% set mem = hostvars[h].get('slurm_real_memory', 1024) -%}
{% set gres = hostvars[h].get('slurm_node_gres', '') -%}
NodeName={{ hn }} CPUs={{ cpus }} ... RealMemory={{ mem }}{% if gres %} Gres={{ gres }}{% endif %} State=UNKNOWN
{% endfor -%}
```

### 4.7 Validaciones
- `roles/munge/tasks/main.yml`: `munge -n | unmunge | grep -q STATUS`.
- `roles/validate/tasks/slurm.yml`:
  - escucha de puertos (`ss -lntp`) en master/worker.
  - conectividad (`wait_for`) workers→controller `6817` y master→workers `6818`.
  - checks firewalld (`--list-rich-rules`, `--query-port` srun range).
- `roles/slurm_validate/tasks/main.yml` (read-only + smoke):
  - `sinfo`, validación particiones, estado de nodos.
  - `srun hostname` (CPU) y `srun nvidia-smi -L` (GPU).
  - `sbatch` smoke CPU/GPU + `sacct` assert `COMPLETED|0:0`.

---

## 5) Servicio: Entorno LLM
### 5.1 Roles implicados
- `llm_env` (`roles/llm_env`).
- Rol `llm_project`: **no existe en `roles/` en este repositorio**.

### 5.2 Plays en site.yml relacionados
- `site.yml` — **Etapa 13 | Entorno LLM (micromamba + torch)** (hosts: `all`, rol `llm_env`).
- Validaciones relacionadas en otras etapas:
  - `Etapa 14` (`validate`) si `validate_llm=true`.
  - `Etapa 15` (`slurm_validate`) con `slurm_validate_torch`.

### 5.3 Variables críticas (micromamba/conda env path, env name, packages, repos de proyecto)
| variable | dónde vive | propósito | ejemplo no sensible |
|---|---|---|---|
| `llm_micromamba_root` | `roles/llm_env/defaults/main.yml` (también `roles/validate/defaults/main.yml`) | raíz de micromamba | `/opt/micromamba` |
| `llm_micromamba_bin` | `roles/llm_env/defaults/main.yml` | binario micromamba | `/opt/micromamba/bin/micromamba` |
| `llm_env_name` | `roles/llm_env/defaults/main.yml` | nombre de entorno | `llm` |
| `llm_pytorch_python_version` | `roles/llm_env/defaults/main.yml` | versión Python para stack PyTorch CUDA | `3.11` |
| `llm_conda_channels` | `roles/llm_env/defaults/main.yml` | canales conda usados | `pytorch,nvidia,conda-forge` |
| `llm_conda_packages` | `group_vars/all/vars.yml` | paquetes conda base | `python,pytorch,pytorch-cuda,...` |
| `llm_pip_packages` | `group_vars/all/vars.yml` | paquetes pip dentro del env | `transformers,datasets,...` |
| `slurm_validate_torch.prelude` | `group_vars/all/vars.yml` | activación del env en validación Slurm | `micromamba activate llm` |

### 5.4 Archivos/templates relevantes
- `roles/llm_env/defaults/main.yml`
- `roles/llm_env/tasks/main.yml`
- Plantillas del rol `llm_env`: **no encontradas**.
- Artefactos que crea el rol:
  - `/etc/profile.d/micromamba.sh`
  - `{{ llm_micromamba_root }}/bin/llm-env-check`

Fragmento útil (protección contra mezcla pip/conda para torch):
```yaml
- name: LLM Env | Fail if pip packages include torch
  ansible.builtin.fail:
    msg: >-
      llm_pip_packages incluye torch. Esto puede sobrescribir el torch conda.
  when: llm_pip_packages | select('match', '^torch($|[=<>])') | list | length > 0
```

### 5.5 Validaciones (import checks, versions) existentes en repo
- En `roles/llm_env/tasks/main.yml`:
  - detecta installer de `torch` y falla si viene de `pip`.
  - ejecuta `python -c` con `torch.__version__`, `torch.version.cuda`, `torch.cuda.is_available()`.
  - falla solo en nodos con GPU NVIDIA (`lspci -nn -d 10de:`) si CUDA no está disponible.
- En `roles/validate/tasks/main.yml`:
  - check opcional `validate_llm` (por defecto `false`) para Torch CUDA en env micromamba.
- En `roles/slurm_validate/tasks/main.yml`:
  - sonda y smoke de importación Torch sobre `srun` en partición GPU.

---

## 6) Mapa de dependencias (resumen)
| Macrofase | depende de | resultado observable | rol(es) |
|---|---|---|---|
| Red | inventario + `network_internal_links` + facts de interfaces | conexiones `int-*` activas, rutas persistentes, reglas base firewall/trusted | `network_internal`, `cluster_routing`, `firewall` |
| Drivers y aceleración GPU | red funcional + repos SO + hardware NVIDIA | driver activo, `nvidia-smi` operativo, NVML saneado | `nvidia_cuda` |
| NFS | red interna operativa + master alcanzable por IP interna | export NFS en master y mount persistente en clientes | `nfs_hpc` |
| Slurm (Munge/DB) | red + (GPU/NVML para GRES) + NFS (uso operativo) + MariaDB | `munge/slurmdbd/slurmctld/slurmd` activos, `slurm.conf/gres.conf` generados, smoke jobs OK | `mariadb_server`, `slurm_db_prep`, `slurm_identities`, `munge`, `slurm_facts`, `slurm_rpm_build`, `slurm_install`, `slurm_controller`, `slurm_compute`, `validate`, `slurm_validate` |
| Entorno LLM | red + (driver/CUDA funcional si hay GPU) | env `llm` con micromamba y checks Torch/CUDA | `llm_env` |

---

## Checklist de facts faltantes / ambigüedades
- [ ] `inventario_glob.ini` está mencionado en guías, pero en este workspace no existe (`inventario_glob.ini: NO_EXISTE`).
- [ ] `slurm_compute` en `inventario.ini` incluye `master`; esto hace que la etapa de compute también aplique al master (puede ser intencional o no).
- [ ] Regla firewalld explícita para `slurmdbd` (`6819/tcp`) no aparece en roles; sí hay validación de escucha en `validate`.
- [ ] Validación dedicada de red (ping/ip/nmcli assert) no existe como rol de validate formal; hay checks operativos/indirectos.
- [ ] Validación NFS end-to-end de escritura/lectura no existe (solo montaje/mountpoint).
- [ ] `roles/slurm_install/files/slurm.conf` existe, pero las tasks actuales usan `templates/slurm.conf.j2` (archivo legacy o referencia histórica).
