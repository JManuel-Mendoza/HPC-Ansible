# Ansible Entrypoints

## Entrypoints activos

| Playbook | Proposito | Estado list-tasks |
|---|---|---|
| `site.yml` | Orquestacion completa del cluster HPC/Slurm/LLM | OK (plays: 15, tasks listadas: 404) |

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

- play #1 (all): Baseline HPC (common + ssh)	TAGS: []
- play #2 (all): Red interna + ruteo + firewall	TAGS: []
- play #3 (all): CUDA/Driver NVIDIA (solo nodos con GPU)	TAGS: []
- play #4 (hpc_master): NFS HPC (server export)	TAGS: []
- play #5 (all:!hpc_master): NFS HPC (clientes mount)	TAGS: []
- play #6 (hpc_master): MariaDB en master	TAGS: []
- play #7 (hpc_master): Preparar SlurmDB en MariaDB (master)	TAGS: []
- play #8 (slurm_all): Configuración de identidades SLURM	TAGS: []
- play #9 (slurm_all): Configuración de Munge en nodos SLURM	TAGS: []
- play #10 (slurm_all): Recopilación de hechos SLURM en nodos SLURM	TAGS: []
- play #11 (hpc_master): Configuración de SLURM en nodo master	TAGS: []
- play #12 (slurm_compute): Configuración de SLURM en nodos compute	TAGS: []
- play #13 (all): Entorno LLM (micromamba + torch)	TAGS: []
- play #14 (all): Validación general de salud del clúster	TAGS: []
- play #15 (hpc_master): Validación Slurm (sin cambios de configuracion)	TAGS: []

## P16 | Pin de colecciones + optimizacion de facts por tags

Objetivo:
- Reducir overhead en ejecuciones con `--tags` evitando `Gathering Facts` en plays sin match.
- Mantener compatibilidad con `ansible-core 2.14` fijando `ansible.posix`.

### Facts (P16): gather_facts deshabilitado + setup taggeado

- En `site.yml`, todos los plays usan `gather_facts: false`.
- Cada play define un `pre_tasks` con `ansible.builtin.setup` taggeado con la unión de `TASK TAGS` reales de ese play.
- Con esto, al ejecutar `--tags`, solo recolectan facts los plays que efectivamente tienen tareas con match.
- Se evita el overhead de `Gathering Facts` en plays sin tareas seleccionadas por tags.
- No se usan `tags` a nivel play para preservar semántica de selección.
- Mantenimiento: si agregas roles/tareas con tags nuevos en un play, actualiza también el `tags:` del `pre_tasks` `setup` de ese play (unión de tags vigente).

Cambios aplicados:
- `requirements.yml`: `ansible.posix` fijado en `1.5.4`.
- `site.yml`: en los 15 plays, `gather_facts: false` + `pre_tasks` con `ansible.builtin.setup` taggeado con el union real de `TASK TAGS` de cada play.
- Sin `tags` a nivel play.

Evidencia:
- Antes:
  - `ansible-playbook -i inventario.ini site.yml --list-tags --vault-password-file .secrets/vault-pass.txt > /tmp/list-tags.P16.before.txt`
- Después:
  - `ansible-playbook -i inventario.ini site.yml --list-tags --vault-password-file .secrets/vault-pass.txt > /tmp/list-tags.P16.after.txt`
  - `ansible-playbook -i inventario.ini site.yml --list-tasks --vault-password-file .secrets/vault-pass.txt > /tmp/list-tasks.P16.after.txt`
- Compatibilidad colección:
  - `ansible-galaxy collection list | rg 'ansible\.posix'`
  - Resultado: `ansible.posix 1.5.4`
- Prueba de no-overhead en run por tags (evidencia operativa):
  - `grep -c "TASK \[Gathering Facts\]" /tmp/salida_nfs.log` => `0`
  - `grep -c "TASK \[Gathering Facts\]" /tmp/salida_validate_slurm.log` => `0`
  - `grep -n "Preflight | Recolectar facts" /tmp/salida_nfs.log /tmp/salida_validate_slurm.log`
    - `/tmp/salida_nfs.log:10:TASK [Preflight | Recolectar facts (play 4)]`
    - `/tmp/salida_nfs.log:95:TASK [Preflight | Recolectar facts (play 5)]`
    - `/tmp/salida_validate_slurm.log:30:TASK [Preflight | Recolectar facts (play 14)]`
