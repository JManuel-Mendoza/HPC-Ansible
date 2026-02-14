# Vars Map (P11a) - Variables operacionales y replicabilidad

Objetivo: documentar, de forma verificable, qué variables controlan la topología/operación del clúster y dónde se definen/consumen, para replicar este repositorio en otro laboratorio sin tocar roles.

Alcance:
- Inventario: `inventario.ini`
- Variables: `group_vars/`, `host_vars/`
- Uso aproximado: búsqueda estática (grep/rg) en `roles/` y `site.yml`
- Vault: solo se referencia (no se abre ni se edita aquí).

## Precedencia (resumen)

Regla práctica (de mayor a menor):
- `host_vars/<host>.yml`
- `group_vars/<grupo>.yml`
- `group_vars/all/*.yml` y `group_vars/all.yml`
- `roles/<rol>/defaults/main.yml`

Implicación: si un valor existe en `host_vars/`, no se debe “centralizar” a `all` porque eso cambia cómo se sobreescribe en el futuro (aunque el valor actual sea igual).

## Qué editar para replicar otro HPC (mínimo)

1. `inventario.ini`
- Hosts (`ansible_host`, `ansible_user`) y pertenencia a grupos (`hpc_master`, `workers_*`, `slurm_*`).
- Variables de conexión globales en `[all:vars]` (p. ej. `ansible_ssh_private_key_file`).
- Secretos de become por grupo apuntan a Vault (ej. `vault_ansible_become_password_workers_u`).

2. `group_vars/all/vars.yml`
- Topología del clúster y operación: red interna, puertos, particiones Slurm, UID/GID, etc.

3. `group_vars/all.yml`
- Baseline/“perfil de software”: paquetes base, toggles (p. ej. chrony), SSH, y paquetes LLM.

4. `group_vars/hpc_master.yml`
- Ajustes específicos del master: interfaces router (`hpc_router_internal_ifaces`), SlurmDBD/MariaDB, NFS server.

5. `host_vars/*.yml`
- Overrides por nodo (por ejemplo reservas/recursos Slurm en nodos concretos).

6. `group_vars/all/vault.yml` (cifrado)
- Secretos (`vault_*`). No se versiona ningún “vault password file”.

## Mapa de variables (operacionales y baseline)

Tabla: variable | definida en | usada en (aprox) | categoría | notas

