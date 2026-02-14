# Referencia de roles

Este documento cubre todos los roles activos bajo `roles/`.

## common

- Proposito: baseline de paquetes y tiempo.
- Archivos:
  - `roles/common/tasks/main.yml`
- Entradas: `common_packages`, `enable_chrony`.
- Salidas: paquetes base instalados, `chronyd` activo si aplica.
- Notas: rol simple e idempotente con `dnf`.

## users_ssh

- Proposito: gestion de `sshd` mediante drop-in `99-hpc.conf`.
- Archivos:
  - `roles/users_ssh/defaults/main.yml`
  - `roles/users_ssh/tasks/main.yml`
  - `roles/users_ssh/handlers/main.yml`
- Entradas: `ssh_*`.
- Salidas: include de `sshd_config.d`, politicas de auth, restart de `sshd` cuando cambia config.
- Validacion interna: `sshd -t`.

## firewall

- Proposito: habilitar `firewalld` y reglas Slurm.
- Archivos:
  - `roles/firewall/tasks/main.yml`
- Entradas: `slurm_firewalld_zone`, `slurm_internal_cidr`, `slurmctld_port`, `slurmd_port`.
- Salidas: reglas ricas para 6817/6818 por CIDR interno.
- Riesgo: reglas aplicadas por grupos de inventario; revisar que grupos representen topologia real.

## network_internal

- Proposito: declarar enlaces internos por `nmcli` y mantener `/etc/hosts`.
- Archivos:
  - `roles/network_internal/defaults/main.yml`
  - `roles/network_internal/tasks/main.yml`
  - `roles/network_internal/tasks/master_link.yml`
- Entradas: `network_internal_keep_if`, `network_internal_links`, exclusiones.
- Nota (P11b): los valores lab-specific (NICs/IPs) se definen en `group_vars/all/vars.yml` para facilitar replicación; el defaults del rol queda intencionalmente vacío.
- Salidas:
  - conexiones `int-*` creadas/ajustadas,
  - conexiones no permitidas eliminadas,
  - bloque administrado en `/etc/hosts`.
- Riesgo: cambios de red en vivo; usar `--limit` y validar conectividad antes de masificar.

## cluster_routing

- Proposito: ruteo entre subredes via master.
- Archivos:
  - `roles/cluster_routing/tasks/main.yml`
- Entradas: `hpc_router_internal_ifaces`, `hpc_internal_supernet`, `hpc_internal_subnets`.
- Salidas:
  - `net.ipv4.ip_forward=1` en master,
  - zona `trusted` en firewall,
  - rutas persistentes en workers por `nmcli`.
- Detalle: calcula gateway como `network_address + 1` por subred local del worker.

## nfs_hpc

- Proposito: export NFS en server y montaje en clientes.
- Archivos:
  - `roles/nfs_hpc/defaults/main.yml`
  - `roles/nfs_hpc/tasks/main.yml`
  - `roles/nfs_hpc/handlers/main.yml`
  - `roles/nfs_hpc/templates/exports.j2`
- Entradas: `nfs_hpc_server_enabled`, `nfs_hpc_client_enabled`, share, permisos y opts.
- Salidas:
  - paquete/servicio NFS,
  - archivo export,
  - puerto 2049/tcp,
  - montaje persistente en clientes.

## nvidia_cuda

- Proposito: deteccion GPU, instalacion driver/CUDA, mitigacion `nouveau`, validacion NVML.
- Archivos:
  - `roles/nvidia_cuda/defaults/main.yml`
  - `roles/nvidia_cuda/tasks/main.yml`
  - `roles/nvidia_cuda/handlers/main.yml`
- Entradas clave:
  - `nvidia_driver_stream` (default `580-dkms`),
  - `nvidia_cuda_reboot`, `nvidia_cuda_repo_enabled`, `nvidia_cuda_validate`.
- Flujo tecnico:
  - detecta GPU (`lspci`), termina host si no hay GPU,
  - configura repos CUDA (RHEL/Ubuntu),
  - fuerza stream de driver,
  - instala prerequisitos DKMS y headers,
  - remueve paquetes conflictivos (`open`, `590`),
  - instala driver,
  - aplica blacklist de `nouveau` + initramfs/grub,
  - calcula si requiere reboot y lo programa via handler,
  - valida `nvidia-smi`, modulos y NVML,
  - crea symlink `libnvidia-ml.so` cuando falta (impacta Slurm NVML).
- Salidas adicionales:
  - fact `slurm_nvml_symlink_changed` para reinicios/reconfigure Slurm.
- Riesgo: puede requerir reinicio de host y tocar boot args.

## llm_env

- Proposito: instalar micromamba y construir entorno `llm` con PyTorch CUDA.
- Archivos:
  - `roles/llm_env/defaults/main.yml`
  - `roles/llm_env/tasks/main.yml`
- Entradas: `llm_micromamba_*`, `llm_env_name`, `llm_conda_channels`, `llm_conda_packages`, `llm_pip_packages`.
- Salidas:
  - micromamba en `/opt/micromamba` y symlink en `/usr/local/bin`,
  - env con paquetes conda,
  - stack `pytorch-cuda=12.4`,
  - helper `llm-env-check`.
- Guardrails:
  - falla si `llm_pip_packages` incluye `torch` para evitar sobreescritura del stack CUDA.

## mariadb_server

- Proposito: instalar/arrancar MariaDB y validar version minima.
- Archivos:
  - `roles/mariadb_server/defaults/main.yml`
  - `roles/mariadb_server/tasks/main.yml`
- Entradas: `mariadb_min_version_major`.
- Salidas: servicio `mariadb` activo, assert de version.

## slurm_db_prep

