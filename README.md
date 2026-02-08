# Automatización de un clúster HPC con Ansible

Este repositorio automatiza el despliegue y operación de un clúster HPC con nodo
`master` y nodos `workers`, incluyendo:

- configuración base de SO y SSH,
- red interna y ruteo entre subredes,
- firewall,
- NFS compartido,
- drivers NVIDIA/CUDA,
- entorno LLM con micromamba,
- Slurm completo (identidades, munge, build/instalación, controller/compute),
- validaciones de salud y smoke tests CPU/GPU.

## Tabla de contenido

- [Objetivo y alcance](#objetivo-y-alcance)
- [Arquitectura de automatización](#arquitectura-de-automatización)
- [Requisitos](#requisitos)
- [Tutorial rápido](#tutorial-rápido)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Guía de roles](#guía-de-roles)
- [Inventario y variables](#inventario-y-variables)
- [Tags más usados](#tags-más-usados)
- [Validación e idempotencia](#validación-e-idempotencia)
- [Operación segura en HPC](#operación-segura-en-hpc)

## Objetivo y alcance

El enfoque es **infraestructura declarativa** con Ansible para evitar cambios
manuales no trazables. El playbook principal es `site.yml`, que aplica
configuración por capas y luego valida estado.

`base.yml` existe como pre-flight simple para tareas base de sistema.

## Arquitectura de automatización

`site.yml` ejecuta, en orden lógico:

1. Baseline para todos los nodos (`common`, `users_ssh`, `firewall`,
   `network_internal`, `cluster_routing`, `nfs_hpc`, `nvidia_cuda`, `llm_env`).
2. Servicios de base de datos y preparación de SlurmDB en `master`
   (`mariadb_server`, `slurm_db_prep`).
3. Validación general (`validate`).
4. Capa Slurm:
   - identidades (`slurm_identities`),
   - autenticación de cluster (`munge`),
   - facts de hardware para templating (`slurm_facts`),
   - build + instalación de paquetes y configs (`slurm_rpm_build`, `slurm_install`),
   - control plane (`slurm_controller`),
   - compute plane (`slurm_compute`),
   - validación read-only de Slurm (`slurm_validate`).

## Requisitos

- Ansible Core instalado en el controlador.
- Acceso SSH al inventario con permisos de `become` según corresponda.
- Colecciones requeridas:

```bash
ansible-galaxy collection install -r requirements.yml
```

El repositorio usa como inventario por defecto `inventario.ini` (definido en
`ansible.cfg`).

## Tutorial rápido

### 1) Revisar inventario y variables

Edita según tu entorno:

- `inventario.ini`
- `group_vars/all.yml`
- `group_vars/hpc_master.yml`
- `host_vars/*.yml`

### 2) Verificar inventario y sintaxis

```bash
ansible-inventory -i inventario.ini --graph
ansible-playbook -i inventario.ini site.yml --syntax-check
```

### 3) Ejecutar dry-run controlado

Primero sobre un nodo o grupo pequeño:

```bash
ansible-playbook -i inventario.ini site.yml --check --diff --limit worker1
```

### 4) Aplicar baseline por capas

```bash
ansible-playbook -i inventario.ini site.yml --tags common,ssh,firewall,network,routing,nfs,cuda,llm --limit all
```

### 5) Aplicar Slurm en orden seguro

Master primero:

```bash
ansible-playbook -i inventario.ini site.yml --tags slurm,munge,identities,slurm_config,slurm_install --limit hpc_master
```

Workers después:

```bash
ansible-playbook -i inventario.ini site.yml --tags slurm,munge,identities,slurm_config,slurm_install --limit slurm_compute
```

### 6) Ejecutar validaciones

Validación general:

```bash
ansible-playbook -i inventario.ini site.yml --tags validate --limit all
```

Validación Slurm (read-only + smoke jobs CPU/GPU):

```bash
ansible-playbook -i inventario.ini site.yml --tags slurm_validate --limit hpc_master
```

### 7) Confirmar idempotencia

```bash
ansible-playbook -i inventario.ini site.yml --check --diff
```

## Estructura del repositorio

### Raíz

- `site.yml`: orquestación completa del clúster por capas.
- `base.yml`: pre-flight básico para preparar nodos.
- `ansible.cfg`: configuración por defecto de Ansible (incluye inventario).
- `inventario.ini`: grupos de hosts (`hpc_master`, `workers`, `slurm_*`).
- `requirements.yml`: colecciones Ansible requeridas.
- `group_vars/`: variables por alcance de grupo.
- `host_vars/`: overrides por host.
- `roles/`: automatización modular por dominio funcional.
- `AGENTS.md`: guía operativa del repositorio para trabajo asistido.

### `group_vars/`

- `group_vars/all.yml`:
  - paquetes base,
  - políticas SSH,
  - configuración LLM (conda/pip),
  - puertos/firewall de Slurm,
  - IDs de usuarios Slurm/Munge,
  - versión/plantillas de Slurm,
  - particiones (`debug`, `gpu`),
  - parámetros de red interna y subredes.
- `group_vars/hpc_master.yml`:
  - configuración del master como router interno,
  - stream de MariaDB,
  - habilitación del servidor NFS,
  - parámetros de SlurmDBD/MySQL.

### `host_vars/`

Overrides puntuales por nodo, por ejemplo reservas de CPU/memoria para Slurm
sin provocar `INVALID_REG`.

### `roles/`

Cada rol mantiene estructura estándar (`tasks/`, `defaults/`, `handlers/`,
`templates/` según aplique).

## Guía de roles

| Rol | Propósito principal |
|---|---|
| `common` | Paquetes base y sincronización de tiempo (`chrony`). |
| `users_ssh` | Endurece/ajusta `sshd` vía drop-in (`/etc/ssh/sshd_config.d/99-hpc.conf`). |
| `firewall` | Activa `firewalld`, abre SSH y reglas Slurm (6817/6818) por CIDR interno. |
| `network_internal` | Configura enlaces internos con `nmcli`, limpia conexiones no deseadas y mantiene `/etc/hosts` del cluster. |
| `cluster_routing` | Habilita forwarding en `master` y rutas persistentes entre subredes en workers. |
| `nfs_hpc` | Gestiona export NFS en servidor y montaje persistente en clientes. |
| `nvidia_cuda` | Detecta GPU NVIDIA, configura repos, instala driver/CUDA y valida `nvidia-smi`/NVML. |
| `llm_env` | Instala micromamba y crea/actualiza entorno `llm` con stack PyTorch CUDA. |
| `mariadb_server` | Instala y arranca MariaDB en el master, validando versión mínima. |
| `slurm_db_prep` | Prepara DB/usuarios/permisos para accounting de Slurm (`slurmdbd`). |
| `validate` | Validaciones de salud generales (SO, SSH efectivo, NVIDIA, Torch CUDA). |
| `slurm_identities` | Crea usuarios y grupos del sistema para `munge` y `slurm` con UID/GID declarados. |
| `munge` | Genera/distribuye `munge.key`, permisos y servicio `munge` en todos los nodos Slurm. |
| `slurm_facts` | Deriva facts de CPU/memoria/GPU para renderizar `slurm.conf`/`gres.conf`. |
| `slurm_rpm_build` | Construye RPMs de Slurm en plataformas Rocky/RHEL. |
| `slurm_install` | Instala paquetes Slurm, despliega `slurm.conf` y `gres.conf`, y aplica higiene `slurmdbd`. |
| `slurm_controller` | Configura `slurmctld`/`slurmdbd` en master, reconfigure y autoresume de nodos. |
| `slurm_compute` | Gestiona `slurmd` en nodos compute (enable/start/restart/verificación). |
| `slurm_validate` | Validación read-only de Slurm: particiones, estados, `srun`, `sbatch`, `sacct`, smoke CPU/GPU y prueba opcional Torch. |

## Inventario y variables

### Grupos de inventario relevantes

- `hpc_master`: nodo controlador.
- `workers`: conjunto de workers.
- `slurm_all`: nodos en dominio Slurm.
- `slurm_compute`: nodos donde corre `slurmd`.
- `slurm_gpu`: nodos habilitados para partición GPU.

### Variables importantes a ajustar

- Slurm:
  - `slurm_version`, `slurm_control_machine`, `slurm_partitions`,
    `slurm_srun_port_range`.
- Munge/identidades:
  - `munge_uid`, `munge_gid`, `slurm_uid`, `slurm_gid`, `munge_key_host`.
- Red/firewall:
  - `slurm_internal_cidr`, `hpc_internal_supernet`, `hpc_internal_subnets`,
    `hpc_router_internal_ifaces`.
- NFS:
  - `nfs_hpc_server_enabled`, `nfs_hpc_share_dir`, `nfs_hpc_server_host`.
- LLM/CUDA:
  - `llm_env_name`, `llm_conda_packages`, `llm_pip_packages`,
    `nvidia_driver_stream`.

> [!IMPORTANT]
> Para entornos sensibles, mueve secretos a Ansible Vault (por ejemplo, claves o
> passwords actualmente definidos como texto plano en variables/inventario).

## Tags más usados

- Baseline: `common`, `ssh`, `firewall`, `network`, `routing`, `nfs`,
  `cuda`, `llm`
- Datos/DB: `mariadb`, `slurmdb`
- Slurm: `slurm`, `slurm_install`, `slurm_config`, `slurmd`, `slurmctld`,
  `slurmdbd`
- Validación: `validate`, `slurm_validate`, `slurm_validate_smoke`

Ejemplos:

```bash
ansible-playbook -i inventario.ini site.yml --tags cuda --limit worker1
ansible-playbook -i inventario.ini site.yml --tags slurm_validate --limit hpc_master
ansible-playbook -i inventario.ini site.yml --tags validate --limit all
```

## Validación e idempotencia

Flujo recomendado antes de cambios amplios:

1. `--syntax-check`
2. `--check --diff` con `--limit` acotado
3. ejecución real por etapas
4. validación con `validate` y `slurm_validate`
5. nueva pasada `--check --diff` para confirmar idempotencia

## Operación segura en HPC

- Evita cambios simultáneos de servicios críticos en todos los nodos.
- Aplica `--limit` para despliegues graduales.
- Prefiere validaciones read-only para confirmar estado antes de tocar
  configuración.
- Mantén firewall/Slurm/NFS como configuración declarativa dentro de Ansible.
