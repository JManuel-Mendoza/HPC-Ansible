# Informe de Auditoría (Fase 1)

Fecha: 2026-02-24  
Alcance: repositorio Ansible en `/Users/juanma/Projects/HPC Repo`  
Exclusión: no se toca `Manual_ZINE_2026` en esta fase.

## 1) Mapa del repositorio

Directorios y archivos clave detectados:
- Entry points:
  - `site.yml` (orquestación principal en 15 etapas)
  - `cleanup_slurm_gpu.yml` (limpieza total de Slurm/GPU para reprovision)
- Inventario y variables:
  - `inventario.ini`
  - `group_vars/all/vars.yml`
  - `group_vars/hpc_master.yml`
  - `host_vars/*.yml`
- Roles:
  - baseline/ssh/red/firewall: `common`, `users_ssh`, `network_internal`, `cluster_routing`, `firewall`
  - storage: `nfs_hpc`
  - GPU/LLM: `nvidia_cuda`, `llm_env`
  - Slurm: `slurm_identities`, `munge`, `slurm_facts`, `slurm_rpm_build`, `slurm_install`, `slurm_controller`, `slurm_compute`, `slurm_db_prep`, `slurm_validate`
  - validación general: `validate`
- Documentación:
  - `README.md`
  - `docs/` (índice, arquitectura, inventario/vars, roles, runbooks, validación)

## 2) Hallazgos por severidad

## Crítico

- No se registraron hallazgos críticos en este corte (omitiendo revisión de secretos por solicitud explícita).

## Importante

1. Normalización de `slurmdb_mysql_user` en flujo SlurmDB
- Diagnóstico:
  - `slurmdb_mysql_user` podía declararse como string (`"slurm"`), pero en `slurm_db_prep` se usaba `| list`, lo que fragmenta en caracteres.
  - `slurmdbd_storage_user` usaba `| first` sobre variable potencialmente string.
- Evidencia:
  - `group_vars/hpc_master.yml`
  - `roles/slurm_db_prep/tasks/main.yml`
- Riesgo:
  - creación/grants incorrectos en MariaDB y configuración inconsistente de `slurmdbd`.

2. Playbook destructivo sin runbook dedicado
- Diagnóstico:
  - `cleanup_slurm_gpu.yml` tenía comportamiento de alto impacto, pero faltaba documentación específica de alcance, seguridad y ejecución.
- Evidencia:
  - existencia de playbook en raíz sin runbook específico.
- Riesgo:
  - uso accidental en alcance amplio o sin validaciones previas.

## Nice-to-have

1. Mayor visibilidad de `cleanup_slurm_gpu.yml` en documentos de entrada
- Diagnóstico:
  - README/mapa de playbooks y runbooks no lo destacaban como flujo separado de alto riesgo.

2. Claridad de tipo esperado para `slurmdb_mysql_user`
- Diagnóstico:
  - la documentación no explicitaba que puede ser string o lista.

## 3) Cambios propuestos y aplicados

## Cambios de código aplicados

1. Corrección de `slurmdbd_storage_user`:
- Archivo: `group_vars/hpc_master.yml`
- Acción:
  - normalización para soportar `slurmdb_mysql_user` como string o lista y obtener el primer usuario efectivo.

2. Corrección de loops/verify en `slurm_db_prep`:
- Archivo: `roles/slurm_db_prep/tasks/main.yml`
- Acción:
  - agregado de normalización `_slurmdb_mysql_users`.
  - loops de creación/grants ahora usan lista normalizada.
  - verificación final usa primer usuario normalizado.

## Cambios de documentación aplicados

1. Nuevo runbook:
- `docs/runbooks/cleanup-slurm-gpu.md`
- Contenido:
  - alcance real de la limpieza,
  - reglas de seguridad operativa,
  - ejecución por etapas,
  - tags útiles,
  - reversión esperada (reprovision),
  - evidencia mínima.

2. Ajustes en documentación existente:
- `README.md`
  - visibilidad de `cleanup_slurm_gpu.yml`,
  - prerrequisitos de red/resolución,
  - sección de limpieza de alto riesgo,
  - enlace al nuevo runbook.
- `docs/00-indice.md`
  - inclusión del runbook de limpieza.
- `docs/04-playbooks-roles-y-tags.md`
  - inclusión del playbook `cleanup_slurm_gpu.yml` y tags `cleanup*`.
- `docs/07-runbooks-operativos.md`
  - agregado de Runbook 6 para limpieza total.
- `docs/runbooks/slurm.md`
  - nota de normalización para `slurmdb_mysql_user`.
- `docs/03-inventario-y-variables.md`
  - aclaración de tipo soportado para `slurmdb_mysql_user`.
- `docs/05-referencia-roles.md`
  - nota funcional en `slurm_db_prep`.

## 4) Evidencia de revisión (comandos ejecutados)

- Mapa del repo:
  - `pwd && ls -la`
  - `find . -maxdepth 2 -type d | sort`
- Entry points y configuración:
  - `sed -n '1,260p' site.yml`
  - `sed -n '1,260p' cleanup_slurm_gpu.yml`
  - `sed -n '1,260p' inventario.ini`
  - `sed -n '1,220p' group_vars/hpc_master.yml`
- Revisión de roles/documentación:
  - `sed -n` sobre roles `slurm_*`, `nvidia_cuda`, `nfs_hpc`, `firewall`, `validate`, `llm_env`
  - `sed -n` sobre `README.md`, `docs/*`, `docs/runbooks/*`

## 5) Riesgo residual

- `cleanup_slurm_gpu.yml` sigue siendo de alto riesgo por naturaleza (desinstalación y borrado de configuración), pero ahora queda documentado con procedimiento seguro.
- No se introdujeron refactors amplios; solo ajustes mínimos de corrección y documentación.
