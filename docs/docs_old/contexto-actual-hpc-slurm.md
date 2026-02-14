# Contexto actual HPC/Slurm (master)

## Tabla de contenidos
- [0. Metadatos de ejecucion](#0-metadatos-de-ejecucion)
- [1. Contexto del repositorio](#1-contexto-del-repositorio)
- [2. Topologia del cluster (master)](#2-topologia-del-cluster-master)
- [3. Estado de Slurm (core)](#3-estado-de-slurm-core)
- [4. Accounting](#4-accounting)
- [5. GPU/CUDA](#5-gpucuda)
- [6. SSH y acceso](#6-ssh-y-acceso)
- [7. Resumen ejecutivo, riesgos y proximos pasos](#7-resumen-ejecutivo-riesgos-y-proximos-pasos)

## 0. Metadatos de ejecucion

#### 0.1 Fecha/hora local
**Comando**
```bash
date
```
**Salida**
```text
Tue Jan 27 12:30:35 -05 2026
```
**Interpretacion breve**
- Marca temporal local del sistema (incluye offset). 

#### 0.2 Hostname
**Comando**
```bash
hostname
```
**Salida**
```text
master
```
**Interpretacion breve**
- Hostname del master desde el que se ejecuta la recoleccion. 

#### 0.3 Usuario de ejecucion
**Comando**
```bash
whoami
```
**Salida**
```text
sistemas
```
**Interpretacion breve**
- Usuario efectivo que ejecuto los comandos. 

#### 0.4 Rama git actual
**Comando**
```bash
git branch --show-current
```
**Salida**
```text
llm
```
**Interpretacion breve**
- Rama actual del repositorio. 

#### 0.5 Commit actual
**Comando**
```bash
git rev-parse HEAD
```
**Salida**
```text
f1b32c29d0fac46620e2dbb1eda18e5113e9d8c0
```
**Interpretacion breve**
- Hash del commit HEAD actual. 

## 1. Contexto del repositorio

#### 1.1 Ruta del repo
**Comando**
```bash
pwd
```
**Salida**
```text
/home/sistemas/hpc-ansible
```
**Interpretacion breve**
- Directorio de trabajo en el repositorio. 

#### 1.2 Estado git
**Comando**
```bash
git status
```
**Salida**
```text
On branch llm
Your branch is up to date with 'ori/llm'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	extras/historial-comandos-master-26-01.txt

nothing added to commit but untracked files present (use "git add" to track)
```
**Interpretacion breve**
- Estado de cambios locales (incluye archivos sin track). 

#### 1.3 Rama git (confirmacion)
**Comando**
```bash
git branch --show-current
```
**Salida**
```text
llm
```
**Interpretacion breve**
- Confirmacion de la rama actual. 

#### 1.4 Commit HEAD (confirmacion)
**Comando**
```bash
git rev-parse HEAD
```
**Salida**
```text
f1b32c29d0fac46620e2dbb1eda18e5113e9d8c0
```
**Interpretacion breve**
- Confirmacion del commit actual. 

#### 1.5 Ultimos 20 commits
**Comando**
```bash
git log -n 20 --oneline
```
**Salida**
```text
f1b32c2 NFS config on /nfs-hpc (improvised) Updated conda packages with numba and cudatoolkit
0ac2127 Slurm storage by default
44959b5 Set per-node CoreSpec/MemSpec overrides
d44f7ae Reserve resources via CoreSpec and run scontrol with become
31b8b8a Allow per-node Slurm resource overrides
8b31f62 Fix slurm_validate torch prelude and node state check
e622653 Document NVML Slurm flow and broaden auto-resume
7c84976 Fix NVML AutoDetect GRES integration
9810da5 AutoDetect nvml not using GPU references Slurm not working
e8c4b22 AutoDetect nvml (not working)
d57fc63 NFS Ereased
1738029 higiene slurmdbd en /run
dec337f validate-slurm integrated on slurm_validate role
3ce2dc1 Smoke tests
b3565c9 Slurm Improved validation
3b466f6 chdir warning fixed Firewall rich rules update
f67c9fc Facts Topology adjusted
d159647 Slurm-ansible DONE Fully connected Proper nodes info is pending
816817f Slurm-ansible config 5: Slurm installed and working (Rocky)
86b4f47 Cuda instal and llm env config for ubuntu nodes (Not verified)
```
**Interpretacion breve**
- Historial reciente para contexto de cambios. 

#### 1.6 Lista top-level del repo
**Comando**
```bash
ls -la
```
**Salida**
```text
total 76
drwxr-xr-x. 12 sistemas sistemas 4096 Jan 27 12:13 .
drwx------. 23 sistemas sistemas 4096 Jan 26 20:23 ..
-rw-r--r--.  1 sistemas sistemas 8196 Jan 16 09:35 .DS_Store
drwxr-xr-x.  3 root     root       24 Jan 21 14:24 .cache
drwxr-xr-x.  8 sistemas sistemas 4096 Jan 27 12:21 .git
-rw-r--r--.  1 sistemas sistemas   14 Jan 27 12:12 .gitignore
-rw-r--r--.  1 sistemas sistemas 8016 Jan 27 12:12 AGENTS.md
-rw-r--r--.  1 sistemas sistemas  497 Jan 27 12:12 README.md
-rw-r--r--.  1 sistemas sistemas  272 Jan 27 12:12 ansible.cfg
-rw-r--r--.  1 sistemas sistemas  452 Jan 27 12:12 base.yml
drwxr-xr-x.  3 sistemas sistemas   96 Jan 27 12:12 docs
drwxr-xr-x.  2 sistemas sistemas 4096 Jan 27 12:13 extras
drwxr-xr-x.  2 sistemas sistemas   43 Jan 27 12:12 group_vars
drwxr-xr-x.  2 sistemas sistemas   62 Jan 27 12:12 host_vars
-rw-r--r--.  1 sistemas sistemas  406 Jan 27 12:12 inventario-glob.ini
-rw-r--r--.  1 sistemas sistemas  687 Jan 27 12:12 inventario.ini
drwxr-xr-x.  6 sistemas sistemas   82 Jan 27 12:12 llm-project
drwxr-xr-x.  2 sistemas sistemas   63 Jan 27 12:12 playbooks
drwxr-xr-x.  8 sistemas sistemas  118 Jan 27 12:12 playbooks sueltos
-rw-r--r--.  1 sistemas sistemas   41 Jan 27 12:12 requirements.yml
drwxr-xr-x. 21 sistemas sistemas 4096 Jan 27 12:12 roles
-rw-r--r--.  1 sistemas sistemas 1977 Jan 27 12:12 site.yml
-rwxr-xr-x.  1 sistemas sistemas  480 Jan 27 12:12 slurm-test.sh
```
**Interpretacion breve**
- Vista del arbol en la raiz del repo. 

#### 1.7 Arbol de archivos (primer intento)
**Comando**
```bash
find . -maxdepth 2 -type f \\( -name '*.yml' -o -name '*.yaml' -o -name '*.ini' -o -name '*.cfg' -o -name '*.md' \\) | sort
```
**Salida**
```text
bash: -c: line 1: syntax error near unexpected token `('
bash: -c: line 1: `find . -maxdepth 2 -type f \\( -name '*.yml' -o -name '*.yaml' -o -name '*.ini' -o -name '*.cfg' -o -name '*.md' \\) | sort'
```
**Interpretacion breve**
- Fallo por escape de parentesis en el comando. 

#### 1.8 Arbol de archivos (corregido)
**Comando**
```bash
find . -maxdepth 2 -type f ( -name '*.yml' -o -name '*.yaml' -o -name '*.ini' -o -name '*.cfg' -o -name '*.md' ) | sort
```
**Salida**
```text
./AGENTS.md
./README.md
./ansible.cfg
./base.yml
./docs/bitacora_codex.md
./docs/codex-log.md
./docs/slurm-ansible-nvml.md
./extras/STATUS.md
./group_vars/all.yml
./group_vars/hpc_master.yml
./host_vars/master.yml
./host_vars/worker1.yml
./host_vars/worker2.yml
./inventario-glob.ini
./inventario.ini
./llm-project/README.md
./playbooks sueltos/ansible0.cfg
./playbooks/ssh-password-toggle.yml
./playbooks/storage_survey.yml
./requirements.yml
./site.yml
```
**Interpretacion breve**
- Listado resumido de archivos YAML/INI/CFG/MD a maxdepth 2. 

#### 1.9 Inventarios candidatos (rg)
**Comando**
```bash
rg --files -g 'inventario*.ini' -g 'inventory*.ini' || true
```
**Salida**
```text
inventario-glob.ini
playbooks sueltos/inventarios/inventario_glob.ini
playbooks sueltos/inventarios/inventario.ini
inventario.ini
```
**Interpretacion breve**
- Inventarios detectados por patron. 

#### 1.10 Inventario principal (inventario.ini)
**Comando**
```bash
sed -n '1,200p' inventario.ini
```
**Salida**
```text
[hpc_master]
master ansible_host=10.195.34.17 ansible_user=sistemas

[workers_r]
worker1 ansible_host=192.168.34.2 ansible_user=sistemas
worker2 ansible_host=192.168.34.18 ansible_user=sistemas

[workers_u]
worker3 ansible_host=192.168.34.34 ansible_user=sistemas ansible_become_password=[REDACTED]
worker4 ansible_host=192.168.34.50 ansible_user=sistemas ansible_become_password=[REDACTED]

[workers]
worker1
worker2
worker3
worker4

[slurm_all]
master
worker1
worker2
; worker3
; worker4

[slurm_compute]
master
worker1
worker2

[slurm_gpu]
; master
worker1
worker2
; worker3
; worker4

[all:vars]
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_private_key_file=~/.ssh/id_ed25519
```
**Interpretacion breve**
- Inventario por defecto del repo. Passwords redacted si aparecen. 

#### 1.11 Inventario alterno (inventory.ini)
**Comando**
```bash
sed -n '1,200p' inventory.ini
```
**Salida**
```text
sed: can't read inventory.ini: No such file or directory
```
**Interpretacion breve**
- No existe en este repo (solo referencia). 

#### 1.12 group_vars/ (lista)
**Comando**
```bash
ls -la group_vars || true
```
**Salida**
```text
total 12
drwxr-xr-x.  2 sistemas sistemas   43 Jan 27 12:12 .
drwxr-xr-x. 12 sistemas sistemas 4096 Jan 27 12:13 ..
-rw-r--r--.  1 sistemas sistemas 3336 Jan 27 12:12 all.yml
-rw-r--r--.  1 sistemas sistemas  716 Jan 27 12:12 hpc_master.yml
```
**Interpretacion breve**
- Archivos de variables globales y por grupo. 

#### 1.13 host_vars/ (lista)
**Comando**
```bash
ls -la host_vars || true
```
**Salida**
```text
total 16
drwxr-xr-x.  2 sistemas sistemas   62 Jan 27 12:12 .
drwxr-xr-x. 12 sistemas sistemas 4096 Jan 27 12:13 ..
-rw-r--r--.  1 sistemas sistemas  179 Jan 27 12:12 master.yml
-rw-r--r--.  1 sistemas sistemas  216 Jan 27 12:12 worker1.yml
-rw-r--r--.  1 sistemas sistemas  217 Jan 27 12:12 worker2.yml
```
**Interpretacion breve**
- Archivos de variables por host. 

#### 1.14 group_vars/ (archivos)
**Comando**
```bash
find group_vars -type f -maxdepth 2 -print | sort || true
```
**Salida**
```text
group_vars/all.yml
group_vars/hpc_master.yml
```
**Interpretacion breve**
- Rutas de archivos en group_vars. 

#### 1.15 host_vars/ (archivos)
**Comando**
```bash
find host_vars -type f -maxdepth 2 -print | sort || true
```
**Salida**
```text
host_vars/master.yml
host_vars/worker1.yml
host_vars/worker2.yml
```
**Interpretacion breve**
- Rutas de archivos en host_vars. 

#### 1.16 group_vars/all.yml
**Comando**
```bash
sed -n '1,200p' group_vars/all.yml
```
**Salida**
```text
common_packages:
  - git
  - curl
  - wget
  - vim
  - rsync
  - tar
  - unzip
  - htop
  - btop
  - tmux
  - jq
  - tree

enable_chrony: true

# =====================
# SSH (password habilitado)
# =====================
ssh_port: 22
ssh_permit_root_login: "yes"
ssh_password_authentication: "yes"

# =====================
# LLM env (micromamba)
# =====================
llm_conda_packages:
  - python
  - pip
  - pytorch
  - torchvision
  - torchaudio
  - pytorch-cuda
  - numba
  - cudatoolkit

llm_pip_packages:
  - transformers
  - datasets
  - accelerate
  - peft
  - safetensors
  - sentencepiece

llm_python_packages:
  - numpy
  - torch
  - transformers

# =====================
# Firewall Rules
# =====================

# Slurm firewall
slurm_firewalld_zone: "public"
slurm_internal_cidr: "192.168.34.0/24"
slurmctld_port: 6817
slurmd_port: 6818


# =====================
# SLURM-Munge settings
# =====================

munge_uid: 1011
munge_gid: 1011
slurm_uid: 1012
slurm_gid: 1012

munge_key_host: master   # nombre de inventario del master
munge_key_size_mb: 4

# =====================
# --- Slurm core ---
# =====================
slurm_version: "23.11.3"
slurm_tarball_url: "https://download.schedmd.com/slurm/slurm-{{ slurm_version }}.tar.bz2"

slurm_etc_dir: /etc/slurm
slurm_log_dir: /var/log/slurm

# cgroup
slurm_cgroup_conf: |
  CgroupPlugin=autodetect

# control machine
# Para construir slurm.conf a partir de facts
slurm_control_machine: "master"     # nombre de inventario del master
slurm_mem_reserve_mb: 1024          # reserva RAM para el SO (MB)

# Define particiones por grupos de inventario
slurm_partitions:
  - name: debug
    groups: ["slurm_compute"]
    default: true
    max_time: "INFINITE"
    state: "UP"
  - name: gpu
    groups: ["slurm_gpu"]
    default: false
    max_time: "INFINITE"
    state: "UP"
    shared: "YES"

slurm_srun_port_range: "60001-60100"

# =====================
# Slurm - Overwrites simples de recursos (por host o por grupo)
# =====================
# Para ajustar recursos visibles a Slurm en cualquier nodo o grupo, define
# variables en:
# - host_vars/<hostname>.yml (override por nodo)
# - group_vars/<group>.yml  (override por grupo: p.ej. slurm_gpu, slurm_compute)
#
# Variables soportadas:
#   slurm_cpus, slurm_sockets, slurm_cores_per_socket, slurm_threads_per_core,
#   slurm_real_memory, slurm_node_gres
#   slurm_core_spec_count (cores reservados), slurm_mem_spec_limit_mb (mem reservada)
#
# Ejemplo por nodo (host_vars/worker1.yml):
#   # Opcion A: limitar recursos visibles (puede causar INVALID_REG si no coincide con slurmd)
#   slurm_cpus: 12
#   slurm_real_memory: 48000
#   slurm_node_gres: "gpu:quadro_p1000:1"
#   # Opcion B (recomendada): reservar recursos sin mismatch
#   slurm_core_spec_count: 2
#   slurm_mem_spec_limit_mb: 8000
#
# Ejemplo por grupo (group_vars/slurm_gpu.yml):
#   slurm_real_memory: 56000
#   slurm_node_gres: "gpu:quadro_p1000:1"
#
# Nota: si defines slurm_node_gres manualmente, Slurm usara ese valor aunque
# NVML detecte mas GPUs. AutoDetect=nvml sigue habilitado para detalles.

# Slurm validate: activar micromamba y entorno llm para pruebas de torch
slurm_validate_torch:
  enabled: "auto"
  python: "python3"
  prelude: |
    set +u
    eval "$(micromamba shell hook --shell bash)"
    micromamba activate llm
    set -u
```
**Interpretacion breve**
- Defaults globales del cluster (paquetes, SSH, Slurm, firewall, LLM). 

#### 1.17 group_vars/hpc_master.yml
**Comando**
```bash
sed -n '1,200p' group_vars/hpc_master.yml
```
**Salida**
```text
# MariaDB module stream (Rocky/RHEL)
mariadb_module_stream: "10.11"

# NFS HPC (servidor)
nfs_hpc_server_enabled: true

# SlurmDB MariaDB settings
slurmdb_mysql_db: "slurm_acct_db"
slurmdb_mysql_user: "slurm"

slurmdb_mysql_password: \"[REDACTED]\"
slurmdb_mysql_hosts:
  - "localhost"
  - "master"

mariadb_slurm_tuning:
  innodb_buffer_pool_size: "4096M"
  innodb_log_file_size: "64M"
  innodb_lock_wait_timeout: "900"
  max_allowed_packet: "500M"

slurmdbd_port: 6819
slurmdbd_host: "localhost"
slurmdbd_storage_host: "localhost"
slurmdbd_storage_loc: "{{ slurmdb_mysql_db }}"   # slurm_acct_db
slurmdbd_storage_user: "{{ slurmdb_mysql_user | first}}" # slurm
slurmdbd_storage_pass: "{{ slurmdb_mysql_password }}" # [REDACTED]
```
**Interpretacion breve**
- Overrides y parametros del master (MariaDB/SlurmDB/NFS). Passwords redacted. 

#### 1.18 host_vars/master.yml
**Comando**
```bash
sed -n '1,200p' host_vars/master.yml
```
**Salida**
```text
# Reservas para administracion sin causar INVALID_REG.
# Slurm mantiene los totales reales, pero no asigna estos recursos.
slurm_core_spec_count: 1
slurm_mem_spec_limit_mb: 16000
```
**Interpretacion breve**
- Overrides del master para recursos Slurm reservados. 

#### 1.19 host_vars/worker1.yml
**Comando**
```bash
sed -n '1,200p' host_vars/worker1.yml
```
**Salida**
```text
# Reservas para administracion sin causar INVALID_REG.
# Slurm mantiene los totales reales, pero no asigna estos recursos.
slurm_core_spec_count: 2
slurm_mem_spec_limit_mb: 8000
slurm_node_gres: "gpu:quadro_p1000:1"
```
**Interpretacion breve**
- Overrides del worker1, incluye GRES GPU declarada. 

#### 1.20 host_vars/worker2.yml
**Comando**
```bash
sed -n '1,200p' host_vars/worker2.yml
```
**Salida**
```text
# Reservas para administracion sin causar INVALID_REG.
# Slurm mantiene los totales reales, pero no asigna estos recursos.
slurm_core_spec_count: 3
slurm_mem_spec_limit_mb: 12000
slurm_node_gres: "gpu:quadro_p1000:1"
```
**Interpretacion breve**
- Overrides del worker2, incluye GRES GPU declarada. 

#### 1.21 roles/ (lista)
**Comando**
```bash
ls -la roles || true
```
**Salida**
```text
total 8
drwxr-xr-x. 21 sistemas sistemas 4096 Jan 27 12:12 .
drwxr-xr-x. 12 sistemas sistemas 4096 Jan 27 12:13 ..
drwxr-xr-x.  3 sistemas sistemas   19 Jan 27 12:12 common
drwxr-xr-x.  3 sistemas sistemas   19 Jan 27 12:12 firewall
drwxr-xr-x.  4 sistemas sistemas   35 Jan 27 12:12 llm_env
drwxr-xr-x.  4 sistemas sistemas   35 Jan 27 12:12 llm_project
drwxr-xr-x.  4 sistemas sistemas   35 Jan 27 12:12 mariadb_server
drwxr-xr-x.  4 sistemas sistemas   35 Jan 27 12:12 munge
drwxr-xr-x.  4 sistemas sistemas   35 Jan 27 12:12 network_internal
drwxr-xr-x.  6 sistemas sistemas   68 Jan 27 12:12 nfs_hpc
drwxr-xr-x.  5 sistemas sistemas   51 Jan 27 12:12 nvidia_cuda
drwxr-xr-x.  3 sistemas sistemas   19 Jan 27 12:12 slurm_compute
drwxr-xr-x.  5 sistemas sistemas   52 Jan 27 12:12 slurm_controller
drwxr-xr-x.  4 sistemas sistemas   35 Jan 27 12:12 slurm_db_prep
drwxr-xr-x.  3 sistemas sistemas   19 Jan 27 12:12 slurm_facts
drwxr-xr-x.  3 sistemas sistemas   19 Jan 27 12:12 slurm_identities
drwxr-xr-x.  7 sistemas sistemas   81 Jan 27 12:12 slurm_install
drwxr-xr-x.  3 sistemas sistemas   19 Jan 27 12:12 slurm_rpm_build
drwxr-xr-x.  5 sistemas sistemas   52 Jan 27 12:12 slurm_validate
drwxr-xr-x.  5 sistemas sistemas   51 Jan 27 12:12 users_ssh
drwxr-xr-x.  4 sistemas sistemas   35 Jan 27 12:12 validate
```
**Interpretacion breve**
- Roles disponibles en el repo. 

#### 1.22 roles/ (estructura de directorios)
**Comando**
```bash
find roles -maxdepth 2 -type d -print | sort || true
```
**Salida**
```text
roles
roles/common
roles/common/tasks
roles/firewall
roles/firewall/tasks
roles/llm_env
roles/llm_env/defaults
roles/llm_env/tasks
roles/llm_project
roles/llm_project/defaults
roles/llm_project/tasks
roles/mariadb_server
roles/mariadb_server/defaults
roles/mariadb_server/tasks
roles/munge
roles/munge/handlers
roles/munge/tasks
roles/network_internal
roles/network_internal/defaults
roles/network_internal/tasks
roles/nfs_hpc
roles/nfs_hpc/defaults
roles/nfs_hpc/handlers
roles/nfs_hpc/tasks
roles/nfs_hpc/templates
roles/nvidia_cuda
roles/nvidia_cuda/defaults
roles/nvidia_cuda/handlers
roles/nvidia_cuda/tasks
roles/slurm_compute
roles/slurm_compute/tasks
roles/slurm_controller
roles/slurm_controller/defaults
roles/slurm_controller/tasks
roles/slurm_controller/templates
roles/slurm_db_prep
roles/slurm_db_prep/handlers
roles/slurm_db_prep/tasks
roles/slurm_facts
roles/slurm_facts/tasks
roles/slurm_identities
roles/slurm_identities/tasks
roles/slurm_install
roles/slurm_install/defaults
roles/slurm_install/files
roles/slurm_install/handlers
roles/slurm_install/tasks
roles/slurm_install/templates
roles/slurm_rpm_build
roles/slurm_rpm_build/tasks
roles/slurm_validate
roles/slurm_validate/defaults
roles/slurm_validate/tasks
roles/slurm_validate/templates
roles/users_ssh
roles/users_ssh/defaults
roles/users_ssh/handlers
roles/users_ssh/tasks
roles/validate
roles/validate/defaults
roles/validate/tasks
```
**Interpretacion breve**
- Arbol de directorios bajo roles (maxdepth 2). 

#### 1.23 roles/ (tasks y README)
**Comando**
```bash
find roles -maxdepth 3 -type f -name 'main.yml' -o -name 'README.md' | sort || true
```
**Salida**
```text
roles/common/tasks/main.yml
roles/firewall/tasks/main.yml
roles/llm_env/defaults/main.yml
roles/llm_env/tasks/main.yml
roles/llm_project/defaults/main.yml
roles/llm_project/tasks/main.yml
roles/mariadb_server/defaults/main.yml
roles/mariadb_server/tasks/main.yml
roles/munge/handlers/main.yml
roles/munge/tasks/main.yml
roles/network_internal/defaults/main.yml
roles/network_internal/tasks/main.yml
roles/nfs_hpc/defaults/main.yml
roles/nfs_hpc/handlers/main.yml
roles/nfs_hpc/tasks/main.yml
roles/nvidia_cuda/defaults/main.yml
roles/nvidia_cuda/handlers/main.yml
roles/nvidia_cuda/tasks/main.yml
roles/slurm_compute/tasks/main.yml
roles/slurm_controller/defaults/main.yml
roles/slurm_controller/tasks/main.yml
roles/slurm_db_prep/handlers/main.yml
roles/slurm_db_prep/tasks/main.yml
roles/slurm_facts/tasks/main.yml
roles/slurm_identities/tasks/main.yml
roles/slurm_install/defaults/main.yml
roles/slurm_install/handlers/main.yml
roles/slurm_install/tasks/main.yml
roles/slurm_rpm_build/tasks/main.yml
roles/slurm_validate/defaults/main.yml
roles/slurm_validate/tasks/main.yml
roles/users_ssh/defaults/main.yml
roles/users_ssh/handlers/main.yml
roles/users_ssh/tasks/main.yml
roles/validate/defaults/main.yml
roles/validate/tasks/main.yml
```
**Interpretacion breve**
- Archivos tasks/main.yml y README.md detectados. 

#### 1.24 roles/common/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/common/tasks/main.yml
```
**Salida**
```text
---
- name: Actualizar caché de paquetes
  ansible.builtin.dnf:
    update_cache: true

- name: Instalar paquetes base
  ansible.builtin.dnf:
    name: "{{ common_packages }}"
    state: present

- name: Instalar chrony si aplica
  ansible.builtin.dnf:
    name: chrony
    state: present
  when: enable_chrony | bool

- name: Habilitar chronyd si aplica
  ansible.builtin.service:
    name: chronyd
    state: started
    enabled: true
  when: enable_chrony | bool
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.25 roles/firewall/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/firewall/tasks/main.yml
```
**Salida**
```text
---
- name: Asegurar firewalld instalado
  ansible.builtin.dnf:
    name: firewalld
    state: present

- name: Habilitar firewalld
  ansible.builtin.service:
    name: firewalld
    state: started
    enabled: true

- name: Permitir SSH
  ansible.posix.firewalld:
    service: ssh
    permanent: true
    state: enabled
    immediate: true

# -------------------------------------------------------------------
# Slurm - allow controller <-> compute traffic only from internal CIDR
# Ports:
# - 6817/tcp: slurmctld (controller on master)
# - 6818/tcp: slurmd (daemon on compute nodes)
# -------------------------------------------------------------------

- name: Firewall | Slurm | Allow slurmctld (6817/tcp) from internal network (masters)
  ansible.posix.firewalld:
    zone: "{{ slurm_firewalld_zone }}"
    permanent: true
    immediate: true
    state: enabled
    rich_rule: >-
      rule family="ipv4"
      source address="{{ slurm_internal_cidr }}"
      port port="{{ slurmctld_port }}" protocol="tcp"
      accept
  when:
    - slurm_internal_cidr is defined
    - inventory_hostname in groups.get('hpc_master', [])
  tags: [firewall, slurm, slurm_firewall]

- name: Firewall | Slurm | Allow slurmd (6818/tcp) from internal network (compute)
  ansible.posix.firewalld:
    zone: "{{ slurm_firewalld_zone }}"
    permanent: true
    immediate: true
    state: enabled
    rich_rule: >-
      rule family="ipv4"
      source address="{{ slurm_internal_cidr }}"
      port port="{{ slurmd_port }}" protocol="tcp"
      accept
  when:
    - slurm_internal_cidr is defined
    # Ajusta el grupo según tu inventario actual:
    - inventory_hostname in (groups.get('workers_r', []) + groups.get('workers', []))
  tags: [firewall, slurm, slurm_firewall]

- name: Firewall | Slurm | Show rich rules (debug)
  ansible.builtin.command: firewall-cmd --zone={{ slurm_firewalld_zone }} --list-rich-rules
  changed_when: false
  when:
    - slurm_internal_cidr is defined
    - inventory_hostname in (groups.get('hpc_master', []) + groups.get('workers_r', []) + groups.get('workers', []))
  tags: [firewall, slurm, slurm_firewall, slurm_validate]
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.26 roles/llm_env/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/llm_env/tasks/main.yml
```
**Salida**
```text
---
- name: LLM Env | Ensure base packages
  ansible.builtin.dnf:
    name:
      - bzip2
      - tar
      - curl
      - ca-certificates
    state: present
    update_cache: true
  when: ansible_facts['os_family'] == 'RedHat'

- name: LLM Env | Ensure base packages (Ubuntu)
  ansible.builtin.apt:
    name:
      - bzip2
      - tar
      - curl
      - ca-certificates
    state: present
    update_cache: true
  when: ansible_facts['os_family'] == 'Debian'

- name: LLM Env | Ensure micromamba root exists
  ansible.builtin.file:
    path: "{{ llm_micromamba_root }}"
    state: directory
    owner: root
    group: root
    mode: "0755"

- name: LLM Env | Download micromamba (latest)
  ansible.builtin.get_url:
    url: "https://github.com/mamba-org/micromamba-releases/releases/latest/download/micromamba-linux-64.tar.bz2"
    dest: "/tmp/micromamba.tar.bz2"
    mode: "0644"
  register: _micromamba_download
  retries: 3
  delay: 5
  until: _micromamba_download is succeeded

- name: LLM Env | Create micromamba install dir
  ansible.builtin.file:
    path: /opt/micromamba
    state: directory
    owner: root
    group: root
    mode: "0755"
  become: true

- name: LLM Env | Extract micromamba
  ansible.builtin.unarchive:
    src: "/tmp/micromamba.tar.bz2"
    dest: "{{ llm_micromamba_root }}"
    remote_src: true
    creates: "{{ llm_micromamba_root }}/bin/micromamba"
  become: true

- name: LLM Env | Symlink micromamba into /usr/local/bin
  ansible.builtin.file:
    src: "{{ llm_micromamba_root }}/bin/micromamba"
    dest: "/usr/local/bin/micromamba"
    state: link
  become: true

- name: LLM Env | Ensure micromamba profile
  ansible.builtin.copy:
    dest: /etc/profile.d/micromamba.sh
    owner: root
    group: root
    mode: "0644"
    content: |
      # Managed by Ansible (llm_env role)
      export MAMBA_ROOT_PREFIX="{{ llm_micromamba_root }}"
      export PATH="{{ llm_micromamba_root }}/bin:$PATH"

- name: LLM Env | Check if env exists
  ansible.builtin.stat:
    path: "{{ llm_micromamba_root }}/envs/{{ llm_env_name }}"
  register: _env_stat

- name: LLM Env | Create env (first time)
  ansible.builtin.command: >
    {{ llm_micromamba_bin }} create -y -n {{ llm_env_name }}
    {% for c in llm_conda_channels %} -c {{ c }}{% endfor %}
    {% for p in llm_conda_packages %} {{ p }}{% endfor %}
  args:
    creates: "/opt/micromamba/envs/{{ llm_env_name }}/conda-meta/history"
  environment:
    MAMBA_ROOT_PREFIX: "/opt/micromamba"
  when: not _env_stat.stat.exists
  register: _mamba_create
  changed_when: true

- name: LLM Env | Set env exists flag
  ansible.builtin.set_fact:
    _llm_env_exists: "{{ _env_stat.stat.exists or (_mamba_create is defined and _mamba_create is changed) }}"

- name: LLM Env | Ensure llm env channel config
  ansible.builtin.copy:
    dest: "{{ llm_micromamba_root }}/envs/{{ llm_env_name }}/.condarc"
    owner: root
    group: root
    mode: "0644"
    content: |
      channels:
        - pytorch
        - nvidia
        - conda-forge
      channel_priority: strict
  when: _llm_env_exists | bool

- name: LLM Env | Install/update conda packages in existing env
  ansible.builtin.command: >
    {{ llm_micromamba_bin }} install -y -n {{ llm_env_name }}
    {% for c in llm_conda_channels %} -c {{ c }}{% endfor %}
    {% for p in llm_conda_packages %} {{ p }}{% endfor %}
  environment:
    MAMBA_ROOT_PREFIX: "/opt/micromamba"
  when: _env_stat.stat.exists
  register: conda_install
  changed_when: "'All requested packages already installed' not in conda_install.stdout"

- name: LLM Env | Install PyTorch CUDA stack
  ansible.builtin.command: >
    {{ llm_micromamba_bin }} install -y -n {{ llm_env_name }}
    -c pytorch -c nvidia -c conda-forge
    python={{ llm_pytorch_python_version }} pytorch torchvision torchaudio pytorch-cuda=12.4
  environment:
    MAMBA_ROOT_PREFIX: "/opt/micromamba"
  register: _pytorch_cuda_install
  changed_when: "'All requested packages already installed' not in _pytorch_cuda_install.stdout"
  when: _llm_env_exists | bool

- name: LLM Env | Fail if pip packages include torch
  ansible.builtin.fail:
    msg: >-
      llm_pip_packages incluye torch. Esto puede sobrescribir el torch conda.
      Elimine torch de la lista pip y reintente.
  when: llm_pip_packages | select('match', '^torch($|[=<>])') | list | length > 0

- name: LLM Env | Compute pip marker hash
  ansible.builtin.set_fact:
    llm_pip_hash: "{{ llm_pip_packages | sort | join(' ') | hash('sha1') }}"
  when: llm_pip_packages | length > 0

- name: LLM Env | Check pip marker
  ansible.builtin.stat:
    path: "{{ llm_micromamba_root }}/envs/{{ llm_env_name }}/.llm_pip_installed_{{ llm_pip_hash }}"
  register: _pip_marker

- name: LLM Env | Install pip packages inside env
  ansible.builtin.command: >
    {{ llm_micromamba_bin }} run -n {{ llm_env_name }}
    pip install -U {% for p in llm_pip_packages %} {{ p }}{% endfor %}
  environment:
    MAMBA_ROOT_PREFIX: "/opt/micromamba"
  when: llm_pip_packages | length > 0 and not _pip_marker.stat.exists
  register: _pip_install
  changed_when: true

- name: LLM Env | Mark pip packages installed
  ansible.builtin.file:
    path: "{{ llm_micromamba_root }}/envs/{{ llm_env_name }}/.llm_pip_installed_{{ llm_pip_hash }}"
    state: touch
  when: llm_pip_packages | length > 0 and _pip_install is changed

- name: LLM Env | Detect torch installer
  ansible.builtin.command: >
    /bin/sh -c "timeout 60s {{ llm_micromamba_bin }} run -n {{ llm_env_name }}
    python -c \"import importlib.metadata as m; 
    dist = m.distribution('torch'); 
    installer = (dist.read_text('INSTALLER') or '').strip(); 
    print(installer if installer else 'unknown')\""
  environment:
    MAMBA_ROOT_PREFIX: "/opt/micromamba"
  register: _torch_installer
  changed_when: false
  when: _llm_env_exists | bool

- name: LLM Env | Fail if torch installer check times out
  ansible.builtin.fail:
    msg: >-
      La validacion de installer de torch excedio 60s. Revise el estado de
      micromamba/conda locks y reintente.
  when:
    - _llm_env_exists | bool
    - _torch_installer.rc == 124

- name: LLM Env | Fail if torch installed via pip
  ansible.builtin.fail:
    msg: >-
      torch fue instalado via pip en el env {{ llm_env_name }}. Esto puede anular
      el stack CUDA. Remueva torch pip y reinstale via micromamba con canales CUDA.
  when:
    - _llm_env_exists | bool
    - _torch_installer.stdout | trim == 'pip'

- name: LLM Env | Detect NVIDIA GPU
  ansible.builtin.command: "lspci -nn -d 10de:"
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.27 roles/llm_project/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/llm_project/tasks/main.yml
```
**Salida**
```text
---
- name: LLM Project | Determine owner/group
  ansible.builtin.set_fact:
    _llm_owner_user: "{{ (llm_project_owner | default('') | trim | length > 0) | ternary(llm_project_owner, ansible_user_id) }}"
    _llm_owner_group: "{{ (llm_project_group | default('') | trim | length > 0) | ternary(llm_project_group, ansible_user_gid | string) }}"

- name: LLM Project | Ensure project destination dir exists
  ansible.builtin.file:
    path: "{{ llm_project_dst_dir }}"
    state: directory
    owner: "{{ _llm_owner_user }}"
    group: "{{ _llm_owner_group }}"
    mode: "0775"

- name: LLM Project | Copy llm-project to destination (controller -> master)
  ansible.builtin.copy:
    src: "{{ llm_project_src_dir }}/"
    dest: "{{ llm_project_dst_dir }}/"
    owner: "{{ _llm_owner_user }}"
    group: "{{ _llm_owner_group }}"
    mode: preserve
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.28 roles/mariadb_server/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/mariadb_server/tasks/main.yml
```
**Salida**
```text
---
- name: MariaDB | Install base packages (Rocky/RHEL)
  ansible.builtin.dnf:
    name:
      - mariadb-server
      - mariadb-devel
      - mariadb-connector-c-devel
      - readline-devel
    state: present
  when: ansible_facts['os_family'] == 'RedHat'
  tags: [mariadb]

- name: MariaDB | Enable and start service
  ansible.builtin.service:
    name: mariadb
    enabled: true
    state: started
  tags: [mariadb]

- name: MariaDB | Check server version
  ansible.builtin.command: mariadb -N -B -e 'SELECT VERSION();'
  register: mariadb_version
  changed_when: false
  tags: [verify]

- name: MariaDB | Parse major version
  ansible.builtin.set_fact:
    mariadb_version_major: "{{ (mariadb_version.stdout | default('0') | trim | regex_search('^[0-9]+')) | default('0') | int }}"
  tags: [verify]

- name: MariaDB | Assert minimum version
  ansible.builtin.assert:
    that:
      - (mariadb_version_major | int) >= (mariadb_min_version_major | int)
    fail_msg: >-
      MariaDB version {{ mariadb_version.stdout | default('unknown') }} is below
      required major {{ mariadb_min_version_major }}.
  tags: [verify]
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.29 roles/munge/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/munge/tasks/main.yml
```
**Salida**
```text
- name: Ensure EPEL is present on Rocky
  ansible.builtin.dnf:
    name: epel-release
    state: present
  when: ansible_facts['os_family'] == 'RedHat'
  tags: [munge]

- name: Install munge-devel from CRB on Rocky
  ansible.builtin.dnf:
    name: munge-devel
    state: present
    enablerepo: crb
  when: ansible_facts['os_family'] == 'RedHat'
  tags: [munge]

- name: Install munge package on Rocky
  ansible.builtin.dnf:
    name: munge
    state: present
  when: ansible_facts['os_family'] == 'RedHat'
  tags: [munge]

- name: Install munge packages on Ubuntu
  ansible.builtin.apt:
    name:
      - munge
      - libmunge-dev
    state: present
    update_cache: true
  when: ansible_facts['os_family'] == 'Debian'
  tags: [munge]

- name: Ensure munge directories exist with correct perms
  ansible.builtin.file:
    path: "{{ item }}"
    state: directory
    owner: munge
    group: munge
    mode: "0700"
  loop:
    - /etc/munge
    - /var/log/munge
    - /var/lib/munge
  tags: [munge]

# Evita problemas con /run (tmpfs) tras reinicio
- name: Ensure systemd tmpfiles entry for /run/munge
  ansible.builtin.copy:
    dest: /etc/tmpfiles.d/munge.conf
    owner: root
    group: root
    mode: "0644"
    content: |
      d /run/munge 0711 munge munge -
  tags: [munge]

- name: Create /run/munge via tmpfiles
  ansible.builtin.command: systemd-tmpfiles --create /etc/tmpfiles.d/munge.conf
  changed_when: false
  tags: [munge]

- name: Ensure /run/munge perms on Rocky/RHEL
  ansible.builtin.file:
    path: /run/munge
    state: directory
    owner: munge
    group: munge
    mode: "0711"
  when: ansible_facts['os_family'] == 'RedHat'
  tags: [munge]

# Generar key SOLO en el master (si no existe)
- name: Generate munge key on key host if missing
  ansible.builtin.command: "dd if=/dev/urandom of=/etc/munge/munge.key bs=1M count={{ munge_key_size_mb }}"
  args:
    creates: /etc/munge/munge.key
  when: inventory_hostname == munge_key_host
  tags: [munge]

- name: Set ownership and mode on munge key (key host)
  ansible.builtin.file:
    path: /etc/munge/munge.key
    owner: munge
    group: munge
    mode: "0600"
  when: inventory_hostname == munge_key_host
  tags: [munge]

# Leer key desde el master y distribuirla a todos
- name: Slurp munge key from key host
  ansible.builtin.slurp:
    src: /etc/munge/munge.key
  delegate_to: "{{ munge_key_host }}"
  run_once: true
  register: munge_key_slurped
  tags: [munge]

- name: Distribute munge key to all nodes
  ansible.builtin.copy:
    dest: /etc/munge/munge.key
    content: "{{ munge_key_slurped.content | b64decode }}"
    owner: munge
    group: munge
    mode: "0600"
  notify: Restart munge
  tags: [munge]

- name: Enable and start munge service
  ansible.builtin.systemd:
    name: munge
    enabled: true
    state: started
  tags: [munge]

- name: Verify munge local STATUS
  ansible.builtin.shell: "munge -n | unmunge | grep -q STATUS"
  changed_when: false
  tags: [munge]
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.30 roles/network_internal/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/network_internal/tasks/main.yml
```
**Salida**
```text
---
- name: Red Interna | Obtener conexiones NM distintas de {{ network_internal_keep_if }}
  ansible.builtin.shell: |
    nmcli -t -f NAME,DEVICE con show | awk -F: '$2 != "{{ network_internal_keep_if }}" && $2 != "" {print $1}'
  register: nmcli_conns
  changed_when: false

- name: Red Interna | Filtrar conexiones a borrar (excluir Tailscale)
  ansible.builtin.set_fact:
    nmcli_to_delete: >-
      {%- set out = [] -%}
      {%- for line in nmcli_conns.stdout_lines | default([]) -%}
      {%- set parts = line.split(':', 1) -%}
      {%- set name = parts[0] -%}
      {%- set dev = (parts | length > 1) | ternary(parts[1], '') -%}
      {%- set is_excluded_iface = dev in network_internal_exclude_ifaces -%}
      {%- set is_excluded_name = (name | regex_search(network_internal_exclude_conn_regex)) is not none -%}
      {%- if dev and dev != network_internal_keep_if and not is_excluded_iface and not is_excluded_name -%}
      {%-   set _ = out.append(name) -%}
      {%- endif -%}
      {%- endfor -%}
      {{ out }}

- name: Red Interna | Mostrar conexiones a borrar
  ansible.builtin.debug:
    var: nmcli_to_delete

- name: Red Interna | Borrar conexiones no permitidas
  ansible.builtin.command: nmcli con delete "{{ item }}"
  loop: "{{ nmcli_to_delete }}"
  when: nmcli_to_delete | length > 0

- name: Red Interna | Configurar enlaces internos en el master
  when: inventory_hostname == "master"
  block:
    - name: Red Interna | Iterar enlaces master
      ansible.builtin.include_tasks: master_link.yml
      loop: "{{ network_internal_links | dict2items }}"
      loop_control:
        loop_var: link_item

- name: Red Interna | Configurar enlace interno en worker
  when:
    - inventory_hostname != "master"
    - inventory_hostname in network_internal_links
  block:
    - name: Red Interna | Definir enlace del worker
      ansible.builtin.set_fact:
        _worker_link: "{{ network_internal_links[inventory_hostname] }}"

    - name: Red Interna | Verificar conexion int-master
      ansible.builtin.command: nmcli -t -f NAME con show int-master
      register: worker_link_exists
      changed_when: false
      failed_when: false

    - name: Red Interna | Crear conexion int-master
      ansible.builtin.command: >-
        nmcli con add type ethernet ifname {{ _worker_link.worker_if }} con-name int-master
        ipv4.method manual ipv4.addresses {{ _worker_link.worker_ip }} ipv6.method ignore
      when: worker_link_exists.rc != 0

    - name: Red Interna | Leer parametros int-master
      ansible.builtin.command: nmcli -g ipv4.addresses,ipv4.method,ipv6.method con show int-master
      register: worker_link_settings
      changed_when: false

    - name: Red Interna | Calcular ajustes int-master
      ansible.builtin.set_fact:
        _worker_link_needs_mod: "{{ worker_link_settings.stdout | trim != (_worker_link.worker_ip ~ ':manual:ignore') }}"

    - name: Red Interna | Ajustar int-master
      ansible.builtin.command: >-
        nmcli con mod int-master ipv4.addresses {{ _worker_link.worker_ip }} ipv4.method manual ipv6.method ignore
      when: _worker_link_needs_mod

    - name: Red Interna | Activar int-master
      ansible.builtin.command: nmcli con up int-master
      changed_when: false
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.31 roles/nfs_hpc/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/nfs_hpc/tasks/main.yml
```
**Salida**
```text
---
- name: NFS | Determinar familia de SO
  ansible.builtin.set_fact:
    nfs_hpc_os_family: "{{ ansible_facts.os_family | default('RedHat') }}"
  changed_when: false
  tags: [nfs]

- name: NFS | Asegurar grupo de escritura en todos los nodos
  ansible.builtin.group:
    name: "{{ nfs_hpc_write_group }}"
    gid: "{{ (nfs_hpc_write_group_gid is number) | ternary(nfs_hpc_write_group_gid, omit) }}"
    state: present
  when: nfs_hpc_server_enabled | bool or nfs_hpc_client_enabled | bool
  tags: [nfs, nfs_permissions]

- name: NFS | Agregar usuarios al grupo de escritura
  ansible.builtin.user:
    name: "{{ item }}"
    groups: "{{ nfs_hpc_write_group }}"
    append: true
  loop: "{{ nfs_hpc_write_group_users }}"
  when:
    - nfs_hpc_write_group_users | length > 0
    - nfs_hpc_server_enabled | bool or nfs_hpc_client_enabled | bool
  tags: [nfs, nfs_permissions]

- name: NFS | Instalar paquetes del servidor
  ansible.builtin.package:
    name: "{{ nfs_hpc_server_packages.get(nfs_hpc_os_family, nfs_hpc_server_packages['RedHat']) }}"
    state: present
  when: nfs_hpc_server_enabled | bool
  tags: [nfs, nfs_server]

- name: NFS | Crear directorio del share en servidor
  ansible.builtin.file:
    path: "{{ nfs_hpc_share_dir }}"
    state: directory
    owner: root
    group: "{{ nfs_hpc_write_group }}"
    mode: "{{ nfs_hpc_share_mode }}"
  when: nfs_hpc_server_enabled | bool
  tags: [nfs, nfs_server, nfs_permissions]

- name: NFS | Configurar exports
  ansible.builtin.template:
    src: exports.j2
    dest: "{{ nfs_hpc_export_file }}"
    owner: root
    group: root
    mode: "0644"
  when: nfs_hpc_server_enabled | bool
  notify: NFS | Recargar exports
  tags: [nfs, nfs_server]

- name: NFS | Habilitar y arrancar servicio NFS
  ansible.builtin.service:
    name: "{{ nfs_hpc_server_service.get(nfs_hpc_os_family, nfs_hpc_server_service['RedHat']) }}"
    state: started
    enabled: true
  when: nfs_hpc_server_enabled | bool
  tags: [nfs, nfs_server]

- name: NFS | Verificar firewalld activo (server)
  ansible.builtin.command: systemctl is-active firewalld
  register: _nfs_firewalld_active
  changed_when: false
  failed_when: false
  when:
    - nfs_hpc_server_enabled | bool
    - nfs_hpc_firewall_manage | bool
  tags: [nfs, nfs_firewall]

- name: NFS | Consultar puerto 2049/tcp en firewalld
  ansible.builtin.command: "firewall-cmd --permanent --query-port=2049/tcp"
  register: _nfs_firewalld_port
  changed_when: false
  failed_when: _nfs_firewalld_port.rc not in [0, 1]
  when:
    - nfs_hpc_server_enabled | bool
    - nfs_hpc_firewall_manage | bool
    - _nfs_firewalld_active.rc == 0
  tags: [nfs, nfs_firewall]

- name: NFS | Abrir puerto 2049/tcp en firewalld
  ansible.builtin.command: "firewall-cmd --permanent --add-port=2049/tcp"
  when:
    - nfs_hpc_server_enabled | bool
    - nfs_hpc_firewall_manage | bool
    - _nfs_firewalld_active.rc == 0
    - _nfs_firewalld_port.rc == 1
  notify: NFS | Recargar firewalld
  tags: [nfs, nfs_firewall]

- name: NFS | Instalar paquetes del cliente
  ansible.builtin.package:
    name: "{{ nfs_hpc_client_packages.get(nfs_hpc_os_family, nfs_hpc_client_packages['RedHat']) }}"
    state: present
  when:
    - nfs_hpc_client_enabled | bool
    - not (nfs_hpc_server_enabled | bool)
  tags: [nfs, nfs_client]

- name: NFS | Verificar si el punto de montaje ya está montado (cliente)
  ansible.builtin.command: "mountpoint -q {{ nfs_hpc_mount_point }}"
  register: _nfs_mountpoint
  changed_when: false
  failed_when: false
  when:
    - nfs_hpc_client_enabled | bool
    - not (nfs_hpc_server_enabled | bool)
  tags: [nfs, nfs_client]

- name: NFS | Crear punto de montaje en cliente
  ansible.builtin.file:
    path: "{{ nfs_hpc_mount_point }}"
    state: directory
    owner: root
    group: root
    mode: "0755"
  when:
    - nfs_hpc_client_enabled | bool
    - not (nfs_hpc_server_enabled | bool)
    - _nfs_mountpoint.rc != 0
  tags: [nfs, nfs_client]

- name: NFS | Montar share en cliente
  ansible.builtin.mount:
    path: "{{ nfs_hpc_mount_point }}"
    src: "{{ nfs_hpc_server_host }}:{{ nfs_hpc_share_dir }}"
    fstype: "{{ nfs_hpc_fstype }}"
    opts: "{{ nfs_hpc_mount_opts }}"
    state: mounted
  when:
    - nfs_hpc_client_enabled | bool
    - not (nfs_hpc_server_enabled | bool)
  tags: [nfs, nfs_client]
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.32 roles/nvidia_cuda/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/nvidia_cuda/tasks/main.yml
```
**Salida**
```text
---
- name: NVIDIA/CUDA | Verificar binario lspci
  ansible.builtin.stat:
    path: /usr/sbin/lspci
  register: _lspci_bin
  when: ansible_facts['os_family'] == 'RedHat'

- name: NVIDIA/CUDA | Instalar pciutils si falta
  ansible.builtin.dnf:
    name: pciutils
    state: present
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - not _lspci_bin.stat.exists

- name: NVIDIA/CUDA | Verificar binario lspci (Ubuntu)
  ansible.builtin.stat:
    path: /usr/bin/lspci
  register: _lspci_bin_ubuntu
  when: ansible_facts['os_family'] == 'Debian'

- name: NVIDIA/CUDA | Instalar pciutils si falta (Ubuntu)
  ansible.builtin.apt:
    name: pciutils
    state: present
    update_cache: true
  when:
    - ansible_facts['os_family'] == 'Debian'
    - not _lspci_bin_ubuntu.stat.exists

- name: NVIDIA/CUDA | Detectar GPU NVIDIA
  ansible.builtin.command: "lspci -nn -d 10de:"
  register: _nvidia_lspci
  changed_when: false
  failed_when: false

- name: NVIDIA/CUDA | Definir presencia de GPU
  ansible.builtin.set_fact:
    _nvidia_gpu_present: "{{ _nvidia_lspci.rc == 0 and (_nvidia_lspci.stdout | trim) != '' }}"

- name: NVIDIA/CUDA | Informar sin GPU y omitir rol
  ansible.builtin.debug:
    msg: "No se detecta GPU NVIDIA (vendor 10de). Se omite el rol nvidia_cuda en este host."
  when: not _nvidia_gpu_present

- name: NVIDIA/CUDA | Saltar host sin GPU
  ansible.builtin.meta: end_host
  when: not _nvidia_gpu_present

- name: NVIDIA/CUDA | Capturar nombre de GPU
  ansible.builtin.set_fact:
    _nvidia_gpu_name: >-
      {{
        (
          (_nvidia_lspci.stdout_lines | first | default(''))
          | regex_search('\\[[^\\]]+\\]$')
        )
        | default((_nvidia_lspci.stdout_lines | first) | default('desconocido'), true)
        | regex_replace('^\\[|\\]$', '')
      }}
  when: _nvidia_gpu_present

- name: NVIDIA/CUDA | Asegurar repo CUDA (RHEL9)
  ansible.builtin.get_url:
    url: "{{ nvidia_cuda_repo_url }}"
    dest: "{{ nvidia_cuda_repo_file }}"
    mode: "0644"
  register: _cuda_repo_file
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - nvidia_cuda_repo_enabled | bool

- name: NVIDIA/CUDA | Asegurar module_hotfixes=1 en repo CUDA
  ansible.builtin.lineinfile:
    path: "{{ nvidia_cuda_repo_file }}"
    regexp: '^module_hotfixes='
    line: 'module_hotfixes=1'
    insertafter: '^\\[cuda-rhel9-x86_64\\]$'
  register: _cuda_repo_hotfix
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - nvidia_cuda_repo_enabled | bool

- name: NVIDIA/CUDA | Refrescar cache DNF si repo cambia
  ansible.builtin.dnf:
    update_cache: true
  changed_when: false
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - nvidia_cuda_repo_enabled | bool
    - _cuda_repo_file is changed or _cuda_repo_hotfix is changed

- name: NVIDIA/CUDA | Asegurar keyring CUDA (Ubuntu)
  ansible.builtin.get_url:
    url: "{{ nvidia_cuda_repo_ubuntu_key_url }}"
    dest: "{{ nvidia_cuda_repo_ubuntu_keyring }}"
    mode: "0644"
  register: _cuda_repo_key_ubuntu
  when:
    - ansible_facts['os_family'] == 'Debian'
    - nvidia_cuda_repo_enabled | bool

- name: NVIDIA/CUDA | Asegurar pin CUDA (Ubuntu)
  ansible.builtin.get_url:
    url: "{{ nvidia_cuda_repo_ubuntu_pin_url }}"
    dest: "{{ nvidia_cuda_repo_ubuntu_pin_file }}"
    mode: "0644"
  register: _cuda_repo_pin_ubuntu
  when:
    - ansible_facts['os_family'] == 'Debian'
    - nvidia_cuda_repo_enabled | bool

- name: NVIDIA/CUDA | Asegurar repo CUDA (Ubuntu)
  ansible.builtin.copy:
    dest: "{{ nvidia_cuda_repo_file_ubuntu }}"
    mode: "0644"
    content: "deb [signed-by={{ nvidia_cuda_repo_ubuntu_keyring }}] {{ nvidia_cuda_repo_ubuntu_baseurl }} /"
  register: _cuda_repo_file_ubuntu
  when:
    - ansible_facts['os_family'] == 'Debian'
    - nvidia_cuda_repo_enabled | bool

- name: NVIDIA/CUDA | Refrescar cache APT si repo cambia
  ansible.builtin.apt:
    update_cache: true
  changed_when: false
  when:
    - ansible_facts['os_family'] == 'Debian'
    - nvidia_cuda_repo_enabled | bool
    - _cuda_repo_key_ubuntu is changed or _cuda_repo_pin_ubuntu is changed or _cuda_repo_file_ubuntu is changed

- name: NVIDIA/CUDA | Verificar stream habilitado de nvidia-driver
  ansible.builtin.command: dnf -q module list --enabled nvidia-driver
  register: _nvidia_module_enabled
  changed_when: false
  failed_when: false
  when: ansible_facts['os_family'] == 'RedHat'

- name: NVIDIA/CUDA | Evaluar stream requerido
  ansible.builtin.set_fact:
    _nvidia_module_stream_ok: "{{ nvidia_driver_stream in (_nvidia_module_enabled.stdout | default('')) }}"
  when: ansible_facts['os_family'] == 'RedHat'

- name: NVIDIA/CUDA | Resetear stream si no coincide
  ansible.builtin.command: dnf -y module reset nvidia-driver
  register: _nvidia_module_reset
  changed_when: "'Nothing to do' not in (_nvidia_module_reset.stdout ~ _nvidia_module_reset.stderr)"
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - not _nvidia_module_stream_ok

- name: NVIDIA/CUDA | Cambiar a stream fijado {{ nvidia_driver_stream }}
  ansible.builtin.command: dnf -y module switch-to nvidia-driver:{{ nvidia_driver_stream }} --allowerasing
  register: _nvidia_module_switch
  changed_when: "'Nothing to do' not in (_nvidia_module_switch.stdout ~ _nvidia_module_switch.stderr)"
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - not _nvidia_module_stream_ok

- name: NVIDIA/CUDA | Instalar prerequisitos de compilacion
  ansible.builtin.dnf:
    name: "{{ nvidia_cuda_prereq_packages }}"
    state: present
  register: _nvidia_prereqs
  when: ansible_facts['os_family'] == 'RedHat'

- name: NVIDIA/CUDA | Instalar headers/devel del kernel actual (best effort)
  ansible.builtin.dnf:
    name:
      - "kernel-devel-{{ ansible_kernel }}"
      - "kernel-headers-{{ ansible_kernel }}"
    state: present
  register: _nvidia_kernel_specific
  ignore_errors: true
  when: ansible_facts['os_family'] == 'RedHat'

- name: NVIDIA/CUDA | Fallback a headers/devel genericos si faltan
  ansible.builtin.dnf:
    name:
      - kernel-devel
      - kernel-headers
    state: present
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - _nvidia_kernel_specific is failed

- name: NVIDIA/CUDA | Instalar prerequisitos de compilacion (Ubuntu)
  ansible.builtin.apt:
    name: "{{ nvidia_cuda_prereq_packages_ubuntu }}"
    state: present
    update_cache: true
  register: _nvidia_prereqs
  when: ansible_facts['os_family'] == 'Debian'

- name: NVIDIA/CUDA | Configurar DKMS para usar gcc-12 (Ubuntu)
  ansible.builtin.lineinfile:
    path: /etc/dkms/framework.conf
    regexp: '^CC='
    line: 'CC=/usr/bin/gcc-12'
    create: true
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.33 roles/slurm_compute/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/slurm_compute/tasks/main.yml
```
**Salida**
```text
---
- name: Slurm | Gather service facts (compute)
  ansible.builtin.service_facts:
  tags: [slurm, slurmd]

- name: Slurm | Decide whether to manage slurmd on this host (compute)
  ansible.builtin.set_fact:
    slurm_manage_slurmd: >-
      {{
        ('slurmd.service' in (ansible_facts.services | default({}))) or
        ('slurmd' in (ansible_facts.services | default({})))
      }}
  tags: [slurm, slurmd]

- name: Slurm | Skip slurmd management if unit is absent (compute)
  ansible.builtin.debug:
    msg: "slurmd.service no existe en este nodo todavía; se omite start/restart (esperable en Ubuntu sin paquetes)."
  when: not (slurm_manage_slurmd | bool)
  tags: [slurm, slurmd]

- name: Slurm | Ensure log dir exists (compute)
  ansible.builtin.file:
    path: "{{ slurm_log_dir }}"
    state: directory
    owner: slurm
    group: slurm
    mode: "0755"
  tags: [slurm, slurm_config]

- name: Slurm | Ensure slurmd spool dir exists (compute)
  ansible.builtin.file:
    path: /var/spool/slurmd
    state: directory
    owner: slurm
    group: slurm
    mode: "0755"
  tags: [slurm, slurm_config]

- name: Slurm | Touch slurmd log (compute)
  ansible.builtin.file:
    path: "{{ slurm_log_dir }}/slurmd.log"
    state: touch
    owner: slurm
    group: slurm
    mode: "0644"
  tags: [slurm, slurm_config]

- name: Slurm | Reload systemd units (compute)
  ansible.builtin.systemd:
    daemon_reload: true
  tags: [slurm, slurmd]

- name: Slurm | Enable and start slurmd (compute)
  ansible.builtin.systemd:
    name: slurmd
    enabled: true
    state: started
  when: slurm_manage_slurmd | bool
  tags: [slurm, slurmd]

- name: Slurm | Restart slurmd si cambia config o NVML (compute)
  ansible.builtin.systemd:
    name: slurmd
    state: restarted
    no_block: true
  when:
    - slurm_manage_slurmd | bool
    - (slurm_conf_changed | default(false)) or (slurm_gres_conf_changed | default(false)) or (slurm_nvml_symlink_changed | default(false))
  tags: [slurm, slurmd]

- name: Slurm | Verificar slurmd activo (compute)
  ansible.builtin.command: systemctl is-active slurmd
  register: _slurmd_active
  changed_when: false
  failed_when: (_slurmd_active.stdout | trim) != 'active'
  when: slurm_manage_slurmd | bool
  tags: [slurm, slurmd]
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.34 roles/slurm_controller/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/slurm_controller/tasks/main.yml
```
**Salida**
```text
---
- name: Slurm | Ensure log dir exists (master)
  ansible.builtin.file:
    path: "{{ slurm_log_dir }}"
    state: directory
    owner: slurm
    group: slurm
    mode: "0755"
  tags: [slurm, slurm_config]

- name: Slurm | Ensure slurmctld spool dir exists (master)
  ansible.builtin.file:
    path: /var/spool/slurmctld
    state: directory
    owner: slurm
    group: slurm
    mode: "0755"
  tags: [slurm, slurm_config]

- name: Slurm | Touch controller/db logs (master)
  ansible.builtin.file:
    path: "{{ item }}"
    state: touch
    owner: slurm
    group: slurm
    mode: "0644"
  loop:
    - "{{ slurm_log_dir }}/slurmctld.log"
    - "{{ slurm_log_dir }}/slurm_jobacct.log"
    - "{{ slurm_log_dir }}/slurm_jobcomp.log"
    - "{{ slurm_log_dir }}/slurmdbd.log"
  tags: [slurm, slurm_config]

- name: Slurm | Install slurmdbd.conf (master)
  ansible.builtin.template:
    src: slurmdbd.conf.j2
    dest: /etc/slurm/slurmdbd.conf
    owner: slurm
    group: slurm
    mode: "0600"
  register: _slurmdbd_conf
  tags: [slurm, slurmdbd]

- name: Slurm | Enable and start slurmdbd (master)
  ansible.builtin.systemd:
    name: slurmdbd
    enabled: true
    state: started
  tags: [slurm, slurmdbd]

- name: Slurm | Restart slurmdbd if config changed (master)
  ansible.builtin.systemd:
    name: slurmdbd
    state: restarted
  when: _slurmdbd_conf.changed
  tags: [slurm, slurmdbd]

- name: Slurm | Enable and start slurmctld (master)
  ansible.builtin.systemd:
    name: slurmctld
    enabled: true
    state: started
  tags: [slurm, slurmctld]

- name: Slurm | Restart slurmctld if slurm.conf changed (master)
  ansible.builtin.systemd:
    name: slurmctld
    state: restarted
  when: slurm_conf_changed | default(false)
  tags: [slurm, slurmctld]

- name: Slurm | Reconfigurar controlador al finalizar configuracion (master)
  ansible.builtin.command: scontrol reconfigure
  changed_when: false
  become: true
  when:
    - slurm_controller_reconfigure_on_change | bool
    - slurm_controller_reconfigure_always | default(false) or
      (slurm_conf_changed | default(false)) or
      (slurm_gres_conf_changed | default(false)) or
      (slurm_nvml_symlink_changed | default(false))
  tags: [slurm]

- name: Slurm | Obtener estado de nodos (master)
  ansible.builtin.command: scontrol show node -o
  register: _slurm_nodes
  changed_when: false
  become: true
  when:
    - slurm_controller_autoresume_enabled | bool
    - (slurm_conf_changed | default(false)) or (slurm_gres_conf_changed | default(false)) or (slurm_nvml_symlink_changed | default(false))
  tags: [slurm]

- name: Slurm | Determinar nodos a reanudar por GRES (master)
  ansible.builtin.set_fact:
    slurm_nodes_to_resume: >-
      {%- set nodes = [] -%}
      {%- for line in _slurm_nodes.stdout_lines | default([]) -%}
      {%- set name = (line | regex_findall('NodeName=([^ ]+)') | first | default('')) -%}
      {%- set state = (line | regex_findall('State=([^ ]+)') | first | default('')) -%}
      {%- set reason = (line | regex_findall('Reason=([^ ]+)') | first | default('')) -%}
      {%- if name and state -%}
      {%- set state_tokens = state.split('+') -%}
      {%- if (state_tokens | intersect(slurm_controller_autoresume_states | default([]))) | length > 0 -%}
      {%- set reason_ok = true -%}
      {%- if (slurm_controller_autoresume_reason_regex | default('') | length) > 0 -%}
      {%- set reason_ok = (reason is match(slurm_controller_autoresume_reason_regex)) -%}
      {%- endif -%}
      {%- if reason_ok -%}
      {%- set _ = nodes.append(name) -%}
      {%- endif -%}
      {%- endif -%}
      {%- endif -%}
      {%- endfor -%}
      {{ nodes | unique }}
  when:
    - slurm_controller_autoresume_enabled | bool
    - (slurm_conf_changed | default(false)) or (slurm_gres_conf_changed | default(false)) or (slurm_nvml_symlink_changed | default(false))
  tags: [slurm]

- name: Slurm | Reanudar nodos con GRES corregido (master)
  ansible.builtin.command: "scontrol update NodeName={{ item }} State=resume"
  become: true
  loop: "{{ slurm_nodes_to_resume | default([]) }}"
  when:
    - slurm_controller_autoresume_enabled | bool
    - (slurm_conf_changed | default(false)) or (slurm_gres_conf_changed | default(false)) or (slurm_nvml_symlink_changed | default(false))
    - (slurm_nodes_to_resume | default([]) | length) > 0
  tags: [slurm]
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.35 roles/slurm_db_prep/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/slurm_db_prep/tasks/main.yml
```
**Salida**
```text
---
- name: SlurmDB | Ensure MariaDB tuning file
  ansible.builtin.copy:
    dest: /etc/my.cnf.d/slurm.cnf
    owner: root
    group: root
    mode: "0644"
    content: |
      [mysqld]
      innodb_buffer_pool_size={{ mariadb_slurm_tuning.innodb_buffer_pool_size }}
      innodb_log_file_size={{ mariadb_slurm_tuning.innodb_log_file_size }}
      innodb_lock_wait_timeout={{ mariadb_slurm_tuning.innodb_lock_wait_timeout }}
      max_allowed_packet={{ mariadb_slurm_tuning.max_allowed_packet }}
  notify: Restart mariadb
  tags: [mariadb, slurmdb]

- name: SlurmDB | Create database
  ansible.builtin.command: >-
    mariadb -N -B -e "CREATE DATABASE IF NOT EXISTS {{ slurmdb_mysql_db }};"
  changed_when: false
  tags: [mariadb, slurmdb]

- name: SlurmDB | Create users
  ansible.builtin.command: >-
    mariadb -N -B -e "CREATE USER IF NOT EXISTS '{{ item.0 }}'@'{{ item.1 }}' IDENTIFIED BY '{{ slurmdb_mysql_password }}';"
  loop: "{{ (slurmdb_mysql_user | list) | product(slurmdb_mysql_hosts | unique) | list }}"
  changed_when: false
  no_log: true
  tags: [mariadb, slurmdb]

- name: SlurmDB | Grant privileges
  ansible.builtin.command: >-
    mariadb -N -B -e "GRANT ALL PRIVILEGES ON {{ slurmdb_mysql_db }}.* TO '{{ item.0 }}'@'{{ item.1 }}' WITH GRANT OPTION;"
  loop: "{{ (slurmdb_mysql_user | list) | product(slurmdb_mysql_hosts | unique) | list }}"
  changed_when: false
  tags: [mariadb, slurmdb]

- name: SlurmDB | Flush privileges
  ansible.builtin.command: mariadb -N -B -e "FLUSH PRIVILEGES;"
  changed_when: false
  tags: [mariadb, slurmdb]

- name: SlurmDB | Verify innodb_buffer_pool_size
  ansible.builtin.command: mariadb -N -B -e "SHOW VARIABLES LIKE 'innodb_buffer_pool_size';"
  register: slurmdb_verify_buffer
  changed_when: false
  tags: [verify]

- name: Verify | Slurm DB exists and grants are readable
  ansible.builtin.command: >
    mariadb -u {{ (slurmdb_mysql_user | list | first | default('slurm')) }} -p{{ slurmdb_mysql_password }} -N -B -e "SHOW DATABASES LIKE '{{ slurmdb_mysql_db }}'; SHOW GRANTS;"
  register: _slurmdb_verify
  changed_when: false
  no_log: true
  tags: [verify, mariadb, slurmdb]
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.36 roles/slurm_facts/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/slurm_facts/tasks/main.yml
```
**Salida**
```text
---
- name: Slurm facts | Default memory reserve (MB)
  ansible.builtin.set_fact:
    slurm_mem_reserve_mb: "{{ slurm_mem_reserve_mb | default(1024) | int }}"
  tags: [slurm, slurm_facts, slurm_config]

- name: Slurm facts | Set node identity + CPU + RealMemory
  ansible.builtin.set_fact:
    slurm_node_name: "{{ slurm_node_name | default(inventory_hostname) }}"
    slurm_cpus: "{{ slurm_cpus | default(_computed_cpus, true) }}"
    slurm_sockets: "{{ slurm_sockets | default(_computed_sockets, true) }}"
    slurm_cores_per_socket: "{{ slurm_cores_per_socket | default(_computed_cores, true) }}"
    slurm_threads_per_core: "{{ slurm_threads_per_core | default(_computed_threads, true) }}"
    slurm_real_memory: "{{ slurm_real_memory | default(_computed_real_memory, true) }}"
  vars:
    _computed_cpus: >-
      {{
        (ansible_facts.processor_vcpus | default(
          (ansible_facts.processor_count | int) *
          (ansible_facts.processor_cores | int) *
          (ansible_facts.processor_threads_per_core | default(1) | int)
        )) | default(1) | int
      }}
    _computed_sockets: "{{ ansible_facts.processor_count | default(1) | int }}"
    _computed_cores: "{{ ansible_facts.processor_cores | default(1) | int }}"
    _computed_threads: "{{ ansible_facts.processor_threads_per_core | default(1) | int }}"
    _computed_real_memory: "{{ [ (ansible_facts.memtotal_mb | int) - (slurm_mem_reserve_mb | int), 1024 ] | max }}"

- name: Slurm facts | Consultar modelos de GPU con NVML (nvidia-smi)
  ansible.builtin.command: nvidia-smi --query-gpu=name --format=csv,noheader
  register: _nvidia_smi_names
  changed_when: false
  failed_when: false
  tags: [slurm, slurm_facts, slurm_config]

- name: Slurm facts | Normalizar lista de modelos de GPU
  ansible.builtin.set_fact:
    slurm_gpu_names: "{{ _gpu_names }}"
    slurm_gpu_count: "{{ _gpu_names | length }}"
  vars:
    _gpu_names: >-
      {{
        _nvidia_smi_names.stdout_lines
        | default([])
        | map('trim')
        | reject('equalto', '')
        | list
      }}
  tags: [slurm, slurm_facts, slurm_config]

- name: Slurm facts | Normalizar tipo NVML de GPU
  ansible.builtin.set_fact:
    slurm_gpu_type_nvml: >-
      {{
        (
          (slurm_gpu_names | default([]) | first | default(''))
          | lower
          | regex_replace('[^a-z0-9]+', '_')
          | regex_replace('^_+|_+$', '')
        ) | default('gpu', true)
      }}
  when: slurm_gpu_count | int > 0
  tags: [slurm, slurm_facts, slurm_config]

- name: Slurm facts | Derivar tipos cortos de GPU
  ansible.builtin.set_fact:
    slurm_gpu_types_short: "{{ slurm_gpu_names | default([]) | map('lower') | map('regex_findall', '([a-z]{1,3}\\\\d{1,4}[a-z]?|\\\\d{3,4})') | map('first') | map('default', 'gpu') | list }}"
  tags: [slurm, slurm_facts, slurm_config]

- name: Slurm facts | Definir tipo corto del nodo (mixed si aplica)
  ansible.builtin.set_fact:
    slurm_gpu_type_short: >-
      {{
        (slurm_gpu_types_short | unique | length > 1)
        | ternary('mixed', (slurm_gpu_types_short | first | default('gpu')))
      }}
  tags: [slurm, slurm_facts, slurm_config]

- name: Slurm facts | Definir GRES desde NVML
  ansible.builtin.set_fact:
    slurm_node_gres: "{{ slurm_node_gres | default('gpu:' ~ (slurm_gpu_type_nvml | default('gpu')) ~ ':' ~ slurm_gpu_count, true) }}"
  when: slurm_gpu_count | int > 0
  tags: [slurm, slurm_facts, slurm_config]

- name: Slurm facts | Limpiar GRES si no hay GPU
  ansible.builtin.set_fact:
    slurm_node_gres: "{{ slurm_node_gres | default('', true) }}"
  when: slurm_gpu_count | int == 0
  tags: [slurm, slurm_facts, slurm_config]

- name: Slurm facts | Advertir mezcla de modelos en el nodo
  ansible.builtin.debug:
    msg: >-
      GPUs mixtas detectadas en el nodo: {{ slurm_gpu_names | unique }}.
      Tipos cortos: {{ slurm_gpu_types_short | unique }}.
  when: slurm_gpu_types_short | unique | length > 1
  tags: [slurm, slurm_facts, slurm_config]
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.37 roles/slurm_identities/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/slurm_identities/tasks/main.yml
```
**Salida**
```text
- name: Choose nologin shell (varies by distro)
  ansible.builtin.set_fact:
    nologin_shell: "{{ '/usr/sbin/nologin' if (ansible_facts['distribution'] in ['Ubuntu', 'Debian']) else '/sbin/nologin' }}"

- name: Ensure munge group exists
  ansible.builtin.group:
    name: munge
    gid: "{{ munge_gid }}"
    state: present

- name: Ensure munge user exists
  ansible.builtin.user:
    name: munge
    comment: "MUNGE Uid 'N' Gid Emporium"
    uid: "{{ munge_uid }}"
    group: munge
    home: /var/lib/munge
    create_home: true
    shell: "{{ nologin_shell }}"
    state: present

- name: Ensure slurm group exists
  ansible.builtin.group:
    name: slurm
    gid: "{{ slurm_gid }}"
    state: present

- name: Ensure slurm user exists
  ansible.builtin.user:
    name: slurm
    comment: "SLURM workload manager"
    uid: "{{ slurm_uid }}"
    group: slurm
    home: /var/lib/slurm
    create_home: true
    shell: /bin/bash
    state: present
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.38 roles/slurm_install/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/slurm_install/tasks/main.yml
```
**Salida**
```text
---
- name: Slurm | See locally built RPMs (Rocky/RHEL)
  ansible.builtin.shell: "ls -1 /root/rpmbuild/RPMS/x86_64/*.rpm | grep -v '/slurm-openlava-'"
  register: _slurm_rpms
  changed_when: false
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - inventory_hostname in groups.get('hpc_master', [])
  tags: [slurm, slurm_install]

- name: Slurm | Install RPMs (Rocky/RHEL)
  ansible.builtin.dnf:
    name: "{{ _slurm_rpms.stdout_lines }}"
    state: present
    disable_gpg_check: true
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - inventory_hostname in groups.get('hpc_master', [])
    - _slurm_rpms.stdout_lines | length > 0
  tags: [slurm, slurm_install]

- name: Slurm | Ensure local RPM cache dir exists (controller)
  ansible.builtin.file:
    path: "{{ slurm_rpm_cache_dir }}"
    state: directory
    owner: "{{ lookup('env', 'USER') | default('sistemas', true) }}"
    group: "{{ lookup('env', 'USER') | default('sistemas', true) }}"
    mode: "0755"
  delegate_to: localhost
  run_once: true
  when: ansible_facts['os_family'] == 'RedHat'
  tags: [slurm, slurm_install]

- name: Slurm | Find built RPMs on master (Rocky/RHEL)
  ansible.builtin.find:
    paths: "{{ slurm_rpm_source_dir }}"
    patterns: "*.rpm"
    file_type: file
  register: _slurm_rpm_find
  changed_when: false
  delegate_to: "{{ groups['hpc_master'][0] }}"
  run_once: true
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - groups.get('hpc_master', []) | length > 0
  tags: [slurm, slurm_install]

- name: Slurm | Fetch RPMs to controller cache (Rocky/RHEL)
  ansible.builtin.fetch:
    src: "{{ item.path }}"
    dest: "{{ slurm_rpm_cache_dir }}/"
    flat: true
  loop: "{{ _slurm_rpm_find.files | rejectattr('path', 'search', '/slurm-openlava-') | list }}"
  delegate_to: "{{ groups['hpc_master'][0] }}"
  run_once: true
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - groups.get('hpc_master', []) | length > 0
    - _slurm_rpm_find is defined
  tags: [slurm, slurm_install]

- name: Slurm | Ensure RPM staging dir exists (workers)
  ansible.builtin.file:
    path: "{{ slurm_rpm_staging_dir }}"
    state: directory
    mode: "0755"
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - inventory_hostname not in groups.get('hpc_master', [])
  tags: [slurm, slurm_install]

- name: Slurm | Copy RPMs to workers (Rocky/RHEL)
  ansible.builtin.copy:
    src: "{{ item }}"
    dest: "{{ slurm_rpm_staging_dir }}/{{ item | basename }}"
    mode: "0644"
  with_fileglob:
    - "{{ slurm_rpm_cache_dir }}/*.rpm"
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - inventory_hostname not in groups.get('hpc_master', [])
  tags: [slurm, slurm_install]

- name: Slurm | List RPMs staged on workers (Rocky/RHEL)
  ansible.builtin.find:
    paths: "{{ slurm_rpm_staging_dir }}"
    patterns: "*.rpm"
    file_type: file
  register: _slurm_worker_rpms
  changed_when: false
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - inventory_hostname not in groups.get('hpc_master', [])
  tags: [slurm, slurm_install]

- name: Slurm | Build worker RPM list from staging (Rocky/RHEL)
  ansible.builtin.set_fact:
    slurm_worker_rpms: "{{ _slurm_worker_rpms.files | map(attribute='path') | list }}"
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - inventory_hostname not in groups.get('hpc_master', [])
    - _slurm_worker_rpms is defined
  tags: [slurm, slurm_install]

- name: Slurm | Install RPMs on workers (Rocky/RHEL)
  ansible.builtin.dnf:
    name: "{{ slurm_worker_rpms }}"
    state: present
    disable_gpg_check: true
    disable_excludes: all
    update_cache: true
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - inventory_hostname not in groups.get('hpc_master', [])
    - slurm_worker_rpms | length > 0
  tags: [slurm, slurm_install]

- name: Slurm | Verify slurmd package installed (workers)
  ansible.builtin.command: rpm -q slurm-slurmd
  register: _slurm_slurmd_rpm
  changed_when: false
  failed_when: _slurm_slurmd_rpm.rc != 0
  when:
    - ansible_facts['os_family'] == 'RedHat'
    - inventory_hostname not in groups.get('hpc_master', [])
  tags: [slurm, slurm_install]

- name: Slurm | Install packages (Debian/Ubuntu) [disabled by default]
  ansible.builtin.apt:
    name: >-
      {{
        (inventory_hostname in groups.get('hpc_master', []))
          | ternary(
              (slurm_debian_master_packages | default(['slurmctld','slurmdbd','slurmd','slurm-client'])),
              (slurm_debian_worker_packages | default(['slurmd','slurm-client']))
            )
      }}
    state: present
    update_cache: true
  when:
    - ansible_facts['os_family'] == 'Debian'
    - slurm_debian_enable | default(false)
  tags: [slurm, slurm_install]


- name: Slurm | Ensure /etc/slurm exists
  ansible.builtin.file:
    path: "{{ slurm_etc_dir }}"
    state: directory
    owner: root
    group: root
    mode: "0755"
  tags: [slurm, slurm_config]

- name: Slurm | Install cgroup.conf
  ansible.builtin.copy:
    dest: "{{ slurm_etc_dir }}/cgroup.conf"
    owner: root
    group: root
    mode: "0644"
    content: "{{ slurm_cgroup_conf }}"
  tags: [slurm, slurm_config]

- name: Slurm | Fallback per-host facts for templating
  ansible.builtin.set_fact:
    slurm_node_name: "{{ inventory_hostname }}"
    slurm_cpus: "{{ ansible_facts.processor_vcpus | default(1) | int }}"
    slurm_sockets: "{{ ansible_facts.processor_count | default(1) | int }}"
    slurm_cores_per_socket: "{{ ansible_facts.processor_cores | default(1) | int }}"
    slurm_threads_per_core: "{{ ansible_facts.processor_threads_per_core | default(1) | int }}"
    slurm_real_memory: "{{ [ (ansible_facts.memtotal_mb | default(2048) | int) - (slurm_mem_reserve_mb | default(1024) | int), 1024 ] | max }}"
  when: >
    slurm_node_name is not defined or
    slurm_cpus is not defined or
    slurm_real_memory is not defined or
    slurm_sockets is not defined or
    slurm_cores_per_socket is not defined or
    slurm_threads_per_core is not defined
  tags: [slurm, slurm_facts]

- name: Slurm | Check firewalld is active (controller)
  ansible.builtin.command: systemctl is-active firewalld
  register: _firewalld_active
  changed_when: false
  failed_when: false
  when: inventory_hostname in groups.get('hpc_master', [])
  tags: [slurm, slurm_firewall]

- name: Slurm | Allow SrunPortRange on controller firewall (firewalld)
  ansible.builtin.command: "firewall-cmd --permanent --query-port={{ slurm_srun_port_range }}/tcp"
  register: _srun_port_query
  changed_when: false
  failed_when: false
  when:
    - inventory_hostname in groups.get('hpc_master', [])
    - _firewalld_active.rc == 0
  tags: [slurm, slurm_firewall]

- name: Slurm | Add SrunPortRange to controller firewall (firewalld)
  ansible.builtin.command: "firewall-cmd --permanent --add-port={{ slurm_srun_port_range }}/tcp"
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.39 roles/slurm_rpm_build/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/slurm_rpm_build/tasks/main.yml
```
**Salida**
```text
---
- name: Slurm | Install build deps (Rocky/RHEL)
  ansible.builtin.dnf:
    name:
      - rpm-build
      - wget
      - perl
      - python3
      - pam-devel
      - dbus-devel
      - readline-devel
      - hwloc-devel
      - munge-devel
      - mariadb-devel
    state: present
  when: ansible_facts['os_family'] == 'RedHat'
  tags: [slurm, slurm_build]

- name: Slurm | Download tarball (Rocky/RHEL)
  ansible.builtin.get_url:
    url: "{{ slurm_tarball_url }}"
    dest: "/root/slurm-{{ slurm_version }}.tar.bz2"
    mode: "0644"
  when: ansible_facts['os_family'] == 'RedHat'
  tags: [slurm, slurm_build]

- name: Slurm | Build RPMs with rpmbuild (Rocky/RHEL)
  ansible.builtin.command: "rpmbuild -ta /root/slurm-{{ slurm_version }}.tar.bz2"
  args:
    creates: "/root/rpmbuild/RPMS/x86_64/.slurm_{{ slurm_version }}_built"
  when: ansible_facts['os_family'] == 'RedHat'
  tags: [slurm, slurm_build]

- name: Slurm | Mark RPM build complete (Rocky/RHEL)
  ansible.builtin.file:
    path: "/root/rpmbuild/RPMS/x86_64/.slurm_{{ slurm_version }}_built"
    state: touch
  when: ansible_facts['os_family'] == 'RedHat'
  tags: [slurm, slurm_build]
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.40 roles/slurm_validate/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/slurm_validate/tasks/main.yml
```
**Salida**
```text
---
# Nota: este rol asume que corre en el master (controller) para ejecutar sinfo/srun/sbatch.
# No cambia configuración. Todo es "changed_when: false".

- name: Validar CLI de Slurm (sinfo)
  ansible.builtin.command: sinfo --version
  register: _sinfo_ver
  changed_when: false
  tags: [slurm_validate]

- name: Listar particiones (normalizado)
  ansible.builtin.shell: |
    set -euo pipefail
    sinfo -h -o "%P" | tr -d '*' | tr ' ' '\n' | sed '/^$/d' | sort -u
  args:
    executable: /bin/bash
  register: _parts
  changed_when: false
  tags: [slurm_validate]

- name: Verificar particion CPU
  ansible.builtin.assert:
    that:
      - slurm_validate_partitions.cpu in _parts.stdout_lines
    fail_msg: "Missing CPU partition '{{ slurm_validate_partitions.cpu }}'. Got: {{ _parts.stdout_lines }}"
  tags: [slurm_validate]

- name: Verificar particion GPU
  ansible.builtin.assert:
    that:
      - slurm_validate_partitions.gpu in _parts.stdout_lines
    fail_msg: "Missing GPU partition '{{ slurm_validate_partitions.gpu }}'. Got: {{ _parts.stdout_lines }}"
  tags: [slurm_validate]

- name: Obtener estados de nodos (basico)
  ansible.builtin.command: sinfo -N -h -o "%N %t"
  register: _node_states
  changed_when: false
  failed_when: _node_states.rc != 0
  tags: [slurm_validate]

- name: Asegurar que no hay nodos DOWN/DRAIN/FAIL (basico)
  ansible.builtin.shell: |
    set -euo pipefail
    printf '%s\n' "{{ _node_states.stdout | default('') }}" | awk '{print $2}' | egrep -i 'down|drain|fail'
  args:
    executable: /bin/bash
  register: _bad_states
  changed_when: false
  failed_when: _bad_states.rc == 0
  tags: [slurm_validate]

- name: srun hostname (particion CPU)
  ansible.builtin.command: >
    srun -N1 -n1 -p {{ slurm_validate_partitions.cpu }} hostname
  register: _srun_cpu_hostname
  changed_when: false
  tags: [slurm_validate]

- name: srun nvidia-smi -L (particion GPU)
  ansible.builtin.command: >
    srun -N1 -n1 -p {{ slurm_validate_partitions.gpu }} --gres=gpu:1 nvidia-smi -L
  register: _srun_gpu_nvsmi_l
  changed_when: false
  tags: [slurm_validate]

- name: Sonda de importacion de Torch en nodo GPU (auto)
  ansible.builtin.command:
    argv:
      - srun
      - -N1
      - -n1
      - -p
      - "{{ slurm_validate_partitions.gpu }}"
      - --gres=gpu:1
      - bash
      - -lc
      - |
          set -euo pipefail
          {{ slurm_validate_torch.prelude }}
          {{ slurm_validate_torch.python }} -c "import torch; print('torch:', torch.__version__)"
  register: _torch_probe
  changed_when: false
  failed_when: false
  when: slurm_validate_torch.enabled in ["auto", "true"]
  tags: [slurm_validate]

- name: Mostrar salida de sonda Torch (auto)
  ansible.builtin.debug:
    msg: |
      torch_probe rc={{ _torch_probe.rc | default('n/a') }}
      stdout:
      {{ _torch_probe.stdout | default('') }}
      stderr:
      {{ _torch_probe.stderr | default('') }}
  when: _torch_probe is defined
  tags: [slurm_validate]

- name: Smoke PyTorch CUDA (solo si sonda OK o enabled=true)
  ansible.builtin.command:
    argv:
      - srun
      - -N1
      - -n1
      - -p
      - "{{ slurm_validate_partitions.gpu }}"
      - --gres=gpu:1
      - bash
      - -lc
      - |
          set -euo pipefail
          {{ slurm_validate_torch.prelude }}
          {{ slurm_validate_torch.python }} -c "import torch; print('torch:', torch.__version__); print('torch.version.cuda:', torch.version.cuda); print('cuda_available:', torch.cuda.is_available()); torch.cuda.is_available() and print('gpu:', torch.cuda.get_device_name(0))"
  register: _torch_smoke
  changed_when: false
  when: >
    slurm_validate_torch.enabled == "true"
    or (slurm_validate_torch.enabled == "auto" and _torch_probe is defined and _torch_probe.rc == 0)
  tags: [slurm_validate]

- name: Mostrar salida de smoke Torch (CUDA)
  ansible.builtin.debug:
    msg: |
      torch_smoke rc={{ _torch_smoke.rc | default('n/a') }}
      stdout:
      {{ _torch_smoke.stdout | default('') }}
      stderr:
      {{ _torch_smoke.stderr | default('') }}
  when: _torch_smoke is defined
  tags: [slurm_validate]

- name: Renderizar scripts smoke (CPU/GPU)
  ansible.builtin.template:
    src: "{{ item.src }}"
    dest: "{{ slurm_validate_smoke.workdir }}/{{ item.dest }}"
    mode: "0755"
  loop:
    - { src: "slurm-smoke-cpu.sbatch.j2", dest: "slurm-smoke-cpu.sbatch" }
    - { src: "slurm-smoke-gpu.sbatch.j2", dest: "slurm-smoke-gpu.sbatch" }
  changed_when: false
  when: slurm_validate_smoke.enabled | bool
  tags: [slurm_validate, slurm_validate_smoke]

- name: Enviar job smoke CPU
  ansible.builtin.command: >
    sbatch --parsable {{ slurm_validate_smoke.workdir }}/slurm-smoke-cpu.sbatch
  register: _cpu_jobid
  changed_when: false
  when: slurm_validate_smoke.enabled | bool
  tags: [slurm_validate, slurm_validate_smoke]

- name: Esperar salida de cola del job CPU
  ansible.builtin.shell: |
    set -euo pipefail
    squeue -h -j {{ _cpu_jobid.stdout }} | wc -l
  args:
    executable: /bin/bash
  register: _cpu_in_queue
  changed_when: false
  until: _cpu_in_queue.stdout | int == 0
  retries: "{{ (slurm_validate_smoke.timeout_seconds // slurm_validate_smoke.poll_delay_seconds) | int }}"
  delay: "{{ slurm_validate_smoke.poll_delay_seconds }}"
  when: slurm_validate_smoke.enabled | bool
  tags: [slurm_validate, slurm_validate_smoke]

- name: Verificar estado sacct del job CPU
  ansible.builtin.shell: |
    set -euo pipefail
    sacct -n -P -j {{ _cpu_jobid.stdout }} -o JobID,State,ExitCode | awk -F'|' '$1=="{{ _cpu_jobid.stdout }}" {print $2"|" $3; exit}'
  args:
    executable: /bin/bash
  register: _cpu_sacct
  changed_when: false
  when: slurm_validate_smoke.enabled | bool
  tags: [slurm_validate, slurm_validate_smoke]

- name: Obtener detalles del job CPU (stdout/stderr/host)
  ansible.builtin.command: "scontrol show job -o {{ _cpu_jobid.stdout | trim }}"
  register: _cpu_job_detail
  changed_when: false
  when: slurm_validate_smoke.enabled | bool
  tags: [slurm_validate, slurm_validate_smoke]

- name: Parsear salida y host del job CPU
  ansible.builtin.set_fact:
    slurm_cpu_job_stdout_path: "{{ _cpu_job_detail.stdout | regex_findall('StdOut=([^ ]+)') | first | default('') }}"
    slurm_cpu_job_stderr_path: "{{ _cpu_job_detail.stdout | regex_findall('StdErr=([^ ]+)') | first | default('') }}"
    slurm_cpu_job_batch_host: "{{ _cpu_job_detail.stdout | regex_findall('BatchHost=([^ ]+)') | first | default('') }}"
  when: slurm_validate_smoke.enabled | bool
  tags: [slurm_validate, slurm_validate_smoke]

- name: Verificar stdout del job CPU en el batch host
  ansible.builtin.stat:
    path: "{{ slurm_cpu_job_stdout_path }}"
  delegate_to: "{{ slurm_cpu_job_batch_host }}"
  register: _cpu_job_out_stat
  changed_when: false
  when:
    - slurm_validate_smoke.enabled | bool
    - slurm_cpu_job_stdout_path | length > 0
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.41 roles/users_ssh/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/users_ssh/tasks/main.yml
```
**Salida**
```text
---
- name: SSH | Ensure sshd service enabled
  ansible.builtin.service:
    name: sshd
    state: started
    enabled: true

# En Rocky/RHEL modernos se usa Include /etc/ssh/sshd_config.d/*.conf
- name: SSH | Ensure sshd_config includes sshd_config.d
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^Include\s+/etc/ssh/sshd_config\.d/\*\.conf$'
    line: 'Include /etc/ssh/sshd_config.d/*.conf'
    insertafter: EOF
    state: present

- name: SSH | Ensure drop-in directory exists
  ansible.builtin.file:
    path: /etc/ssh/sshd_config.d
    state: directory
    owner: root
    group: root
    mode: "0755"

- name: SSH | Write drop-in config (99-hpc.conf)
  ansible.builtin.copy:
    dest: /etc/ssh/sshd_config.d/99-hpc.conf
    owner: root
    group: root
    mode: "0644"
    content: |
      # Managed by Ansible (users_ssh role)
      Port {{ ssh_port }}
      PermitRootLogin {{ ssh_permit_root_login }}
      PasswordAuthentication {{ ssh_password_authentication }}
      PubkeyAuthentication {{ ssh_pubkey_authentication }}
      UsePAM {{ ssh_use_pam }}
      KbdInteractiveAuthentication {{ ssh_kbdinteractive_authentication }}
      {% if ssh_allow_groups | length > 0 %}
      AllowGroups {{ ssh_allow_groups | join(' ') }}
      {% endif %}

      # Robust override (if other Match blocks disable passwords):
      Match all
          PasswordAuthentication {{ ssh_password_authentication }}
          KbdInteractiveAuthentication {{ ssh_kbdinteractive_authentication }}
          PubkeyAuthentication {{ ssh_pubkey_authentication }}
  notify: Restart sshd

- name: SSH | Validate sshd configuration
  ansible.builtin.command: sshd -t
  changed_when: false
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

#### 1.42 roles/validate/tasks/main.yml
**Comando**
```bash
sed -n '1,200p' roles/validate/tasks/main.yml
```
**Salida**
```text
---
- name: Validate | Show hostname and OS
  ansible.builtin.command: uname -a
  register: uname_out
  changed_when: false

- name: Validate | Print uname
  ansible.builtin.debug:
    var: uname_out.stdout

- name: Validate | Check SSH password auth effective config (sshd -T)
  ansible.builtin.shell: |
    set -euo pipefail
    sshd -T | egrep -i 'passwordauthentication|usepam|kbdinteractiveauthentication|port|permitrootlogin'
  args:
    executable: /bin/bash
  register: sshd_t
  changed_when: false

- name: Validate | Print sshd -T relevant lines
  ansible.builtin.debug:
    var: sshd_t.stdout_lines

- name: Validate | Check nvidia-smi
  ansible.builtin.command: nvidia-smi -L
  register: nvsmi
  changed_when: false
  failed_when: validate_cuda | bool and (nvsmi.rc != 0)

- name: Validate | Print nvidia-smi
  ansible.builtin.debug:
    var: nvsmi.stdout_lines

- name: Validate | Check Torch CUDA inside micromamba env
  ansible.builtin.command: >
    {{ llm_micromamba_bin }} run -n {{ llm_env_name }}
    python -c "import torch; print(torch.__version__); print('cuda', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no-gpu')"
  environment:
    MAMBA_ROOT_PREFIX: "/opt/micromamba"
  register: torch_cuda
  changed_when: false
  failed_when: false

- name: Validate | Fail if LLM env missing or Torch CUDA unavailable
  ansible.builtin.fail:
    msg: >-
      LLM env check failed (rc={{ torch_cuda.rc }}). Ensure micromamba env
      '{{ llm_env_name }}' exists and torch has CUDA. stdout={{ torch_cuda.stdout | default('') }}
      stderr={{ torch_cuda.stderr | default('') }}
  when: validate_llm | bool and (torch_cuda.rc != 0 or 'cuda True' not in torch_cuda.stdout)

- name: Validate | Print Torch CUDA check
  ansible.builtin.debug:
    var: torch_cuda.stdout_lines

# - name: Validate | Slurm checks
#   ansible.builtin.include_tasks: slurm.yml
#   tags: [validate, validate_slurm]
```
**Interpretacion breve**
- Extracto para inferir el proposito del rol. 

### 1.43 Resumen de propositos de roles (derivado de tasks/main.yml)
- common: paquetes base y chrony.
- firewall: firewalld + reglas SSH/Slurm.
- llm_env: instala micromamba y entorno LLM (conda/pip) + validaciones torch.
- llm_project: despliega el contenido de llm-project en el destino.
- mariadb_server: instala y valida MariaDB.
- munge: instala/crea clave munge y distribuye servicio.
- network_internal: configura enlaces internos via nmcli (master/worker).
- nfs_hpc: configura NFS server/cliente y permisos de grupo.
- nvidia_cuda: instala/valida driver CUDA y prerequisitos.
- slurm_compute: gestiona slurmd en nodos compute.
- slurm_controller: gestiona slurmctld y slurmdbd en master.
- slurm_db_prep: prepara MariaDB para SlurmDB (DB/usuarios/tuning).
- slurm_facts: calcula facts de CPU/MEM/GPU y GRES.
- slurm_identities: crea usuarios/grupos munge y slurm.
- slurm_install: instala RPMs/paquetes y archivos base de Slurm.
- slurm_rpm_build: compila RPMs de Slurm desde tarball.
- slurm_validate: validaciones y smoke tests Slurm (CPU/GPU).
- users_ssh: configura sshd con drop-in 99-hpc.conf.
- validate: validaciones de SSH/GPU/LLM (no Slurm).

## 2. Topologia del cluster (master)

#### 2.1 hostnamectl
**Comando**
```bash
hostnamectl
```
**Salida**
```text
Failed to connect to bus: Operation not permitted
```
**Interpretacion breve**
- No verificado: fallo al acceder a dbus/systemd. 

#### 2.2 hostname
**Comando**
```bash
hostname
```
**Salida**
```text
master
```
**Interpretacion breve**
- Hostname local obtenido sin privilegios. 

#### 2.3 /etc/os-release
**Comando**
```bash
cat /etc/os-release
```
**Salida**
```text
NAME="Rocky Linux"
VERSION="9.7 (Blue Onyx)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.7"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Rocky Linux 9.7 (Blue Onyx)"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:9::baseos"
HOME_URL="https://rockylinux.org/"
VENDOR_NAME="RESF"
VENDOR_URL="https://resf.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
SUPPORT_END="2032-05-31"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-9"
ROCKY_SUPPORT_PRODUCT_VERSION="9.7"
REDHAT_SUPPORT_PRODUCT="Rocky Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.7"
```
**Interpretacion breve**
- Version de SO reportada por el sistema. 

#### 2.4 uptime
**Comando**
```bash
uptime
```
**Salida**
```text
 12:21:34 up 4 days, 44 min,  3 users,  load average: 1.34, 1.05, 0.82
```
**Interpretacion breve**
- Uptime y carga actual. 

#### 2.5 timedatectl
**Comando**
```bash
timedatectl
```
**Salida**
```text
Failed to connect to bus: Operation not permitted
```
**Interpretacion breve**
- No verificado: fallo al acceder a dbus/systemd. 

#### 2.6 lscpu
**Comando**
```bash
lscpu
```
**Salida**
```text
Architecture:                            x86_64
CPU op-mode(s):                          32-bit, 64-bit
Address sizes:                           39 bits physical, 48 bits virtual
Byte Order:                              Little Endian
CPU(s):                                  20
On-line CPU(s) list:                     0-19
Vendor ID:                               GenuineIntel
Model name:                              Intel(R) Xeon(R) W-1290 CPU @ 3.20GHz
CPU family:                              6
Model:                                   165
Thread(s) per core:                      2
Core(s) per socket:                      10
Socket(s):                               1
Stepping:                                5
CPU(s) scaling MHz:                      25%
CPU max MHz:                             5200.0000
CPU min MHz:                             800.0000
BogoMIPS:                                6399.96
Flags:                                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp vnmi pku ospke md_clear flush_l1d arch_capabilities
Virtualization:                          VT-x
L1d cache:                               320 KiB (10 instances)
L1i cache:                               320 KiB (10 instances)
L2 cache:                                2.5 MiB (10 instances)
L3 cache:                                20 MiB (1 instance)
NUMA node(s):                            1
NUMA node0 CPU(s):                       0-19
Vulnerability Gather data sampling:      Mitigation; Microcode
Vulnerability Indirect target selection: Mitigation; Aligned branch/return thunks
Vulnerability Itlb multihit:             KVM: Mitigation: Split huge pages
Vulnerability L1tf:                      Not affected
Vulnerability Mds:                       Not affected
Vulnerability Meltdown:                  Not affected
Vulnerability Mmio stale data:           Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Reg file data sampling:    Not affected
Vulnerability Retbleed:                  Mitigation; Enhanced IBRS
Vulnerability Spec rstack overflow:      Not affected
Vulnerability Spec store bypass:         Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:                Mitigation; Enhanced / Automatic IBRS; IBPB conditional; PBRSB-eIBRS SW sequence; BHI SW loop, KVM SW loop
Vulnerability Srbds:                     Mitigation; Microcode
Vulnerability Tsa:                       Not affected
Vulnerability Tsx async abort:           Not affected
Vulnerability Vmscape:                   Mitigation; IBPB before exit to userspace
```
**Interpretacion breve**
- CPU/threads/topologia detectada en el master. 

#### 2.7 free -h
**Comando**
```bash
free -h
```
**Salida**
```text
               total        used        free      shared  buff/cache   available
Mem:            62Gi       7.5Gi        47Gi       938Mi       8.5Gi        54Gi
Swap:          8.0Gi          0B       8.0Gi
```
**Interpretacion breve**
- Memoria RAM y swap. 

#### 2.8 lsblk -f
**Comando**
```bash
lsblk -f
```
**Salida**
```text
NAME        FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
sda                                                                                
├─sda1      xfs                1ff09a7d-2dc3-4aa6-bd8b-890b5c90f6d6                
└─sda2                                                                             
sr0                                                                                
nvme0n1                                                                            
├─nvme0n1p1 vfat   FAT16       76EA-135F                             292.7M     2% /boot/efi
├─nvme0n1p2 xfs                0f4756a1-ab50-4ba3-9cff-a2c1fa7386ef  123.3M    87% /boot
├─nvme0n1p3 xfs                89c7bebb-e7b2-4b30-a177-2900bbb73583   58.3G    27% /
├─nvme0n1p4 xfs                139eee00-175e-4f5c-a673-5ecea46fce23   40.7G    32% /opt
├─nvme0n1p5 xfs                6e1adf42-3253-49a7-a975-fad41eb18654   38.5G     4% /var
├─nvme0n1p6 xfs                1065f17a-5798-49a6-b6fb-10abfd0e092a     27G    10% /home
└─nvme0n1p7 swap   1           66a3234c-459f-4cd8-85ed-8ec9fe7b20e2                [SWAP]
```
**Interpretacion breve**
- Dispositivos y sistemas de archivos. 

#### 2.9 df -hT
**Comando**
```bash
df -hT
```
**Salida**
```text
Filesystem     Type      Size  Used Avail Use% Mounted on
devtmpfs       devtmpfs  4.0M     0  4.0M   0% /dev
tmpfs          tmpfs      32G     0   32G   0% /dev/shm
tmpfs          tmpfs      13G   48M   13G   1% /run
efivarfs       efivarfs  384K   90K  290K  24% /sys/firmware/efi/efivars
/dev/nvme0n1p3 xfs        80G   22G   59G  28% /
/dev/nvme0n1p6 xfs        30G  3.0G   28G  10% /home
/dev/nvme0n1p5 xfs        40G  1.5G   39G   4% /var
/dev/nvme0n1p2 xfs       960M  837M  124M  88% /boot
/dev/nvme0n1p4 xfs        60G   20G   41G  33% /opt
/dev/nvme0n1p1 vfat      300M  7.1M  293M   3% /boot/efi
tmpfs          tmpfs     6.3G  916K  6.3G   1% /run/user/1000
```
**Interpretacion breve**
- Uso de disco por filesystem. 

#### 2.10 ip -br a
**Comando**
```bash
ip -br a
```
**Salida**
```text
Cannot open netlink socket: Operation not permitted
```
**Interpretacion breve**
- No verificado: netlink sin permisos. 

#### 2.11 ip r
**Comando**
```bash
ip r
```
**Salida**
```text
Cannot open netlink socket: Operation not permitted
```
**Interpretacion breve**
- No verificado: netlink sin permisos. 

#### 2.12 ss -lntp (head 200)
**Comando**
```bash
ss -lntp | head -n 200
```
**Salida**
```text
Cannot open netlink socket: Operation not permitted
State  Recv-Q Send-Q               Local Address:Port  Peer Address:PortProcess
LISTEN 0      0                          0.0.0.0:3306       0.0.0.0:*          
LISTEN 0      0                          0.0.0.0:2049       0.0.0.0:*          
LISTEN 0      0                          0.0.0.0:34345      0.0.0.0:*          
LISTEN 0      0                          0.0.0.0:22         0.0.0.0:*          
LISTEN 0      0                          0.0.0.0:111        0.0.0.0:*          
LISTEN 0      0                          0.0.0.0:6818       0.0.0.0:*          
LISTEN 0      0                          0.0.0.0:6819       0.0.0.0:*          
LISTEN 0      0                          0.0.0.0:6817       0.0.0.0:*          
LISTEN 0      0                          0.0.0.0:47027      0.0.0.0:*          
LISTEN 0      0                     100.98.68.22:63756      0.0.0.0:*          
LISTEN 0      0                          0.0.0.0:20048      0.0.0.0:*          
LISTEN 0      0                        127.0.0.1:33349      0.0.0.0:*          
LISTEN 0      0                        127.0.0.1:631        0.0.0.0:*          
LISTEN 0      0                                *:3306             *:*          
LISTEN 0      0                                *:2049             *:*          
LISTEN 0      0                                *:22               *:*          
LISTEN 0      0                                *:111              *:*          
LISTEN 0      0                                *:40097            *:*          
LISTEN 0      0                                *:5900             *:*          
LISTEN 0      0                                *:20048            *:*          
LISTEN 0      0      [fd7a:115c:a1e0::2f32:4416]:55228            *:*          
LISTEN 0      0                            [::1]:631              *:*          
LISTEN 0      0                                *:57387            *:*          
```
**Interpretacion breve**
- Puertos en escucha visibles sin privilegios completos (incluye Slurm/NFS/DB). 

#### 2.13 mount | egrep 'nfs|/data|/scratch'
**Comando**
```bash
mount | egrep 'nfs|/data|/scratch' || true
```
**Salida**
```text
sunrpc on /var/lib/nfs/rpc_pipefs type rpc_pipefs (rw,relatime)
nfsd on /proc/fs/nfsd type nfsd (rw,relatime)
```
**Interpretacion breve**
- Indicios de NFS en el master. 

#### 2.14 showmount -e localhost
**Comando**
```bash
showmount -e localhost || true
```
**Salida**
```text
clnt_create: RPC: Remote system error - Operation not permitted
```
**Interpretacion breve**
- No verificado: RPC sin permisos o servicio restringido. 

**Nota sobre acceso a workers**
- No se ejecutaron comandos remotos; el estado de workers solo se infiere desde archivos locales y logs del master.

## 3. Estado de Slurm (core)

#### 3.1 systemctl status slurmctld
**Comando**
```bash
systemctl status slurmctld --no-pager
```
**Salida**
```text
Failed to connect to bus: Operation not permitted
```
**Interpretacion breve**
- No verificado: fallo al acceder a systemd. 

#### 3.2 systemctl status slurmd
**Comando**
```bash
systemctl status slurmd --no-pager
```
**Salida**
```text
Failed to connect to bus: Operation not permitted
```
**Interpretacion breve**
- No verificado: fallo al acceder a systemd. 

#### 3.3 systemctl status slurmdbd
**Comando**
```bash
systemctl status slurmdbd --no-pager || true
```
**Salida**
```text
Failed to connect to bus: Operation not permitted
```
**Interpretacion breve**
- No verificado: fallo al acceder a systemd. 

#### 3.4 sinfo --version
**Comando**
```bash
sinfo --version || true
```
**Salida**
```text
slurm 23.11.3
```
**Interpretacion breve**
- Version de cliente Slurm instalada. 

#### 3.5 scontrol --version
**Comando**
```bash
scontrol --version || true
```
**Salida**
```text
slurm 23.11.3
```
**Interpretacion breve**
- Version de scontrol instalada. 

#### 3.6 scontrol ping
**Comando**
```bash
timeout 5 scontrol ping || true
```
**Salida**
```text
scontrol: error: Error creating slurm stream socket: Operation not permitted
Slurmctld(primary) at master is DOWN
```
**Interpretacion breve**
- Cliente no pudo crear socket Slurm; reporte indica slurmctld DOWN. 

#### 3.7 sinfo -lN
**Comando**
```bash
timeout 5 sinfo -lN || true
```
**Salida**
```text
Tue Jan 27 12:22:06 2026
sinfo: error: Error creating slurm stream socket: Operation not permitted
sinfo: error: Error creating slurm stream socket: Operation not permitted
sinfo: error: Error creating slurm stream socket: Operation not permitted
sinfo: error: Error creating slurm stream socket: Operation not permitted
sinfo: error: Error creating slurm stream socket: Operation not permitted
```
**Interpretacion breve**
- No verificado: error de socket Slurm. 

#### 3.8 sinfo -o '%P %a %l %D %t %N'
**Comando**
```bash
timeout 5 sinfo -o '%P %a %l %D %t %N' || true
```
**Salida**
```text
sinfo: error: Error creating slurm stream socket: Operation not permitted
sinfo: error: Error creating slurm stream socket: Operation not permitted
sinfo: error: Error creating slurm stream socket: Operation not permitted
sinfo: error: Error creating slurm stream socket: Operation not permitted
sinfo: error: Error creating slurm stream socket: Operation not permitted
```
**Interpretacion breve**
- No verificado: error de socket Slurm. 

#### 3.9 squeue
**Comando**
```bash
timeout 5 squeue || true
```
**Salida**
```text
squeue: error: Error creating slurm stream socket: Operation not permitted
squeue: error: Error creating slurm stream socket: Operation not permitted
squeue: error: Error creating slurm stream socket: Operation not permitted
squeue: error: Error creating slurm stream socket: Operation not permitted
squeue: error: Error creating slurm stream socket: Operation not permitted
```
**Interpretacion breve**
- No verificado: error de socket Slurm. 

#### 3.10 scontrol show partitions
**Comando**
```bash
timeout 5 scontrol show partitions || true
```
**Salida**
```text
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
```
**Interpretacion breve**
- No verificado: error de socket Slurm. 

#### 3.11 scontrol show nodes
**Comando**
```bash
timeout 5 scontrol show nodes || true
```
**Salida**
```text
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
```
**Interpretacion breve**
- No verificado: error de socket Slurm. 

#### 3.12 scontrol show config | head -n 200
**Comando**
```bash
timeout 5 scontrol show config | head -n 200 || true
```
**Salida**
```text
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
scontrol: error: Error creating slurm stream socket: Operation not permitted
```
**Interpretacion breve**
- No verificado: error de socket Slurm. 

#### 3.13 ls -la /etc/slurm + archivos clave
**Comando**
```bash
ls -la /etc/slurm /etc/slurm/slurm.conf /etc/slurm/gres.conf /etc/slurm/cgroup.conf 2>/dev/null || true
```
**Salida**
```text
-rw-r--r--. 1 root root   24 Jan 21 12:20 /etc/slurm/cgroup.conf
-rw-r--r--. 1 root root  212 Jan 24 10:45 /etc/slurm/gres.conf
-rw-r--r--. 1 root root 4682 Jan 26 09:28 /etc/slurm/slurm.conf

/etc/slurm:
total 64
drwxr-xr-x.   2 root  root  4096 Jan 26 11:08 .
drwxr-xr-x. 153 root  root  8192 Jan 26 16:37 ..
-rw-r--r--.   1 root  root    24 Jan 21 12:20 cgroup.conf
-rw-r--r--.   1 root  root   241 Jan 21 12:04 cgroup.conf.example
-rw-r--r--.   1 root  root  3126 Jan 21 12:04 cli_filter.lua.example
-rw-r--r--.   1 root  root   212 Jan 24 10:45 gres.conf
-rw-r--r--.   1 root  root  6371 Jan 21 12:04 job_submit.lua.example
-rw-r--r--.   1 root  root  2879 Jan 21 12:04 prolog.example
-rw-r--r--.   1 root  root  4682 Jan 26 09:28 slurm.conf
-rw-r--r--.   1 root  root  3021 Jan 21 12:04 slurm.conf.example
-rw-------.   1 slurm slurm  287 Jan 26 11:08 slurmdbd.conf
-rw-------.   1 root  root   745 Jan 21 12:04 slurmdbd.conf.example
```
**Interpretacion breve**
- Archivos Slurm presentes en /etc/slurm (slurm.conf, gres.conf, cgroup.conf). 

#### 3.14 /etc/slurm/slurm.conf (1-200)
**Comando**
```bash
sed -n '1,200p' /etc/slurm/slurm.conf 2>/dev/null || true
```
**Salida**
```text
# slurm.config_1
# Example slurm.conf file. Please run configurator.html
# (in doc/html) to build a configuration file customized
# for your environment.
#
#
# slurm.conf file generated by configurator.html.
# Put this file on all nodes of your cluster.
# See the slurm.conf man page for more information.
#
ClusterName=cluster_HPC
SlurmctldHost=master
#
#DisableRootJobs=NO
#EnforcePartLimits=NO
#Epilog=
#EpilogSlurmctld=
#FirstJobId=1
#MaxJobId=67043328
GresTypes=gpu
#GroupUpdateForce=0
#GroupUpdateTime=600
#JobFileAppend=0
#JobRequeue=1
#JobSubmitPlugins=lua
#KillOnBadExit=0
#LaunchType=launch/slurm
#Licenses=foo*4,bar
MailProg=/usr/bin/slurm-spool-mail
#MaxJobCount=10000
#MaxStepCount=40000
#MaxTasksPerNode=512
MpiDefault=none
#MpiParams=ports=#-#
#PluginDir=
#PlugStackConfig=
#PrivateData=jobs
ProctrackType=proctrack/cgroup
#Prolog=
#PrologFlags=
#PrologSlurmctld=
#PropagatePrioProcess=0
#PropagateResourceLimits=
#PropagateResourceLimitsExcept=
#RebootProgram=
ReturnToService=1
SlurmctldPidFile=/var/run/slurmctld.pid
SlurmctldPort=6817
# Modificacion julio 22 2025
SlurmdPidFile=/var/run/slurm/slurmd.pid
#SlurmdPidFile=/var/run/slurmd.pid
SlurmdPort=6818

# srun uses a return TCP port range on the submitting host (controller/login)
SrunPortRange=60001-60100

SlurmdSpoolDir=/var/spool/slurmd
SlurmUser=slurm
#
# 03-04-2024 Modicamos a usuario root
#SlurmdUser=root
#SrunEpilog=
#SrunProlog=
StateSaveLocation=/var/spool/slurmctld
SwitchType=switch/none
#TaskEpilog=
#TaskPlugin=task/affinity
TaskPlugin=task/cgroup
#TaskProlog=
#TopologyPlugin=topology/tree
#TmpFS=/tmp
#TrackWCKey=no
#TreeWidth=
#UnkillableStepProgram=
#UsePAM=0
#
#
# TIMERS
#BatchStartTimeout=10
#CompleteWait=0
#EpilogMsgTime=2000
#GetEnvTimeout=2
#HealthCheckInterval=0
#HealthCheckProgram=
InactiveLimit=0
KillWait=30
#MessageTimeout=10
#ResvOverRun=0
MinJobAge=300
#OverTimeLimit=0
SlurmctldTimeout=120
SlurmdTimeout=300
#UnkillableStepTimeout=60
#VSizeFactor=0
Waittime=0
#
#
# SCHEDULING
# 2025-01-30
# Memoria RAM [MB] asignada por defecto a cada CPU
DefMemPerCPU=100
#MaxMemPerCPU=0
#SchedulerTimeSlice=30
SchedulerType=sched/backfill
# 2024-11-07
# Para poder distrubuis recursos en un nodo entre varios Jobs
SelectType=select/cons_tres
# Para distribuis memorya y cpus totales (incluyendo threads)
SelectTypeParameters=CR_Core_Memory
#2025-10-30
# Se agrega para incluir GPU
#SelectTypeParameters=CR_Core_Memory,CR_GPU
#
#
# JOB PRIORITY
#PriorityFlags=
#PriorityType=priority/multifactor
#PriorityDecayHalfLife=
#PriorityCalcPeriod=
#PriorityFavorSmall=
#PriorityMaxAge=
#PriorityUsageResetPeriod=
#PriorityWeightAge=
#PriorityWeightFairshare=
#PriorityWeightJobSize=
#PriorityWeightPartition=
#PriorityWeightQOS=
#
#
# LOGGING AND ACCOUNTING
#AccountingStorageEnforce=limits
#AccountingStorageHost=
#AccountingStoragePass=
#AccountingStoragePort=
#AccountingStorageType=accounting_storage/none
# 27/03/2024 enable from
AccountingStorageType=accounting_storage/slurmdbd
AccountingStorageUser=slurm
AccountingStorageHost=localhost
#AccountingStoreJobComment=YES
#AccountingStoragePass=[REDACTED]
# 03/04/2024 linea comentada
#AccountingStorageLoc=slurm_acct_db
#AccountingStorageLoc=slurm_acct_db
#AccountingStoreFlags=job_comment
#AccountingStoreFlags=
# (1) JobCompHost=localhost
#JobCompLoc=slurm_jobcomp_db
#JobCompLoc=
#JobCompPass=
#JobCompPort=
# 04-04-2024 
#JobCompType=jobcomp/mysql
#JobCompUser=
#JobContainerType=
JobAcctGatherFrequency=30
# 04-04-2024
JobAcctGatherType=jobacct_gather/cgroup
#JobAcctGatherType=jobacct_gather/linux
#JobAcctGatherType=jobacct_gather/none #Original
SlurmctldDebug=info
SlurmctldLogFile=/var/log/slurm/slurmctld.log
SlurmdDebug=info
SlurmdLogFile=/var/log/slurm/slurmd.log
#SlurmSchedLogFile=
#SlurmSchedLogLevel=
#DebugFlags=
#
#
# POWER SAVE SUPPORT FOR IDLE NODES (optional)
#SuspendProgram=
#ResumeProgram=
#SuspendTimeout=
#ResumeTimeout=
#ResumeRate=
#SuspendExcNodes=
#SuspendExcParts=
#SuspendRate=
#SuspendTime=
#
#
# COMPUTE NODES (ANSIBLE MANAGED)
NodeName=master CPUs=20 Sockets=1 CoresPerSocket=10 ThreadsPerCore=2 RealMemory=62715 CoreSpecCount=1 MemSpecLimit=16000 Gres=gpu:quadro_p1000:1 State=UNKNOWN
NodeName=worker1 CPUs=20 Sockets=1 CoresPerSocket=10 ThreadsPerCore=2 RealMemory=62715 CoreSpecCount=2 MemSpecLimit=8000 Gres=gpu:quadro_p1000:1 State=UNKNOWN
NodeName=worker2 CPUs=20 Sockets=1 CoresPerSocket=10 ThreadsPerCore=2 RealMemory=62715 CoreSpecCount=3 MemSpecLimit=12000 Gres=gpu:quadro_p1000:1 State=UNKNOWN
# PARTITIONS (ANSIBLE MANAGED)
PartitionName=debug Nodes=master,worker1,worker2 Default=YES MaxTime=INFINITE State=UP
PartitionName=gpu Nodes=worker1,worker2 Default=NO MaxTime=INFINITE State=UP Shared=YES
```
**Interpretacion breve**
- Configuracion principal de Slurm, incluye nodos y particiones. Passwords redacted si aparecen. 

#### 3.15 /etc/slurm/gres.conf (1-200)
**Comando**
```bash
sed -n '1,200p' /etc/slurm/gres.conf 2>/dev/null || true
```
**Salida**
```text
# COMPUTE GRES (ANSIBLE MANAGED)
# AutoDetect=nvml habilita detección de GPUs y exposición de detalles vía NVML.
# El tipo se reduce a un identificador corto para scheduling (ej: a100, 3090).

AutoDetect=nvml
```
**Interpretacion breve**
- Configuracion de GRES (AutoDetect NVML). 

#### 3.16 /etc/slurm/cgroup.conf (1-200)
**Comando**
```bash
sed -n '1,200p' /etc/slurm/cgroup.conf 2>/dev/null || true
```
**Salida**
```text
CgroupPlugin=autodetect
```
**Interpretacion breve**
- Plugin de cgroups configurado. 

#### 3.17 journalctl -u slurmctld -n 200
**Comando**
```bash
journalctl -u slurmctld -n 200 --no-pager || true
```
**Salida**
```text
Jan 26 11:09:01 master slurmctld[1955645]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=242 NodeList=worker1 usec=182
Jan 26 11:09:01 master slurmctld[1955645]: slurmctld: _job_complete: JobId=242 WEXITSTATUS 0
Jan 26 11:09:01 master slurmctld[1955645]: slurmctld: _job_complete: JobId=242 done
Jan 26 11:09:02 master slurmctld[1955645]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=243 NodeList=worker1 usec=174
Jan 26 11:09:03 master slurmctld[1955645]: slurmctld: _job_complete: JobId=243 WEXITSTATUS 0
Jan 26 11:09:03 master slurmctld[1955645]: slurmctld: _job_complete: JobId=243 done
Jan 26 11:09:04 master slurmctld[1955645]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=244 NodeList=worker1 usec=170
Jan 26 11:09:05 master slurmctld[1955645]: slurmctld: _job_complete: JobId=244 WEXITSTATUS 0
Jan 26 11:09:05 master slurmctld[1955645]: slurmctld: _job_complete: JobId=244 done
Jan 26 11:09:08 master slurmctld[1955645]: slurmctld: _slurm_rpc_submit_batch_job: JobId=245 InitPrio=1 usec=163
Jan 26 11:09:09 master slurmctld[1955645]: slurmctld: sched: Allocate JobId=245 NodeList=worker2 #CPUs=2 Partition=debug
Jan 26 11:09:09 master slurmctld[1955645]: slurmctld: _job_complete: JobId=245 WEXITSTATUS 0
Jan 26 11:09:09 master slurmctld[1955645]: slurmctld: _job_complete: JobId=245 done
Jan 26 11:09:15 master slurmctld[1955645]: slurmctld: _slurm_rpc_submit_batch_job: JobId=246 InitPrio=1 usec=171
Jan 26 11:09:17 master slurmctld[1955645]: slurmctld: sched: Allocate JobId=246 NodeList=worker1 #CPUs=2 Partition=gpu
Jan 26 11:09:17 master slurmctld[1955645]: slurmctld: _job_complete: JobId=246 WEXITSTATUS 0
Jan 26 11:09:17 master slurmctld[1955645]: slurmctld: _job_complete: JobId=246 done
Jan 26 11:09:37 master slurmctld[1955645]: slurmctld: _slurm_rpc_submit_batch_job: JobId=247 InitPrio=1 usec=236
Jan 26 11:09:38 master slurmctld[1955645]: slurmctld: sched: Allocate JobId=247 NodeList=worker1 #CPUs=2 Partition=gpu
Jan 26 11:09:43 master slurmctld[1955645]: slurmctld: _job_complete: JobId=247 WEXITSTATUS 0
Jan 26 11:09:43 master slurmctld[1955645]: slurmctld: _job_complete: JobId=247 done
Jan 26 11:11:47 master slurmctld[1955645]: slurmctld: Terminate signal (SIGINT or SIGTERM) received
Jan 26 11:11:47 master slurmctld[1955645]: slurmctld: Saving all slurm state
Jan 26 11:11:47 master systemd[1]: Stopping Slurm controller daemon...
Jan 26 11:11:47 master systemd[1]: slurmctld.service: Deactivated successfully.
Jan 26 11:11:47 master systemd[1]: Stopped Slurm controller daemon.
Jan 26 11:11:47 master systemd[1]: slurmctld.service: Consumed 3min 48.316s CPU time.
Jan 26 11:11:47 master systemd[1]: Starting Slurm controller daemon...
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: error: Configured MailProg is invalid
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: slurmctld version 23.11.3 started on cluster cluster_hpc
Jan 26 11:11:47 master systemd[1]: Started Slurm controller daemon.
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: accounting_storage/slurmdbd: clusteracct_storage_p_register_ctld: Registering slurmctld at port 6817 with slurmdbd
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: No memory enforcing mechanism configured.
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered state of 3 nodes
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered JobId=240 Assoc=0
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered JobId=241 Assoc=2
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered JobId=242 Assoc=2
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered JobId=243 Assoc=2
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered JobId=244 Assoc=2
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered JobId=245 Assoc=2
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered JobId=246 Assoc=2
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered JobId=247 Assoc=0
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered information about 8 jobs
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: select/cons_tres: part_data_create_array: select/cons_tres: preparing for 2 partitions
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Recovered state of 0 reservations
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: read_slurm_conf: backup_controller not specified
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: select/cons_tres: select_p_reconfigure: select/cons_tres: reconfigure
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: select/cons_tres: part_data_create_array: select/cons_tres: preparing for 2 partitions
Jan 26 11:11:47 master slurmctld[1973174]: slurmctld: Running as primary controller
Jan 26 11:12:11 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=248 InitPrio=1 usec=346
Jan 26 11:12:12 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=248 NodeList=worker1 #CPUs=2 Partition=gpu
Jan 26 11:12:17 master slurmctld[1973174]: slurmctld: _job_complete: JobId=248 WEXITSTATUS 0
Jan 26 11:12:17 master slurmctld[1973174]: slurmctld: _job_complete: JobId=248 done
Jan 26 11:14:16 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=249 InitPrio=1 usec=209
Jan 26 11:14:17 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=249 NodeList=worker1 #CPUs=2 Partition=gpu
Jan 26 11:14:23 master slurmctld[1973174]: slurmctld: _job_complete: JobId=249 WEXITSTATUS 0
Jan 26 11:14:23 master slurmctld[1973174]: slurmctld: _job_complete: JobId=249 done
Jan 26 11:16:42 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=250 InitPrio=1 usec=204
Jan 26 11:16:42 master slurmctld[1973174]: slurmctld: sched/backfill: _start_job: Started JobId=250 in gpu on worker1
Jan 26 11:16:49 master slurmctld[1973174]: slurmctld: _job_complete: JobId=250 WEXITSTATUS 0
Jan 26 11:16:49 master slurmctld[1973174]: slurmctld: _job_complete: JobId=250 done
Jan 26 11:16:56 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=251 InitPrio=1 usec=214
Jan 26 11:16:57 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=251 NodeList=worker1 #CPUs=2 Partition=gpu
Jan 26 11:17:03 master slurmctld[1973174]: slurmctld: _job_complete: JobId=251 WEXITSTATUS 0
Jan 26 11:17:03 master slurmctld[1973174]: slurmctld: _job_complete: JobId=251 done
Jan 26 11:17:13 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=252 InitPrio=1 usec=235
Jan 26 11:17:14 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=252 NodeList=worker1 #CPUs=2 Partition=gpu
Jan 26 11:17:20 master slurmctld[1973174]: slurmctld: _job_complete: JobId=252 WEXITSTATUS 0
Jan 26 11:17:20 master slurmctld[1973174]: slurmctld: _job_complete: JobId=252 done
Jan 26 11:18:25 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=253 InitPrio=1 usec=338
Jan 26 11:18:26 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=253 NodeList=worker1 #CPUs=6 Partition=gpu
Jan 26 11:18:32 master slurmctld[1973174]: slurmctld: _job_complete: JobId=253 WEXITSTATUS 0
Jan 26 11:18:32 master slurmctld[1973174]: slurmctld: _job_complete: JobId=253 done
Jan 26 11:19:59 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=254 InitPrio=1 usec=214
Jan 26 11:20:00 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=254 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 11:20:05 master slurmctld[1973174]: slurmctld: _job_complete: JobId=254 WEXITSTATUS 0
Jan 26 11:20:05 master slurmctld[1973174]: slurmctld: _job_complete: JobId=254 done
Jan 26 11:58:18 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=255 NodeList=worker2 usec=270
Jan 26 11:58:18 master slurmctld[1973174]: slurmctld: _job_complete: JobId=255 WEXITSTATUS 0
Jan 26 11:58:18 master slurmctld[1973174]: slurmctld: _job_complete: JobId=255 done
Jan 26 11:58:18 master slurmctld[1973174]: slurmctld: error: slurm_send_node_msg: [socket:[7034675]] slurm_bufs_sendto(msg_type=SRUN_JOB_COMPLETE) failed: Connection reset by peer
Jan 26 11:58:18 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=256 NodeList=worker1 usec=181
Jan 26 11:58:18 master slurmctld[1973174]: slurmctld: _job_complete: JobId=256 WEXITSTATUS 0
Jan 26 11:58:18 master slurmctld[1973174]: slurmctld: _job_complete: JobId=256 done
Jan 26 11:58:19 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=257 NodeList=worker1 usec=177
Jan 26 11:58:20 master slurmctld[1973174]: slurmctld: _job_complete: JobId=257 WEXITSTATUS 0
Jan 26 11:58:20 master slurmctld[1973174]: slurmctld: _job_complete: JobId=257 done
Jan 26 11:58:21 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=258 NodeList=worker1 usec=169
Jan 26 11:58:22 master slurmctld[1973174]: slurmctld: _job_complete: JobId=258 WEXITSTATUS 0
Jan 26 11:58:22 master slurmctld[1973174]: slurmctld: _job_complete: JobId=258 done
Jan 26 11:58:25 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=259 InitPrio=1 usec=168
Jan 26 11:58:28 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=259 NodeList=worker2 #CPUs=2 Partition=debug
Jan 26 11:58:28 master slurmctld[1973174]: slurmctld: _job_complete: JobId=259 WEXITSTATUS 0
Jan 26 11:58:28 master slurmctld[1973174]: slurmctld: _job_complete: JobId=259 done
Jan 26 11:58:33 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=260 InitPrio=1 usec=167
Jan 26 11:58:34 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=260 NodeList=worker1 #CPUs=2 Partition=gpu
Jan 26 11:58:34 master slurmctld[1973174]: slurmctld: _job_complete: JobId=260 WEXITSTATUS 0
Jan 26 11:58:34 master slurmctld[1973174]: slurmctld: _job_complete: JobId=260 done
Jan 26 12:11:49 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=261 NodeList=worker2 usec=205
Jan 26 12:11:49 master slurmctld[1973174]: slurmctld: _job_complete: JobId=261 WEXITSTATUS 0
Jan 26 12:11:49 master slurmctld[1973174]: slurmctld: _job_complete: JobId=261 done
Jan 26 12:11:50 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=262 NodeList=worker1 usec=207
Jan 26 12:11:50 master slurmctld[1973174]: slurmctld: _job_complete: JobId=262 WEXITSTATUS 0
Jan 26 12:11:50 master slurmctld[1973174]: slurmctld: _job_complete: JobId=262 done
Jan 26 12:11:51 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=263 NodeList=worker1 usec=162
Jan 26 12:11:52 master slurmctld[1973174]: slurmctld: _job_complete: JobId=263 WEXITSTATUS 0
Jan 26 12:11:52 master slurmctld[1973174]: slurmctld: _job_complete: JobId=263 done
Jan 26 12:11:53 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=264 NodeList=worker1 usec=160
Jan 26 12:11:54 master slurmctld[1973174]: slurmctld: _job_complete: JobId=264 WEXITSTATUS 0
Jan 26 12:11:54 master slurmctld[1973174]: slurmctld: _job_complete: JobId=264 done
Jan 26 12:11:57 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=265 InitPrio=1 usec=157
Jan 26 12:11:58 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=265 NodeList=worker2 #CPUs=2 Partition=debug
Jan 26 12:12:03 master slurmctld[1973174]: slurmctld: _job_complete: JobId=265 WEXITSTATUS 0
Jan 26 12:12:03 master slurmctld[1973174]: slurmctld: _job_complete: JobId=265 done
Jan 26 12:12:09 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=266 InitPrio=1 usec=171
Jan 26 12:12:10 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=266 NodeList=worker1 #CPUs=2 Partition=gpu
Jan 26 12:12:10 master slurmctld[1973174]: slurmctld: _job_complete: JobId=266 WEXITSTATUS 0
Jan 26 12:12:10 master slurmctld[1973174]: slurmctld: _job_complete: JobId=266 done
Jan 26 12:15:09 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=267 NodeList=worker2 usec=322
Jan 26 12:15:09 master slurmctld[1973174]: slurmctld: _job_complete: JobId=267 WEXITSTATUS 0
Jan 26 12:15:09 master slurmctld[1973174]: slurmctld: _job_complete: JobId=267 done
Jan 26 12:15:10 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=268 NodeList=worker1 usec=163
Jan 26 12:15:10 master slurmctld[1973174]: slurmctld: _job_complete: JobId=268 WEXITSTATUS 0
Jan 26 12:15:10 master slurmctld[1973174]: slurmctld: _job_complete: JobId=268 done
Jan 26 12:15:11 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=269 NodeList=worker1 usec=174
Jan 26 12:15:12 master slurmctld[1973174]: slurmctld: _job_complete: JobId=269 WEXITSTATUS 0
Jan 26 12:15:12 master slurmctld[1973174]: slurmctld: _job_complete: JobId=269 done
Jan 26 12:15:12 master slurmctld[1973174]: slurmctld: sched: _slurm_rpc_allocate_resources JobId=270 NodeList=worker1 usec=169
Jan 26 12:15:13 master slurmctld[1973174]: slurmctld: _job_complete: JobId=270 WEXITSTATUS 0
Jan 26 12:15:13 master slurmctld[1973174]: slurmctld: _job_complete: JobId=270 done
Jan 26 12:15:17 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=271 InitPrio=1 usec=157
Jan 26 12:15:19 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=271 NodeList=worker2 #CPUs=2 Partition=debug
Jan 26 12:15:24 master slurmctld[1973174]: slurmctld: _job_complete: JobId=271 WEXITSTATUS 0
Jan 26 12:15:24 master slurmctld[1973174]: slurmctld: _job_complete: JobId=271 done
Jan 26 12:15:28 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=272 InitPrio=1 usec=161
Jan 26 12:15:29 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=272 NodeList=worker1 #CPUs=2 Partition=gpu
Jan 26 12:15:29 master slurmctld[1973174]: slurmctld: _job_complete: JobId=272 WEXITSTATUS 0
Jan 26 12:15:29 master slurmctld[1973174]: slurmctld: _job_complete: JobId=272 done
Jan 26 12:20:14 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=273 InitPrio=1 usec=339
Jan 26 12:20:15 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=273 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 12:20:20 master slurmctld[1973174]: slurmctld: _job_complete: JobId=273 WEXITSTATUS 0
Jan 26 12:20:20 master slurmctld[1973174]: slurmctld: _job_complete: JobId=273 done
Jan 26 16:13:42 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=274 InitPrio=1 usec=354
Jan 26 16:13:43 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=274 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 16:13:43 master slurmctld[1973174]: slurmctld: _job_complete: JobId=274 WTERMSIG 53
Jan 26 16:13:43 master slurmctld[1973174]: slurmctld: _job_complete: JobId=274 done
Jan 26 16:16:48 master slurmctld[1973174]: slurmctld: error: Nodes worker1 not responding
Jan 26 16:16:54 master slurmctld[1973174]: slurmctld: error: Nodes worker1 not responding, setting DOWN
Jan 26 16:20:36 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=275 InitPrio=1 usec=165
Jan 26 16:20:37 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=275 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 16:20:37 master slurmctld[1973174]: slurmctld: _job_complete: JobId=275 WTERMSIG 53
Jan 26 16:20:37 master slurmctld[1973174]: slurmctld: _job_complete: JobId=275 done
Jan 26 16:40:16 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=276 InitPrio=1 usec=470
Jan 26 16:40:17 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=276 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 16:40:22 master slurmctld[1973174]: slurmctld: _job_complete: JobId=276 WEXITSTATUS 0
Jan 26 16:40:22 master slurmctld[1973174]: slurmctld: _job_complete: JobId=276 done
Jan 26 16:41:31 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=277 InitPrio=1 usec=208
Jan 26 16:41:31 master slurmctld[1973174]: slurmctld: sched/backfill: _start_job: Started JobId=277 in gpu on worker2
Jan 26 16:41:37 master slurmctld[1973174]: slurmctld: _job_complete: JobId=277 WEXITSTATUS 0
Jan 26 16:41:37 master slurmctld[1973174]: slurmctld: _job_complete: JobId=277 done
Jan 26 16:49:39 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=278 InitPrio=1 usec=225
Jan 26 16:49:40 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=278 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 16:49:40 master slurmctld[1973174]: slurmctld: _job_complete: JobId=278 WTERMSIG 53
Jan 26 16:49:40 master slurmctld[1973174]: slurmctld: _job_complete: JobId=278 done
Jan 26 16:52:24 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=279 InitPrio=1 usec=252
Jan 26 16:52:25 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=279 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 16:52:25 master slurmctld[1973174]: slurmctld: _job_complete: JobId=279 WTERMSIG 53
Jan 26 16:52:25 master slurmctld[1973174]: slurmctld: _job_complete: JobId=279 done
Jan 26 16:56:29 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=280 InitPrio=1 usec=354
Jan 26 16:56:29 master slurmctld[1973174]: slurmctld: sched/backfill: _start_job: Started JobId=280 in gpu on worker2
Jan 26 16:56:35 master slurmctld[1973174]: slurmctld: _job_complete: JobId=280 WEXITSTATUS 0
Jan 26 16:56:35 master slurmctld[1973174]: slurmctld: _job_complete: JobId=280 done
Jan 26 16:59:26 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=281 InitPrio=1 usec=973
Jan 26 16:59:26 master slurmctld[1973174]: slurmctld: sched/backfill: _start_job: Started JobId=281 in gpu on worker2
Jan 26 16:59:26 master slurmctld[1973174]: slurmctld: _job_complete: JobId=281 WTERMSIG 53
Jan 26 16:59:26 master slurmctld[1973174]: slurmctld: _job_complete: JobId=281 done
Jan 26 17:03:52 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=282 InitPrio=1 usec=396
Jan 26 17:03:53 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=282 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 17:03:53 master slurmctld[1973174]: slurmctld: _job_complete: JobId=282 WTERMSIG 53
Jan 26 17:03:53 master slurmctld[1973174]: slurmctld: _job_complete: JobId=282 done
Jan 26 17:10:31 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=283 InitPrio=1 usec=454
Jan 26 17:10:32 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=283 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 17:10:37 master slurmctld[1973174]: slurmctld: _job_complete: JobId=283 WEXITSTATUS 0
Jan 26 17:10:37 master slurmctld[1973174]: slurmctld: _job_complete: JobId=283 done
Jan 26 17:22:38 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=284 InitPrio=1 usec=398
Jan 26 17:22:39 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=284 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 17:22:45 master slurmctld[1973174]: slurmctld: _job_complete: JobId=284 WEXITSTATUS 0
Jan 26 17:22:45 master slurmctld[1973174]: slurmctld: _job_complete: JobId=284 done
Jan 26 17:36:21 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=285 InitPrio=1 usec=658
Jan 26 17:36:22 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=285 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 17:36:28 master slurmctld[1973174]: slurmctld: _job_complete: JobId=285 WEXITSTATUS 0
Jan 26 17:36:28 master slurmctld[1973174]: slurmctld: _job_complete: JobId=285 done
Jan 26 17:49:04 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=286 InitPrio=1 usec=417
Jan 26 17:49:05 master slurmctld[1973174]: slurmctld: sched: Allocate JobId=286 NodeList=worker2 #CPUs=6 Partition=gpu
Jan 26 17:49:11 master slurmctld[1973174]: slurmctld: _job_complete: JobId=286 WEXITSTATUS 0
Jan 26 17:49:11 master slurmctld[1973174]: slurmctld: _job_complete: JobId=286 done
Jan 26 17:50:13 master slurmctld[1973174]: slurmctld: _slurm_rpc_submit_batch_job: JobId=287 InitPrio=1 usec=216
Jan 26 17:50:13 master slurmctld[1973174]: slurmctld: sched/backfill: _start_job: Started JobId=287 in gpu on worker2
Jan 26 17:50:19 master slurmctld[1973174]: slurmctld: _job_complete: JobId=287 WEXITSTATUS 0
Jan 26 17:50:19 master slurmctld[1973174]: slurmctld: _job_complete: JobId=287 done
```
**Interpretacion breve**
- Eventos recientes de slurmctld (jobs, restarts, warnings). 

#### 3.18 journalctl -u slurmd -n 200
**Comando**
```bash
journalctl -u slurmd -n 200 --no-pager || true
```
**Salida**
```text
Jan 24 10:17:10 master systemd[1]: Stopped Slurm node daemon.
Jan 24 10:17:10 master systemd[1]: Starting Slurm node daemon...
Jan 24 10:17:10 master slurmd[910646]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 10:17:10 master slurmd[910646]: slurmd: gres/gpu: _normalize_sys_gres_types: Could not find an unused configuration record with a GRES type that is a substring of system device `quadro_p1000`. Setting system GRES type to NULL
Jan 24 10:17:10 master slurmd[910646]: slurmd: slurmd version 23.11.3 started
Jan 24 10:17:10 master slurmd[910646]: slurmd: slurmd started on Sat, 24 Jan 2026 10:17:10 -0500
Jan 24 10:17:10 master slurmd[910646]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=81604 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 10:17:10 master systemd[1]: Started Slurm node daemon.
Jan 24 10:50:40 master systemd[1]: Stopping Slurm node daemon...
Jan 24 10:50:40 master slurmd[910646]: slurmd: Slurmd shutdown completing
Jan 24 10:50:40 master systemd[1]: slurmd.service: Deactivated successfully.
Jan 24 10:50:40 master systemd[1]: Stopped Slurm node daemon.
Jan 24 10:50:40 master systemd[1]: Starting Slurm node daemon...
Jan 24 10:50:40 master slurmd[952648]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 10:50:40 master slurmd[952648]: slurmd: slurmd version 23.11.3 started
Jan 24 10:50:40 master slurmd[952648]: slurmd: slurmd started on Sat, 24 Jan 2026 10:50:40 -0500
Jan 24 10:50:40 master slurmd[952648]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=83615 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 10:50:40 master systemd[1]: Started Slurm node daemon.
Jan 24 11:08:56 master slurmd[956584]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 11:08:56 master slurmd[956584]: slurmd: slurmd version 23.11.3 started
Jan 24 11:08:56 master slurmd[956584]: slurmd: slurmd started on Sat, 24 Jan 2026 11:08:56 -0500
Jan 24 11:08:56 master slurmd[956584]: slurmd: child started successfully
Jan 24 11:08:56 master slurmd[952648]: slurmd: Relinquishing control to new slurmd process (956584)
Jan 24 11:08:56 master slurmd[956584]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=84711 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 12:25:11 master slurmd[956584]: slurmd: launch task StepId=113.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:38924
Jan 24 12:25:21 master slurmd[956584]: slurmd: Launching batch job 117 for UID 0
Jan 24 12:44:31 master slurmd[956584]: slurmd: launch task StepId=119.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:56662
Jan 24 12:44:37 master slurmd[956584]: slurmd: Launching batch job 122 for UID 0
Jan 24 12:47:04 master slurmd[956584]: slurmd: launch task StepId=124.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:49624
Jan 24 12:47:10 master slurmd[956584]: slurmd: Launching batch job 127 for UID 0
Jan 24 12:49:37 master slurmd[956584]: slurmd: Launching batch job 129 for UID 1000
Jan 24 13:02:48 master slurmd[956584]: slurmd: launch task StepId=131.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:49126
Jan 24 13:02:54 master slurmd[956584]: slurmd: Launching batch job 134 for UID 0
Jan 24 13:06:21 master slurmd[956584]: slurmd: launch task StepId=136.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:58348
Jan 24 13:06:30 master slurmd[956584]: slurmd: Launching batch job 140 for UID 0
Jan 24 13:15:10 master slurmd[956584]: slurmd: launch task StepId=142.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:45874
Jan 24 13:15:19 master slurmd[956584]: slurmd: Launching batch job 146 for UID 0
Jan 24 13:20:12 master slurmd[956584]: slurmd: launch task StepId=148.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:43538
Jan 24 13:20:21 master slurmd[956584]: slurmd: Launching batch job 152 for UID 0
Jan 24 13:31:24 master slurmd[956584]: slurmd: launch task StepId=156.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:58894
Jan 24 13:31:34 master slurmd[956584]: slurmd: Launching batch job 160 for UID 0
Jan 24 13:58:52 master slurmd[1242122]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 13:58:52 master slurmd[1242122]: slurmd: slurmd version 23.11.3 started
Jan 24 13:58:52 master slurmd[1242122]: slurmd: slurmd started on Sat, 24 Jan 2026 13:58:52 -0500
Jan 24 13:58:52 master slurmd[1242122]: slurmd: child started successfully
Jan 24 13:58:52 master slurmd[956584]: slurmd: Relinquishing control to new slurmd process (1242122)
Jan 24 13:58:52 master slurmd[1242122]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=94906 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 14:11:05 master slurmd[1330186]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 14:11:05 master slurmd[1330186]: slurmd: slurmd version 23.11.3 started
Jan 24 14:11:05 master slurmd[1330186]: slurmd: slurmd started on Sat, 24 Jan 2026 14:11:05 -0500
Jan 24 14:11:05 master slurmd[1330186]: slurmd: child started successfully
Jan 24 14:11:05 master slurmd[1242122]: slurmd: Relinquishing control to new slurmd process (1330186)
Jan 24 14:11:05 master slurmd[1330186]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=95640 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 14:11:49 master systemd[1]: Stopping Slurm node daemon...
Jan 24 14:11:49 master slurmd[1330186]: slurmd: Slurmd shutdown completing
Jan 24 14:11:49 master systemd[1]: slurmd.service: Deactivated successfully.
Jan 24 14:11:49 master systemd[1]: Stopped Slurm node daemon.
Jan 24 14:11:49 master systemd[1]: Starting Slurm node daemon...
Jan 24 14:11:49 master slurmd[1341364]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 14:11:49 master slurmd[1341364]: slurmd: slurmd version 23.11.3 started
Jan 24 14:11:49 master slurmd[1341364]: slurmd: slurmd started on Sat, 24 Jan 2026 14:11:49 -0500
Jan 24 14:11:49 master systemd[1]: Started Slurm node daemon.
Jan 24 14:11:49 master slurmd[1341364]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=95684 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 14:11:55 master slurmd[1341364]: slurmd: launch task StepId=168.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:33962
Jan 24 14:12:04 master slurmd[1341364]: slurmd: Launching batch job 172 for UID 0
Jan 24 14:25:47 master slurmd[1406209]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 14:25:47 master slurmd[1406209]: slurmd: slurmd version 23.11.3 started
Jan 24 14:25:47 master slurmd[1406209]: slurmd: slurmd started on Sat, 24 Jan 2026 14:25:47 -0500
Jan 24 14:25:47 master slurmd[1406209]: slurmd: child started successfully
Jan 24 14:25:47 master slurmd[1341364]: slurmd: Relinquishing control to new slurmd process (1406209)
Jan 24 14:25:47 master slurmd[1406209]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=96522 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 15:47:06 master slurmd[1465334]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 15:47:06 master slurmd[1465334]: slurmd: slurmd version 23.11.3 started
Jan 24 15:47:06 master slurmd[1465334]: slurmd: slurmd started on Sat, 24 Jan 2026 15:47:06 -0500
Jan 24 15:47:06 master slurmd[1465334]: slurmd: child started successfully
Jan 24 15:47:06 master slurmd[1406209]: slurmd: Relinquishing control to new slurmd process (1465334)
Jan 24 15:47:06 master slurmd[1465334]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=101400 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 16:25:26 master slurmd[1551125]: slurmd: error: NodeNames=worker1 CoreSpecCount=2 is invalid, reset to 1
Jan 24 16:25:26 master slurmd[1551125]: slurmd: error: NodeNames=worker1 MemSpecLimit=8000 is invalid, reset to 0
Jan 24 16:25:26 master slurmd[1551125]: error: NodeNames=worker1 CoreSpecCount=2 is invalid, reset to 1
Jan 24 16:25:26 master slurmd[1551125]: error: NodeNames=worker1 MemSpecLimit=8000 is invalid, reset to 0
Jan 24 16:25:26 master slurmd[1551125]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 16:25:26 master slurmd[1551125]: slurmd: slurmd version 23.11.3 started
Jan 24 16:25:26 master slurmd[1551125]: slurmd: slurmd started on Sat, 24 Jan 2026 16:25:26 -0500
Jan 24 16:25:26 master slurmd[1551125]: slurmd: child started successfully
Jan 24 16:25:26 master slurmd[1465334]: slurmd: Relinquishing control to new slurmd process (1551125)
Jan 24 16:25:26 master slurmd[1551125]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=103701 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 16:26:39 master slurmd[1551286]: slurmd: error: NodeNames=worker1 CoreSpecCount=2 is invalid, reset to 1
Jan 24 16:26:39 master slurmd[1551286]: slurmd: error: NodeNames=worker1 MemSpecLimit=8000 is invalid, reset to 0
Jan 24 16:26:39 master slurmd[1551286]: error: NodeNames=worker1 CoreSpecCount=2 is invalid, reset to 1
Jan 24 16:26:39 master slurmd[1551286]: error: NodeNames=worker1 MemSpecLimit=8000 is invalid, reset to 0
Jan 24 16:26:39 master slurmd[1551286]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 16:26:39 master slurmd[1551286]: slurmd: slurmd version 23.11.3 started
Jan 24 16:26:39 master slurmd[1551286]: slurmd: slurmd started on Sat, 24 Jan 2026 16:26:39 -0500
Jan 24 16:26:39 master slurmd[1551286]: slurmd: child started successfully
Jan 24 16:26:39 master slurmd[1551125]: slurmd: Relinquishing control to new slurmd process (1551286)
Jan 24 16:26:39 master slurmd[1551286]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=103774 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 16:33:55 master slurmd[1580001]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 16:33:55 master slurmd[1580001]: slurmd: slurmd version 23.11.3 started
Jan 24 16:33:55 master slurmd[1580001]: slurmd: slurmd started on Sat, 24 Jan 2026 16:33:55 -0500
Jan 24 16:33:55 master slurmd[1580001]: slurmd: child started successfully
Jan 24 16:33:55 master slurmd[1551286]: slurmd: Relinquishing control to new slurmd process (1580001)
Jan 24 16:33:55 master slurmd[1580001]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=104210 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 16:37:54 master slurmd[1580134]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 16:37:54 master slurmd[1580134]: slurmd: slurmd version 23.11.3 started
Jan 24 16:37:54 master slurmd[1580134]: slurmd: slurmd started on Sat, 24 Jan 2026 16:37:54 -0500
Jan 24 16:37:54 master slurmd[1580134]: slurmd: child started successfully
Jan 24 16:37:54 master slurmd[1580001]: slurmd: Relinquishing control to new slurmd process (1580134)
Jan 24 16:37:54 master slurmd[1580134]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=104448 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 16:54:12 master slurmd[1654764]: slurmd: error: NodeNames=master CoreSpecCount=10 is invalid, reset to 1
Jan 24 16:54:12 master slurmd[1654764]: error: NodeNames=master CoreSpecCount=10 is invalid, reset to 1
Jan 24 16:54:13 master slurmd[1654764]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 16:54:13 master slurmd[1654764]: slurmd: Resource spec: Reserved abstract CPU IDs: 18-19
Jan 24 16:54:13 master slurmd[1654764]: slurmd: Resource spec: Reserved machine CPU IDs: 9,19
Jan 24 16:54:13 master slurmd[1654764]: slurmd: error: Resource spec: Limited MemSpecLimit support. Slurmd daemon not memory constrained. Reserved 32000 MB
Jan 24 16:54:13 master slurmd[1654764]: slurmd: slurmd version 23.11.3 started
Jan 24 16:54:13 master slurmd[1654764]: slurmd: slurmd started on Sat, 24 Jan 2026 16:54:13 -0500
Jan 24 16:54:13 master slurmd[1654764]: slurmd: child started successfully
Jan 24 16:54:13 master slurmd[1580134]: slurmd: Relinquishing control to new slurmd process (1654764)
Jan 24 16:54:13 master slurmd[1654764]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=105427 CPUSpecList=18-19 FeaturesAvail=(null) FeaturesActive=(null)
Jan 24 19:01:06 master slurmd[1715228]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 24 19:01:06 master slurmd[1715228]: slurmd: Resource spec: Reserved abstract CPU IDs: 18-19
Jan 24 19:01:06 master slurmd[1715228]: slurmd: Resource spec: Reserved machine CPU IDs: 9,19
Jan 24 19:01:06 master slurmd[1715228]: slurmd: error: Resource spec: Limited MemSpecLimit support. Slurmd daemon not memory constrained. Reserved 16000 MB
Jan 24 19:01:06 master slurmd[1715228]: slurmd: slurmd version 23.11.3 started
Jan 24 19:01:06 master slurmd[1715228]: slurmd: slurmd started on Sat, 24 Jan 2026 19:01:06 -0500
Jan 24 19:01:06 master slurmd[1715228]: slurmd: child started successfully
Jan 24 19:01:06 master slurmd[1654764]: slurmd: Relinquishing control to new slurmd process (1715228)
Jan 24 19:01:06 master slurmd[1715228]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=113041 CPUSpecList=18-19 FeaturesAvail=(null) FeaturesActive=(null)
Jan 25 20:13:34 master slurmd[1802269]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 25 20:13:34 master slurmd[1802269]: slurmd: slurmd version 23.11.3 started
Jan 25 20:13:34 master slurmd[1802269]: slurmd: slurmd started on Sun, 25 Jan 2026 20:13:34 -0500
Jan 25 20:13:34 master slurmd[1802269]: slurmd: child started successfully
Jan 25 20:13:34 master slurmd[1715228]: slurmd: Relinquishing control to new slurmd process (1802269)
Jan 25 20:13:34 master slurmd[1802269]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=203789 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 25 20:15:11 master slurmd[1802269]: slurmd: launch task StepId=210.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:36560
Jan 25 20:15:20 master slurmd[1802269]: slurmd: Launching batch job 214 for UID 0
Jan 25 20:24:10 master slurmd[1802269]: slurmd: launch task StepId=216.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:34318
Jan 25 20:26:19 master slurmd[1843096]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 25 20:26:19 master slurmd[1843096]: slurmd: Resource spec: Reserved abstract CPU IDs: 18-19
Jan 25 20:26:19 master slurmd[1843096]: slurmd: Resource spec: Reserved machine CPU IDs: 9,19
Jan 25 20:26:19 master slurmd[1843096]: slurmd: error: Resource spec: Limited MemSpecLimit support. Slurmd daemon not memory constrained. Reserved 16000 MB
Jan 25 20:26:19 master slurmd[1843096]: slurmd: slurmd version 23.11.3 started
Jan 25 20:26:19 master slurmd[1843096]: slurmd: slurmd started on Sun, 25 Jan 2026 20:26:19 -0500
Jan 25 20:26:19 master slurmd[1843096]: slurmd: child started successfully
Jan 25 20:26:19 master slurmd[1802269]: slurmd: Relinquishing control to new slurmd process (1843096)
Jan 25 20:26:19 master slurmd[1843096]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=204553 CPUSpecList=18-19 FeaturesAvail=(null) FeaturesActive=(null)
Jan 26 09:23:10 master slurmd[1892735]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 26 09:23:10 master slurmd[1892735]: slurmd: slurmd version 23.11.3 started
Jan 26 09:23:10 master slurmd[1892735]: slurmd: slurmd started on Mon, 26 Jan 2026 09:23:10 -0500
Jan 26 09:23:10 master slurmd[1892735]: slurmd: child started successfully
Jan 26 09:23:10 master slurmd[1843096]: slurmd: Relinquishing control to new slurmd process (1892735)
Jan 26 09:23:10 master slurmd[1892735]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=251164 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
Jan 26 09:25:03 master slurmd[1892735]: slurmd: launch task StepId=230.0 request from UID:0 GID:0 HOST:10.195.34.17 PORT:43972
Jan 26 09:25:13 master slurmd[1892735]: slurmd: Launching batch job 234 for UID 0
Jan 26 09:30:46 master slurmd[1931988]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 26 09:30:46 master slurmd[1931988]: slurmd: Resource spec: Reserved abstract CPU IDs: 18-19
Jan 26 09:30:46 master slurmd[1931988]: slurmd: Resource spec: Reserved machine CPU IDs: 9,19
Jan 26 09:30:46 master slurmd[1931988]: slurmd: error: Resource spec: Limited MemSpecLimit support. Slurmd daemon not memory constrained. Reserved 16000 MB
Jan 26 09:30:46 master slurmd[1931988]: slurmd: slurmd version 23.11.3 started
Jan 26 09:30:46 master slurmd[1931988]: slurmd: slurmd started on Mon, 26 Jan 2026 09:30:46 -0500
Jan 26 09:30:46 master slurmd[1931988]: slurmd: child started successfully
Jan 26 09:30:46 master slurmd[1892735]: slurmd: Relinquishing control to new slurmd process (1931988)
Jan 26 09:30:46 master slurmd[1931988]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=251620 CPUSpecList=18-19 FeaturesAvail=(null) FeaturesActive=(null)
Jan 26 11:08:13 master slurmd[1955676]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 26 11:08:13 master slurmd[1955676]: slurmd: Resource spec: Reserved abstract CPU IDs: 18-19
Jan 26 11:08:13 master slurmd[1955676]: slurmd: Resource spec: Reserved machine CPU IDs: 9,19
Jan 26 11:08:13 master slurmd[1955676]: slurmd: error: Resource spec: Limited MemSpecLimit support. Slurmd daemon not memory constrained. Reserved 16000 MB
Jan 26 11:08:13 master slurmd[1955676]: slurmd: slurmd version 23.11.3 started
Jan 26 11:08:13 master slurmd[1955676]: slurmd: slurmd started on Mon, 26 Jan 2026 11:08:13 -0500
Jan 26 11:08:13 master slurmd[1955676]: slurmd: child started successfully
Jan 26 11:08:13 master slurmd[1931988]: slurmd: Relinquishing control to new slurmd process (1955676)
Jan 26 11:08:13 master slurmd[1955676]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=257467 CPUSpecList=18-19 FeaturesAvail=(null) FeaturesActive=(null)
Jan 26 11:10:30 master systemd[1]: Stopping Slurm node daemon...
Jan 26 11:10:30 master slurmd[1955676]: slurmd: Slurmd shutdown completing
Jan 26 11:10:30 master systemd[1]: slurmd.service: Deactivated successfully.
Jan 26 11:10:30 master systemd[1]: Stopped Slurm node daemon.
Jan 26 11:10:30 master systemd[1]: slurmd.service: Consumed 1.389s CPU time, 33.2M memory peak.
Jan 26 11:10:30 master systemd[1]: Starting Slurm node daemon...
Jan 26 11:10:30 master slurmd[1973114]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 26 11:10:30 master slurmd[1973114]: slurmd: Resource spec: Reserved abstract CPU IDs: 18-19
Jan 26 11:10:30 master slurmd[1973114]: slurmd: Resource spec: Reserved machine CPU IDs: 9,19
Jan 26 11:10:30 master slurmd[1973114]: slurmd: error: Resource spec: Limited MemSpecLimit support. Slurmd daemon not memory constrained. Reserved 16000 MB
Jan 26 11:10:30 master slurmd[1973114]: slurmd: slurmd version 23.11.3 started
Jan 26 11:10:30 master slurmd[1973114]: slurmd: slurmd started on Mon, 26 Jan 2026 11:10:30 -0500
Jan 26 11:10:30 master systemd[1]: Started Slurm node daemon.
Jan 26 11:10:30 master slurmd[1973114]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=257605 CPUSpecList=18-19 FeaturesAvail=(null) FeaturesActive=(null)
Jan 26 11:12:02 master systemd[1]: Stopping Slurm node daemon...
Jan 26 11:12:02 master slurmd[1973114]: slurmd: Slurmd shutdown completing
Jan 26 11:12:02 master systemd[1]: slurmd.service: Deactivated successfully.
Jan 26 11:12:02 master systemd[1]: Stopped Slurm node daemon.
Jan 26 11:12:02 master systemd[1]: Starting Slurm node daemon...
Jan 26 11:12:02 master slurmd[1973256]: slurmd: gpu/nvml: _get_system_gpu_list_nvml: 1 GPU system device(s) detected
Jan 26 11:12:02 master slurmd[1973256]: slurmd: Resource spec: Reserved abstract CPU IDs: 18-19
Jan 26 11:12:02 master slurmd[1973256]: slurmd: Resource spec: Reserved machine CPU IDs: 9,19
Jan 26 11:12:02 master slurmd[1973256]: slurmd: error: Resource spec: Limited MemSpecLimit support. Slurmd daemon not memory constrained. Reserved 16000 MB
Jan 26 11:12:02 master slurmd[1973256]: slurmd: slurmd version 23.11.3 started
Jan 26 11:12:02 master slurmd[1973256]: slurmd: slurmd started on Mon, 26 Jan 2026 11:12:02 -0500
Jan 26 11:12:02 master slurmd[1973256]: slurmd: CPUs=20 Boards=1 Sockets=1 Cores=10 Threads=2 Memory=63739 TmpDisk=81856 Uptime=257697 CPUSpecList=18-19 FeaturesAvail=(null) FeaturesActive=(null)
Jan 26 11:12:02 master systemd[1]: Started Slurm node daemon.
```
**Interpretacion breve**
- Eventos recientes de slurmd, incluye NVML/GRES. 

#### 3.19 journalctl -u slurmdbd -n 200
**Comando**
```bash
journalctl -u slurmdbd -n 200 --no-pager || true
```
**Salida**
```text
Jan 24 16:23:22 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 16:23:22 master slurmdbd[1539547]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 24 16:23:22 master slurmdbd[1539547]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 16:23:22 master slurmdbd[1539547]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 16:23:22 master slurmdbd[1539547]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 16:24:11 master slurmdbd[1539547]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 16:24:11 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 16:24:11 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 16:24:11 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 16:24:11 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 16:24:11 master slurmdbd[1550657]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 16:24:11 master slurmdbd[1550657]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 16:24:11 master slurmdbd[1550657]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 16:31:19 master slurmdbd[1550657]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 16:31:19 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 16:31:19 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 16:31:19 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 16:31:19 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 16:31:19 master slurmdbd[1568066]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 24 16:31:19 master slurmdbd[1568066]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 16:31:19 master slurmdbd[1568066]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 16:31:19 master slurmdbd[1568066]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 16:32:06 master slurmdbd[1568066]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 16:32:06 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 16:32:06 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 16:32:06 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 16:32:06 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 16:32:06 master slurmdbd[1579548]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 16:32:06 master slurmdbd[1579548]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 16:32:06 master slurmdbd[1579548]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 16:41:54 master slurmdbd[1579548]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 16:41:54 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 16:41:54 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 16:41:54 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 16:41:54 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 16:41:54 master slurmdbd[1607935]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 24 16:41:54 master slurmdbd[1607935]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 16:41:54 master slurmdbd[1607935]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 16:41:54 master slurmdbd[1607935]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 16:42:40 master slurmdbd[1607935]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 16:42:40 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 16:42:40 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 16:42:40 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 16:42:40 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 16:42:40 master slurmdbd[1619399]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 16:42:40 master slurmdbd[1619399]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 16:42:40 master slurmdbd[1619399]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 16:48:28 master slurmdbd[1619399]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 16:48:28 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 16:48:28 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 16:48:28 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 16:48:28 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 16:48:28 master slurmdbd[1642788]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 24 16:48:28 master slurmdbd[1642788]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 16:48:28 master slurmdbd[1642788]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 16:48:28 master slurmdbd[1642788]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 16:49:15 master slurmdbd[1642788]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 16:49:15 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 16:49:15 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 16:49:15 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 16:49:15 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 16:49:15 master slurmdbd[1654275]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 16:49:15 master slurmdbd[1654275]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 16:49:15 master slurmdbd[1654275]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 17:08:33 master slurmdbd[1654275]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 17:08:33 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 17:08:33 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 17:08:33 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 17:08:33 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 17:08:33 master slurmdbd[1672938]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 24 17:08:33 master slurmdbd[1672938]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 17:08:33 master slurmdbd[1672938]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 17:08:33 master slurmdbd[1672938]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 17:09:19 master slurmdbd[1672938]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 17:09:19 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 17:09:19 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 17:09:19 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 17:09:19 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 17:09:20 master slurmdbd[1684426]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 17:09:20 master slurmdbd[1684426]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 17:09:20 master slurmdbd[1684426]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 18:58:59 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 18:58:59 master slurmdbd[1684426]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 18:58:59 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 18:58:59 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 18:58:59 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 18:58:59 master slurmdbd[1702331]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 24 18:58:59 master slurmdbd[1702331]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 18:58:59 master slurmdbd[1702331]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 18:58:59 master slurmdbd[1702331]: slurmdbd: slurmdbd version 23.11.3 started
Jan 24 18:59:44 master slurmdbd[1702331]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 24 18:59:44 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 24 18:59:44 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 24 18:59:44 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 24 18:59:44 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 24 18:59:44 master slurmdbd[1713842]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 24 18:59:44 master slurmdbd[1713842]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 24 18:59:44 master slurmdbd[1713842]: slurmdbd: slurmdbd version 23.11.3 started
Jan 25 20:02:11 master slurmdbd[1713842]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 25 20:02:11 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 25 20:02:11 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 25 20:02:11 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 25 20:02:11 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 25 20:02:11 master slurmdbd[1749591]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 25 20:02:11 master slurmdbd[1749591]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 25 20:02:11 master slurmdbd[1749591]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 25 20:02:11 master slurmdbd[1749591]: slurmdbd: slurmdbd version 23.11.3 started
Jan 25 20:02:59 master slurmdbd[1749591]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 25 20:02:59 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 25 20:02:59 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 25 20:02:59 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 25 20:02:59 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 25 20:02:59 master slurmdbd[1761051]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 25 20:02:59 master slurmdbd[1761051]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 25 20:02:59 master slurmdbd[1761051]: slurmdbd: slurmdbd version 23.11.3 started
Jan 25 20:07:05 master slurmdbd[1761051]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 25 20:07:05 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 25 20:07:05 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 25 20:07:05 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 25 20:07:05 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 25 20:07:05 master slurmdbd[1784422]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 25 20:07:05 master slurmdbd[1784422]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 25 20:07:05 master slurmdbd[1784422]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 25 20:07:05 master slurmdbd[1784422]: slurmdbd: slurmdbd version 23.11.3 started
Jan 25 20:07:49 master slurmdbd[1784422]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 25 20:07:49 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 25 20:07:49 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 25 20:07:49 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 25 20:07:49 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 25 20:07:49 master slurmdbd[1795905]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 25 20:07:49 master slurmdbd[1795905]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 25 20:07:49 master slurmdbd[1795905]: slurmdbd: slurmdbd version 23.11.3 started
Jan 25 20:23:18 master slurmdbd[1795905]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 25 20:23:18 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 25 20:23:18 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 25 20:23:18 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 25 20:23:18 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 25 20:23:18 master slurmdbd[1829471]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 25 20:23:18 master slurmdbd[1829471]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 25 20:23:18 master slurmdbd[1829471]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 25 20:23:18 master slurmdbd[1829471]: slurmdbd: slurmdbd version 23.11.3 started
Jan 25 20:24:05 master slurmdbd[1829471]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 25 20:24:05 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 25 20:24:05 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 25 20:24:05 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 25 20:24:05 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 25 20:24:05 master slurmdbd[1840952]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 25 20:24:05 master slurmdbd[1840952]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 25 20:24:05 master slurmdbd[1840952]: slurmdbd: slurmdbd version 23.11.3 started
Jan 26 09:21:08 master slurmdbd[1840952]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 26 09:21:08 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 26 09:21:08 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 26 09:21:08 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 26 09:21:08 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 26 09:21:08 master slurmdbd[1874449]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 26 09:21:08 master slurmdbd[1874449]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 26 09:21:08 master slurmdbd[1874449]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 26 09:21:08 master slurmdbd[1874449]: slurmdbd: slurmdbd version 23.11.3 started
Jan 26 09:21:53 master slurmdbd[1874449]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 26 09:21:53 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 26 09:21:53 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 26 09:21:53 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 26 09:21:53 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 26 09:21:53 master slurmdbd[1886020]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 26 09:21:53 master slurmdbd[1886020]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 26 09:21:53 master slurmdbd[1886020]: slurmdbd: slurmdbd version 23.11.3 started
Jan 26 09:28:16 master slurmdbd[1886020]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 26 09:28:16 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 26 09:28:16 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 26 09:28:16 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 26 09:28:16 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 26 09:28:16 master slurmdbd[1919963]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 26 09:28:16 master slurmdbd[1919963]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 26 09:28:16 master slurmdbd[1919963]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 26 09:28:16 master slurmdbd[1919963]: slurmdbd: slurmdbd version 23.11.3 started
Jan 26 09:29:02 master slurmdbd[1919963]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 26 09:29:02 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 26 09:29:02 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 26 09:29:02 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 26 09:29:02 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 26 09:29:02 master slurmdbd[1931457]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 26 09:29:02 master slurmdbd[1931457]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 26 09:29:02 master slurmdbd[1931457]: slurmdbd: slurmdbd version 23.11.3 started
Jan 26 11:08:11 master slurmdbd[1931457]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 26 11:08:11 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 26 11:08:11 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 26 11:08:11 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 26 11:08:11 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 26 11:08:11 master slurmdbd[1955086]: slurmdbd: error: Unable to open pidfile `/run/slurmdbd.pid': Permission denied
Jan 26 11:08:11 master slurmdbd[1955086]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 26 11:08:11 master slurmdbd[1955086]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 26 11:08:11 master slurmdbd[1955086]: slurmdbd: slurmdbd version 23.11.3 started
Jan 26 11:08:55 master slurmdbd[1955086]: slurmdbd: Terminate signal (SIGINT or SIGTERM) received
Jan 26 11:08:55 master systemd[1]: Stopping Slurm DBD accounting daemon...
Jan 26 11:08:55 master systemd[1]: slurmdbd.service: Deactivated successfully.
Jan 26 11:08:55 master systemd[1]: Stopped Slurm DBD accounting daemon.
Jan 26 11:08:55 master systemd[1]: Started Slurm DBD accounting daemon.
Jan 26 11:08:55 master slurmdbd[1966460]: slurmdbd: Not running as root. Can't drop supplementary groups
Jan 26 11:08:55 master slurmdbd[1966460]: slurmdbd: accounting_storage/as_mysql: _check_mysql_concat_is_sane: MySQL server version is: 10.11.15-MariaDB
Jan 26 11:08:56 master slurmdbd[1966460]: slurmdbd: slurmdbd version 23.11.3 started
```
**Interpretacion breve**
- Eventos recientes de slurmdbd (DB/permiso pidfile). 

## 4. Accounting

#### 4.1 sacctmgr -V
**Comando**
```bash
sacctmgr -V || true
```
**Salida**
```text
slurm 23.11.3
```
**Interpretacion breve**
- Version de sacctmgr instalada. 

#### 4.2 sacctmgr show cluster -n -p
**Comando**
```bash
sacctmgr show cluster -n -p || true
```
**Salida**
```text
sacctmgr: error: Error creating slurm stream socket: Operation not permitted
sacctmgr: error: slurm_persist_conn_open_without_init: failed to open persistent connection to host:localhost:6819: Operation not permitted
sacctmgr: error: Sending PersistInit msg: Operation not permitted
```
**Interpretacion breve**
- No verificado: error de conexion persistente a slurmdbd. 

#### 4.3 sacctmgr show account -n -p
**Comando**
```bash
sacctmgr show account -n -p || true
```
**Salida**
```text
sacctmgr: error: Error creating slurm stream socket: Operation not permitted
sacctmgr: error: slurm_persist_conn_open_without_init: failed to open persistent connection to host:localhost:6819: Operation not permitted
sacctmgr: error: Sending PersistInit msg: Operation not permitted
```
**Interpretacion breve**
- No verificado: error de conexion persistente a slurmdbd. 

#### 4.4 sacctmgr show user -n -p
**Comando**
```bash
sacctmgr show user -n -p || true
```
**Salida**
```text
sacctmgr: error: Error creating slurm stream socket: Operation not permitted
sacctmgr: error: slurm_persist_conn_open_without_init: failed to open persistent connection to host:localhost:6819: Operation not permitted
sacctmgr: error: Sending PersistInit msg: Operation not permitted
```
**Interpretacion breve**
- No verificado: error de conexion persistente a slurmdbd. 

#### 4.5 sacct -S today ...
**Comando**
```bash
sacct -S today -o JobID,JobName,Partition,Account,AllocCPUS,ReqMem,State,Elapsed || true
```
**Salida**
```text
sacct: error: Error creating slurm stream socket: Operation not permitted
sacct: error: slurm_persist_conn_open_without_init: failed to open persistent connection to host:localhost:6819: Operation not permitted
sacct: error: Sending PersistInit msg: Operation not permitted
sacct: error: Problem talking to the database: Operation not permitted
```
**Interpretacion breve**
- No verificado: problema al hablar con la base de datos. 

#### 4.6 systemctl status mariadb
**Comando**
```bash
systemctl status mariadb --no-pager || true
```
**Salida**
```text
Failed to connect to bus: Operation not permitted
```
**Interpretacion breve**
- No verificado: fallo al acceder a systemd. 

#### 4.7 ss -lntp | egrep '3306|6819'
**Comando**
```bash
ss -lntp | egrep '3306|6819' || true
```
**Salida**
```text
Cannot open netlink socket: Operation not permitted
LISTEN 0      0                          0.0.0.0:3306       0.0.0.0:*          
LISTEN 0      0                          0.0.0.0:6819       0.0.0.0:*          
LISTEN 0      0                                *:3306             *:*          
```
**Interpretacion breve**
- Puertos DB (3306) y slurmdbd (6819) en escucha. 

## 5. GPU/CUDA

#### 5.1 nvidia-smi
**Comando**
```bash
nvidia-smi || true
```
**Salida**
```text
Failed to initialize NVML: Unknown Error
```
**Interpretacion breve**
- NVML no inicializa; GPU no verificable via nvidia-smi. 

#### 5.2 nvidia-smi -L
**Comando**
```bash
nvidia-smi -L || true
```
**Salida**
```text
Failed to initialize NVML: Unknown Error
```
**Interpretacion breve**
- Listado de GPUs no disponible por fallo NVML. 

#### 5.3 lsmod | egrep 'nvidia|nouveau'
**Comando**
```bash
lsmod | egrep 'nvidia|nouveau' || true
```
**Salida**
```text
nvidia_uvm           2818048  2
nvidia_drm            131072  4
nvidia_modeset       1589248  3 nvidia_drm
nvidia              103497728  61 nvidia_uvm,nvidia_modeset
drm_ttm_helper         16384  1 nvidia_drm
drm_client_lib         16384  2 nvidia_drm,i915
drm_kms_helper        266240  5 drm_display_helper,drm_ttm_helper,nvidia_drm,drm_client_lib,i915
drm                   843776  20 drm_kms_helper,drm_display_helper,nvidia,drm_buddy,drm_ttm_helper,nvidia_drm,drm_client_lib,i915,ttm
video                  77824  3 dell_wmi,i915,nvidia_modeset
```
**Interpretacion breve**
- Modulos NVIDIA cargados en el kernel. 

#### 5.4 nvcc --version
**Comando**
```bash
nvcc --version || true
```
**Salida**
```text
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Thu_Mar_28_02:18:24_PDT_2024
Cuda compilation tools, release 12.4, V12.4.131
Build cuda_12.4.r12.4/compiler.34097967_0
```
**Interpretacion breve**
- Toolkit CUDA presente (version del compilador). 

#### 5.5 ldconfig -p | egrep 'cuda|cudart|cublas'
**Comando**
```bash
ldconfig -p | egrep 'cuda|cudart|cublas' | head -n 200 || true
```
**Salida**
```text
	libpcsamplingutil.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libpcsamplingutil.so
	libnvrtc.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvrtc.so.12
	libnvrtc.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvrtc.so
	libnvrtc-builtins.so.12.4 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvrtc-builtins.so.12.4
	libnvrtc-builtins.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvrtc-builtins.so
	libnvperf_target.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvperf_target.so
	libnvperf_host.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvperf_host.so
	libnvjpeg.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvjpeg.so.12
	libnvjpeg.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvjpeg.so
	libnvfatbin.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvfatbin.so.12
	libnvfatbin.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvfatbin.so
	libnvblas.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvblas.so.12
	libnvblas.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvblas.so
	libnvToolsExt.so.1 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvToolsExt.so.1
	libnvToolsExt.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvToolsExt.so
	libnvJitLink.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvJitLink.so.12
	libnvJitLink.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnvJitLink.so
	libnpps.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnpps.so.12
	libnpps.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnpps.so
	libnppitc.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppitc.so.12
	libnppitc.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppitc.so
	libnppisu.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppisu.so.12
	libnppisu.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppisu.so
	libnppist.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppist.so.12
	libnppist.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppist.so
	libnppim.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppim.so.12
	libnppim.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppim.so
	libnppig.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppig.so.12
	libnppig.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppig.so
	libnppif.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppif.so.12
	libnppif.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppif.so
	libnppidei.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppidei.so.12
	libnppidei.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppidei.so
	libnppicc.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppicc.so.12
	libnppicc.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppicc.so
	libnppial.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppial.so.12
	libnppial.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppial.so
	libnppc.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppc.so.12
	libnppc.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libnppc.so
	libicudata.so.67 (libc6,x86-64) => /lib64/libicudata.so.67
	libgstcuda-1.0.so.0 (libc6,x86-64) => /lib64/libgstcuda-1.0.so.0
	libcusparse.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcusparse.so.12
	libcusparse.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcusparse.so
	libcusolverMg.so.11 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcusolverMg.so.11
	libcusolverMg.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcusolverMg.so
	libcusolver.so.11 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcusolver.so.11
	libcusolver.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcusolver.so
	libcurand.so.10 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcurand.so.10
	libcurand.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcurand.so
	libcupti.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcupti.so.12
	libcupti.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcupti.so
	libcuinj64.so.12.4 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcuinj64.so.12.4
	libcuinj64.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcuinj64.so
	libcufile_rdma.so.1 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcufile_rdma.so.1
	libcufile_rdma.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcufile_rdma.so
	libcufile.so.0 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcufile.so.0
	libcufile.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcufile.so
	libcufftw.so.11 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcufftw.so.11
	libcufftw.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcufftw.so
	libcufft.so.11 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcufft.so.11
	libcufft.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcufft.so
	libcudart.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcudart.so.12
	libcudart.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcudart.so
	libcudadebugger.so.1 (libc6,x86-64) => /lib64/libcudadebugger.so.1
	libcuda.so.1 (libc6,x86-64) => /lib64/libcuda.so.1
	libcuda.so (libc6,x86-64) => /lib64/libcuda.so
	libcublasLt.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcublasLt.so.12
	libcublasLt.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcublasLt.so
	libcublas.so.12 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcublas.so.12
	libcublas.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcublas.so
	libcheckpoint.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libcheckpoint.so
	libaccinj64.so.12.4 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libaccinj64.so.12.4
	libaccinj64.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libaccinj64.so
	libOpenCL.so.1 (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libOpenCL.so.1
	libOpenCL.so (libc6,x86-64) => /usr/local/cuda/targets/x86_64-linux/lib/libOpenCL.so
```
**Interpretacion breve**
- Bibliotecas CUDA detectadas en el linker cache. 

**Nota sobre GRES GPU en Slurm**
- slurm.conf declara GresTypes=gpu y nodos con Gres=gpu:quadro_p1000:1.
- host_vars/worker1.yml y host_vars/worker2.yml fijan slurm_node_gres a gpu:quadro_p1000:1.
- La verificacion via scontrol/sinfo no fue posible (errores de socket).

## 6. SSH y acceso

#### 6.1 sshd -T | egrep ...
**Comando**
```bash
sshd -T | egrep 'passwordauthentication|pubkeyauthentication|permitrootlogin' || true
```
**Salida**
```text
/etc/ssh/sshd_config: Permission denied
```
**Interpretacion breve**
- No verificado: sshd -T no pudo leer /etc/ssh/sshd_config. 

#### 6.2 grep sshd_config / sshd_config.d
**Comando**
```bash
grep -nE 'PasswordAuthentication|PubkeyAuthentication|PermitRootLogin' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null || true
```
**Salida**
```text
/etc/ssh/sshd_config.d/99-hpc.conf:3:PermitRootLogin yes
/etc/ssh/sshd_config.d/99-hpc.conf:4:PasswordAuthentication yes
/etc/ssh/sshd_config.d/99-hpc.conf:5:PubkeyAuthentication yes
/etc/ssh/sshd_config.d/99-hpc.conf:11:    PasswordAuthentication yes
/etc/ssh/sshd_config.d/99-hpc.conf:13:    PubkeyAuthentication yes
```
**Interpretacion breve**
- Drop-in 99-hpc.conf indica PermitRootLogin y PasswordAuthentication en yes. 

## 7. Resumen ejecutivo, riesgos y proximos pasos

### Resumen ejecutivo
- Repo en rama `llm`, commit `f1b32c29d0fac46620e2dbb1eda18e5113e9d8c0`. 
- SO del master: Rocky Linux 9.7 (segun /etc/os-release). 
- CPU del master: Intel Xeon W-1290, 20 CPUs logicas (10C/20T), RAM ~62GiB. 
- Particiones en slurm.conf: `debug` (master,worker1,worker2) y `gpu` (worker1,worker2). 
- GRES declarado: `gpu:quadro_p1000:1` en master/worker1/worker2; AutoDetect=nvml en gres.conf. 
- Slurm CLI instalada (23.11.3) pero consultas a slurmctld fallan por socket (Operation not permitted). 
- Puertos en escucha: 6817/6818/6819 (Slurm), 3306 (MariaDB), 2049/111/20048 (NFS). 
- nvidia-smi falla (NVML), pero modulos NVIDIA estan cargados y CUDA toolkit 12.4 disponible. 
- Logs de slurmd muestran avisos de GRES/CoreSpec en worker1 y reinicios de slurmdbd con pidfile sin permisos. 
- Sin acceso verificado a workers ni a systemd/dbus desde esta sesion. 

### Lo que ya esta funcionando (checklist)
- [ ] Slurmctld/slurmd activos y accesibles via CLI (no verificado desde este usuario).
- [ ] Puertos Slurm y MariaDB en escucha en el master (evidencia via ss).
- [ ] slurm.conf/gres.conf/cgroup.conf presentes en /etc/slurm. 
- [ ] CUDA toolkit instalado (nvcc 12.4, libs en /usr/local/cuda).
- [ ] SSH configurado con drop-in 99-hpc.conf (PermitRootLogin/PasswordAuthentication).

### Lo que falta / incertidumbres (checklist)
- [ ] Verificar estado real de slurmctld/slurmd/slurmdbd via systemctl (dbus sin permisos).
- [ ] Verificar topologia y estado de nodos con sinfo/scontrol (error de socket).
- [ ] Verificar accounting con sacctmgr/sacct (conexion persistente a slurmdbd falla).
- [ ] Verificar interfaces/red/rutas (ip -br a / ip r fallan por netlink).
- [ ] Verificar exportaciones NFS (showmount falla por permisos).
- [ ] Verificar NVML/nvidia-smi funcionando en master (actualmente falla).

### Riesgos tecnicos
- Slurm CLI no puede comunicarse con slurmctld desde este usuario; posible problema de permisos o slurmctld caido. 
- slurmd log indica CoreSpec/MemSpec invalidos para worker1 (posible mismatch de recursos). 
- slurmdbd reporta `Unable to open pidfile` y `Not running as root`; riesgo de accounting inestable. 
- NVML falla pese a modulos cargados; GPU puede no estar disponible para jobs. 
- SSH permite PasswordAuthentication y PermitRootLogin (riesgo de seguridad si no esta controlado). 

### Prerequisitos para stress tests CPU/GPU
- Confirmar slurmctld/slurmd activos y accesibles desde CLI en master.
- Confirmar particiones `debug` y `gpu` visibles en `sinfo`.
- Verificar GRES GPU con `scontrol show node` y/o `sinfo -o '%N %G'`.
- Confirmar accounting operativo si se requiere medicion via sacct.
- Validar NVML/nvidia-smi funcional en nodos GPU. 

### Propuesta de bateria de pruebas (plan, no ejecutado)
- CPU: `stress-ng` via sbatch (n=1 nodo, CPU 100%, 10-30 min) y medir con `sstat`/`sacct`. 
- CPU: `srun -N1 -n1 -p debug hostname` y `srun -N1 -n1 -p debug stress-ng --cpu 20 --timeout 300s`. 
- GPU: `nvidia-smi dmon` en nodo GPU durante un job `srun --gres=gpu:1`.
- GPU: smoke PyTorch CUDA (si env LLM existe) y `nvidia-smi -L` dentro del job.
- Medicion: `sacct -j <jobid> -o JobID,State,Elapsed,AllocCPUS,ReqMem` y `sstat -j <jobid>.batch`. 