| Variable | Definida en | Usada en (aprox) | Categoría | Notas |
|---|---|---|---|---|
| `common_packages` | `group_vars/all.yml` | `roles/common/tasks/main.yml` | baseline | Lista de herramientas base (incluye “herramientas de monitoreo” integradas). |
| `enable_chrony` | `group_vars/all.yml` | `roles/common/tasks/main.yml` | baseline | Habilita/instala chrony según rol `common`. |
| `ssh_port` | `group_vars/all.yml` (override) | `roles/users_ssh/tasks/main.yml` | ssh | También existe default en `roles/users_ssh/defaults/main.yml`. |
| `ssh_permit_root_login` | `group_vars/all.yml` (override) | `roles/users_ssh/tasks/main.yml` | ssh | Controla drop-in de `sshd_config`. |
| `ssh_password_authentication` | `group_vars/all.yml` (override) | `roles/users_ssh/tasks/main.yml` | ssh | Controla drop-in de `sshd_config`. |
| `llm_conda_packages` | `group_vars/all.yml` (override) | `roles/llm_env/tasks/main.yml` | llm | Paquetes micromamba/conda a instalar. |
| `llm_pip_packages` | `group_vars/all.yml` | `roles/llm_env/tasks/main.yml` | llm | Si incluye `torch`, el rol advierte sobre override del torch conda. |
| `llm_python_packages` | `group_vars/all.yml` | (referencia documental/uso futuro) | llm | Lista base para scripts/validación. |
| `slurm_firewalld_zone` | `group_vars/all/vars.yml` | `roles/firewall/tasks/main.yml` | firewall/slurm | Zona donde se aplican rich rules. |
| `slurm_internal_cidr` | `group_vars/all/vars.yml` | `roles/firewall/tasks/main.yml`, `roles/nfs_hpc/defaults/main.yml` | firewall/network/nfs | CIDR de confianza para Slurm y clientes NFS. |
| `slurmctld_port` | `group_vars/all/vars.yml` | `roles/firewall/tasks/main.yml` | firewall/slurm | Puerto TCP del controller. |
| `slurmd_port` | `group_vars/all/vars.yml` | `roles/firewall/tasks/main.yml` | firewall/slurm | Puerto TCP del daemon compute. |
| `munge_uid` | `group_vars/all/vars.yml` | `roles/slurm_identities/tasks/main.yml` | slurm/munge | UID/GID declarados para consistencia entre nodos. |
| `munge_gid` | `group_vars/all/vars.yml` | `roles/slurm_identities/tasks/main.yml` | slurm/munge | Idem. |
| `slurm_uid` | `group_vars/all/vars.yml` | `roles/slurm_identities/tasks/main.yml` | slurm | Idem. |
| `slurm_gid` | `group_vars/all/vars.yml` | `roles/slurm_identities/tasks/main.yml` | slurm | Idem. |
| `munge_key_host` | `group_vars/all/vars.yml` | `roles/munge/tasks/main.yml` | munge | Host “fuente” donde se genera la munge key. |
| `munge_key_size_mb` | `group_vars/all/vars.yml` | `roles/munge/tasks/main.yml` | munge | Tamaño de key (dd) en MB. |
| `slurm_version` | `group_vars/all/vars.yml` | `roles/slurm_rpm_build/tasks/main.yml` | slurm | Versión Slurm para tarball/build RPM. |
| `slurm_tarball_url` | `group_vars/all/vars.yml` | `roles/slurm_rpm_build/tasks/main.yml` | slurm | URL del tarball; compone con `slurm_version`. |
| `slurm_etc_dir` | `group_vars/all/vars.yml` | `roles/slurm_install/*` (rutas de configs) | slurm | Ruta base de configs Slurm. |
| `slurm_log_dir` | `group_vars/all/vars.yml` | `roles/slurm_install/*` | slurm | Ruta de logs Slurm. |
| `slurm_cgroup_conf` | `group_vars/all/vars.yml` | `roles/slurm_install/*` | slurm | Contenido de `cgroup.conf`. |
| `slurm_control_machine` | `group_vars/all/vars.yml` | `roles/slurm_install/templates/slurm.conf.j2`, `roles/validate/tasks/slurm.yml`, `roles/nfs_hpc/defaults/main.yml` | slurm/nfs/validate | Nombre de inventario del controller. |
| `slurm_mem_reserve_mb` | `group_vars/all/vars.yml` | `roles/slurm_install/templates/slurm.conf.j2` | slurm | Reserva para SO al derivar Memory en templates. |
| `slurm_partitions` | `group_vars/all/vars.yml` | `roles/slurm_install/templates/slurm.conf.j2` | slurm | Particiones por grupos de inventario. |
| `slurm_srun_port_range` | `group_vars/all/vars.yml` | `roles/slurm_install/templates/slurm.conf.j2`, `roles/slurm_install/tasks/main.yml` | slurm/firewall | Rango de puertos para `srun`. |
| `slurm_validate_torch` | `group_vars/all/vars.yml` (override) | `roles/slurm_validate/tasks/main.yml` | validate/llm | Controla prelude/exec para validar torch dentro de Slurm. Default también existe en `roles/slurm_validate/defaults/main.yml`. |
| `hpc_internal_supernet` | `group_vars/all/vars.yml` | `roles/cluster_routing/tasks/main.yml` | routing/network | Superred usada para políticas/rutas. |
| `hpc_internal_subnets` | `group_vars/all/vars.yml` | `roles/cluster_routing/tasks/main.yml` | routing/network | Lista de subredes internas permitidas/esperadas. |
| `hpc_router_internal_ifaces` | `group_vars/hpc_master.yml` | `roles/cluster_routing/tasks/main.yml` | routing/network | Interfaces del master que enrutan entre subredes. |
| `slurmdb_mysql_password` | `group_vars/hpc_master.yml` (vault-backed) | `roles/slurm_db_prep/*`, `roles/slurm_controller/*` | slurmdb | Referencia a `vault_slurmdb_mysql_password`. No está en claro. |

## Hardcodes detectados (pendientes de parametrización)

Estas ocurrencias son evidencia de valores embebidos en defaults/archivos. En P11a se documentan; no se refactorizan para no tocar roles.

IPs hardcodeadas:
- `inventario.ini`: `master ansible_host=10.195.34.17` y workers `192.168.34.*`
- `group_vars/all/vars.yml`: `slurm_internal_cidr`, `hpc_internal_supernet`, `hpc_internal_subnets`
- `roles/network_internal/defaults/main.yml`: `master_ip`/`worker_ip` por enlace (`192.168.34.x/28`)

Interfaces hardcodeadas:
- `group_vars/hpc_master.yml`: `hpc_router_internal_ifaces: [enp3s0f*]`
- `roles/network_internal/defaults/main.yml`: `network_internal_keep_if: eno1` y mapa de `master_if`/`worker_if` (`enp3s0f*`)

Paths `/srv/nfs`, `/data`, `/scratch`:
- Búsqueda rápida no encontró ocurrencias con ese patrón; los paths reales (si existen) deben confirmarse mirando defaults/templates del rol correspondiente.

## Nota operativa

Cambios de red/ruteo/firewall son HIGH-RISK. Para replicar en otro sitio, normalmente se requiere adaptar como mínimo:
- `inventario.ini` (IPs y grupos)
- `group_vars/all/vars.yml` (CIDRs/subredes/puertos/particiones)
- `group_vars/hpc_master.yml` + `roles/network_internal/defaults/main.yml` (interfaces y esquema de enlaces)

