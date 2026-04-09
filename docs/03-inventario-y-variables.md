# Inventario y variables

## Inventario principal

Archivo: `inventario.ini`

Grupos observados:
- `hpc_master`: nodo master.
- `workers_r`: workers con Rocky/RHEL.
- `workers_u`: workers con Ubuntu/Debian (requieren `ansible_become_password`).
- `workers`: union de workers.
- `slurm_all`: nodos considerados por dominio Slurm.
- `slurm_compute`: nodos donde corre `slurmd`.
- `slurm_gpu`: subset con GPUs para particion GPU.

Nota operativa:
- En el estado actual, `slurm_compute` incluye `master`, por lo que el master puede recibir configuracion compute de Slurm.

## Variables globales

Archivo: `group_vars/all/vars.yml`

Bloques clave:
- Baseline:
  - `common_packages`
  - `enable_chrony`
- SSH:
  - `ssh_port`, `ssh_permit_root_login`, `ssh_password_authentication`
- LLM:
  - `llm_conda_packages`, `llm_pip_packages`, `llm_python_packages`
- NFS:
  - `nfs_export_path` (export en master)
  - `nfs_client_mountpoint` (mountpoint en workers)
  - `nfs_server_ip` (prioriza `network_internal_links[<worker>].master_ip` por enlace punto-a-punto; fallback a `ansible_host` del master)
- Firewall Slurm:
  - `slurm_firewalld_zone`, `slurm_internal_cidr`, `slurmctld_port`, `slurmd_port`
- Identidades:
  - `munge_uid`, `munge_gid`, `slurm_uid`, `slurm_gid`, `munge_key_host`
- Slurm:
  - `slurm_version`, `slurm_tarball_url`, `slurm_etc_dir`, `slurm_log_dir`
  - `slurm_control_machine`, `slurm_mem_reserve_mb`, `slurm_partitions`
  - `slurm_srun_port_range`, `slurm_validate_torch`
  - `slurm_cgroup_conf`
- Red interna:
  - `hpc_internal_supernet`, `hpc_internal_subnets`
  - `network_internal_links` (mapa de topologia master<->worker: NIC e IP por extremo)
  - `network_internal_keep_if` (interfaz a preservar siempre)
  - `network_internal_exclude_ifaces` (interfaces excluidas de gestion)
  - `network_internal_exclude_conn_regex` (patron regex para conexiones excluidas)

## Variables de master

Archivo: `group_vars/hpc_master.yml`

Bloques clave:
- Ruteo master:
  - `hpc_router_internal_ifaces`
- MariaDB:
  - `mariadb_module_stream`
- NFS:
  - `nfs_hpc_server_enabled`
- SlurmDBD:
  - `slurmdb_mysql_db`, `slurmdb_mysql_user`, `slurmdb_mysql_password`
  - `slurmdb_mysql_hosts`
  - `mariadb_slurm_tuning`
  - `slurmdbd_port`, `slurmdbd_host`, `slurmdbd_storage_*`
  - `slurmdb_mysql_user` admite string o lista; internamente se normaliza y `slurmdbd_storage_user` usa el primer usuario efectivo.

## Variables por host

Archivos:
- `host_vars/master.yml`
- `host_vars/worker1.yml`
- `host_vars/worker2.yml`

Estado actual:
- Son ejemplos comentados para reservar recursos Slurm (`slurm_core_spec_count`, `slurm_mem_spec_limit_mb`, `slurm_node_gres`).

## Recomendaciones de gestion de variables

- Mantener defaults en `defaults/main.yml` de cada rol y overrides en `group_vars/` o `host_vars/`.
- Evitar hardcode de valores de red/GPU fuera de variables.
- Mantener credenciales sensibles acotadas a los archivos donde realmente se consumen.
