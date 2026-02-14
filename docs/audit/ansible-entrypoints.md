# Ansible Entrypoints

## Entrypoints activos

| Playbook | Proposito | Estado list-tasks |
|---|---|---|
| `site.yml` | Orquestacion completa del cluster HPC/Slurm/LLM | OK (plays: 10, tasks listadas: 354) |

Documentos relacionados:
- Plan de cambios por paquetes: `docs/audit/plan.md`
- Gestión de secretos: `docs/vault.md`

## Entry points legacy/no activos

- Documentación histórica: `docs/docs_old/README.md` (bitácoras y notas de iteraciones previas; no parte del flujo activo).

## Orden recomendado de ejecucion (operativo)

1. `clean OS` (si aplica fuera de este repo)
2. `bootstrap/base` -> tags `common,ssh`
3. `network` -> tag `network`
4. `routing` -> tag `routing`
5. `firewall` -> tag `firewall`
6. `cuda` -> tag `cuda`
7. `nfs` -> tag `nfs`
8. `slurm` -> tags `slurm,slurm_install,slurm_config,munge,identities,slurmdb`
9. `llm` -> tag `llm`
10. `validate` -> tags `validate,slurm_validate`

## Nota: reinicios de Slurm por handlers/notify

Desde el paquete P8a, los reinicios de `slurmctld`, `slurmd` y `slurmdbd` se ejecutan via **handlers** y se disparan solo cuando cambia configuración (tareas `template`/`copy`/`lineinfile` que notifican).
En los roles `slurm_controller` y `slurm_compute` se usa `meta: flush_handlers` antes de reconfigurar/validar para aplicar reinicios pendientes y evitar estados intermedios.

## Advertencias (HIGH-RISK)

Zonas de alto riesgo: ejecutar siempre con `--limit` (un nodo primero) y ventana de mantenimiento si aplica.

- Red interna y ruteo: `roles/network_internal/*`, `roles/cluster_routing/*`
- SSH y acceso: `roles/users_ssh/*`
- Firewall: `roles/firewall/*`
- Kernel/driver GPU: `roles/nvidia_cuda/*` (incluye reinicios/cambios de kernel)
- NFS: `roles/nfs_hpc/*`
- SlurmDB/MariaDB: `roles/mariadb_server/*`, `roles/slurm_db_prep/*`, `group_vars/hpc_master.yml`
- Slurm control/compute: `roles/slurm_install/*`, `roles/slurm_controller/*`, `roles/slurm_compute/*`
- Munge: `roles/munge/*`

## Nota sobre warnings del entorno de auditoria

En algunos entornos (sandbox) pueden aparecer warnings de carga de plugins (`Errno 13 Permission denied`).
Estos warnings no invalidan `--syntax-check` ni el parseo de `--list-tasks` para fines de auditoria.

## Roles cargados por `site.yml`

`common`, `users_ssh`, `firewall`, `network_internal`, `cluster_routing`, `nfs_hpc`, `nvidia_cuda`, `llm_env`, `mariadb_server`, `slurm_db_prep`, `validate`, `slurm_identities`, `munge`, `slurm_facts`, `slurm_rpm_build`, `slurm_install`, `slurm_controller`, `slurm_compute`, `slurm_validate`

## Plays detectadas en `site.yml --list-tasks`

- play #1 (all): Baseline para todos los nodos (SO + SSH + Firewall + GPU/CUDA + Entorno LLM)	TAGS: []
- play #2 (hpc_master): MariaDB en master	TAGS: []
- play #3 (hpc_master): Preparar SlurmDB en MariaDB (master)	TAGS: []
- play #4 (all): Validación de salud del clúster	TAGS: []
- play #5 (all): Configuración de identidades SLURM	TAGS: []
- play #6 (all): Configuración de munge en nodos SLURM	TAGS: []
- play #7 (all): Recopilación de hechos SLURM en todos los nodos	TAGS: []
- play #8 (hpc_master): Configuración de SLURM en nodo master	TAGS: []
- play #9 (slurm_compute): Configuración de SLURM en nodos workers	TAGS: []
- play #10 (hpc_master): Validacion Slurm (sin cambios de configuracion)	TAGS: []
