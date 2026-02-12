# Ansible Entrypoints

## Entrypoints activos

| Playbook | Proposito | Estado list-tasks |
|---|---|---|
| `site.yml` | Orquestacion completa del cluster HPC/Slurm/LLM | OK (plays: 10, tasks listadas: 354) |

## Entry points legacy/no activos

- `archivo_no_en_uso/playbooks/*.yml` y `archivo_no_en_uso/playbooks sueltos/**/*.yml`: historicos, no parte del flujo activo actual.

## Orden recomendado de ejecucion (operativo)

1. `clean OS` (si aplica fuera de este repo)
2. `baseline` -> tags `common,ssh`
3. `red` -> tags `network,routing`
4. `firewall` -> tag `firewall`
5. `gpu` -> tag `cuda`
6. `nfs` -> tag `nfs`
7. `slurm` -> tags `slurm,munge,identities,slurm_install,slurm_config`
8. `llm` -> tag `llm`
9. `validate` -> tags `validate,slurm_validate`

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