- Proposito: preparar DB y grants para `slurmdbd`.
- Archivos:
  - `roles/slurm_db_prep/tasks/main.yml`
  - `roles/slurm_db_prep/handlers/main.yml`
- Entradas: `slurmdb_mysql_*`, `mariadb_slurm_tuning`.
- Salidas:
  - `/etc/my.cnf.d/slurm.cnf`,
  - DB y usuarios,
  - grants aplicados,
  - verificacion de acceso.
- Seguridad: tareas con password usan `no_log: true` en puntos criticos.

## validate

- Proposito: validacion general (SO, SSH, NVIDIA, Torch CUDA).
- Archivos:
  - `roles/validate/defaults/main.yml`
  - `roles/validate/tasks/main.yml`
  - `roles/validate/tasks/slurm.yml` (actualmente no incluido por default en `main.yml`).
- Entradas: `validate_cuda`, `validate_llm`, `llm_*`.
- Salidas: evidencia de estado via `debug` y `fail` cuando no cumple.

## slurm_identities

- Proposito: usuarios/grupos del sistema para `munge` y `slurm` con UID/GID declarados.
- Archivos:
  - `roles/slurm_identities/tasks/main.yml`
- Entradas: `munge_uid`, `munge_gid`, `slurm_uid`, `slurm_gid`.
- Salidas: cuentas del sistema consistentes entre nodos.

## munge

- Proposito: instalar/configurar Munge y distribuir `munge.key`.
- Archivos:
  - `roles/munge/tasks/main.yml`
  - `roles/munge/handlers/main.yml`
- Entradas: `munge_key_host`, `munge_key_size_mb`.
- Salidas:
  - dirs/permisos correctos,
  - tmpfiles de `/run/munge`,
  - key generada en host fuente y distribuida a todos,
  - servicio `munge` activo.

## slurm_facts

- Proposito: derivar CPU/mem/GPU por nodo para templating Slurm.
- Archivos:
  - `roles/slurm_facts/tasks/main.yml`
- Entradas: facts Ansible + overrides `slurm_*`.
- Salidas:
  - `slurm_node_name`, `slurm_cpus`, `slurm_real_memory`,
  - `slurm_gpu_count`, `slurm_gpu_type_*`, `slurm_node_gres`.

## slurm_rpm_build

- Proposito: construir RPMs Slurm desde tarball (RHEL/Rocky).
- Archivos:
  - `roles/slurm_rpm_build/tasks/main.yml`
- Entradas: `slurm_tarball_url`, `slurm_version`.
- Salidas: RPMs en `/root/rpmbuild/RPMS/x86_64` con marca `.slurm_<version>_built`.

## slurm_install

- Proposito: instalar paquetes Slurm, desplegar `slurm.conf`/`gres.conf`, higiene `slurmdbd`.
- Archivos:
  - `roles/slurm_install/defaults/main.yml`
  - `roles/slurm_install/tasks/main.yml`
  - `roles/slurm_install/tasks/slurmdbd_hygiene.yml`
  - `roles/slurm_install/handlers/main.yml`
  - `roles/slurm_install/templates/slurm.conf.j2`
  - `roles/slurm_install/templates/gres.conf.j2`
  - `roles/slurm_install/files/slurm.conf` (referencia historica).
- Flujo tecnico:
  - en master instala RPMs locales,
  - baja RPMs al controller y los distribuye a workers,
  - en workers instala RPMs staged,
  - asegura `/etc/slurm` y `cgroup.conf`,
  - abre `SrunPortRange` en firewall del controller,
  - renderiza `slurm.conf` en master y lo copia a workers,
  - genera `gres.conf` por nodo,
  - registra flags de cambio (`slurm_conf_changed`, `slurm_gres_conf_changed`),
  - aplica higiene de `slurmdbd` (`/run/slurm`, `PidFile`, `SlurmUser`).

## slurm_controller

- Proposito: gestionar `slurmctld` y `slurmdbd` en master.
- Archivos:
  - `roles/slurm_controller/defaults/main.yml`
  - `roles/slurm_controller/tasks/main.yml`
  - `roles/slurm_controller/templates/slurmdbd.conf.j2`
- Entradas:
  - `slurm_controller_reconfigure_*`,
  - `slurm_controller_autoresume_*`,
  - variables `slurmdbd_*`.
- Salidas:
  - config `slurmdbd.conf`, servicios activos,
  - `scontrol reconfigure` condicional,
  - autoresume de nodos en `DRAIN`/`INVALID_REG` segun reglas.

## slurm_compute

- Proposito: gestionar `slurmd` y estructura local en compute.
- Archivos:
  - `roles/slurm_compute/tasks/main.yml`
- Entradas: `slurm_log_dir` y flags de cambio de config.
- Salidas:
  - spool/logs de `slurmd`,
  - servicio `slurmd` habilitado,
  - restart condicional si cambia config/NVML.
- Detalle: detecta si existe `slurmd.service` antes de gestionarlo.

## slurm_validate

- Proposito: validacion read-only de Slurm y smoke jobs CPU/GPU.
- Archivos:
  - `roles/slurm_validate/defaults/main.yml`
  - `roles/slurm_validate/tasks/main.yml`
  - `roles/slurm_validate/templates/slurm-smoke-cpu.sbatch.j2`
  - `roles/slurm_validate/templates/slurm-smoke-gpu.sbatch.j2`
- Entradas:
  - `slurm_validate_partitions.*`,
  - `slurm_validate_smoke.*`,
  - `slurm_validate_torch.*`.
- Salidas:
  - comprobacion de CLI, particiones y estados,
  - ejecucion de `srun` CPU/GPU,
  - smoke `sbatch` CPU/GPU con verificacion `sacct` `COMPLETED|0:0`,
  - logs stdout/stderr recuperados para evidencia.
