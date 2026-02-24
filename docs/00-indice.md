# Indice de documentacion

Este indice organiza la documentacion para tres perfiles:
- Personas sin experiencia previa en HPC.
- Operadores/DevOps del cluster.
- Ingenieria que mantiene playbooks y roles Ansible.

## Ruta recomendada de lectura

1. `docs/01-guia-rapida-no-especialistas.md`
2. `docs/02-arquitectura-ejecucion.md`
3. `docs/03-inventario-y-variables.md`
4. `docs/05-referencia-roles.md`
5. `docs/07-runbooks-operativos.md`
6. `docs/07-verificacion-rapida.md`
7. `docs/08-validacion-y-evidencia.md`

## Documentos

- `docs/01-guia-rapida-no-especialistas.md`
  - Explica conceptos base (HPC, Slurm, GPU, NFS) y como usar este repo sin conocimiento previo.

- `docs/02-arquitectura-ejecucion.md`
  - Describe la arquitectura funcional del proyecto y el orden de ejecucion de `site.yml`.

- `docs/03-inventario-y-variables.md`
  - Documenta grupos, hosts, `group_vars` y `host_vars`, con foco operativo.

- `docs/04-playbooks-roles-y-tags.md`
  - Mapa de playbooks y tags para ejecuciones parciales seguras.

- `docs/05-referencia-roles.md`
  - Referencia detallada de todos los roles activos en `roles/`.

- `docs/06-referencia-archivos.md`
  - Referencia de archivo por archivo (codigo activo).

- `docs/07-runbooks-operativos.md`
  - Procedimientos de despliegue, cambio y recuperacion.

- `docs/07-verificacion-rapida.md`
  - Checklist smoke mínimo para validar entrypoint, tags y jobs Slurm CPU/GPU.

- `docs/08-validacion-y-evidencia.md`
  - Como validar correctamente, que evidencia guardar y criterios de aceptacion.

- `docs/09-glosario.md`
  - Definiciones de terminos tecnicos usados en este repositorio.

## Runbooks operativos

Runbooks mínimos, orientados a comandos y evidencia:

- `docs/runbooks/slurm.md`
  - Operación/diagnóstico de `slurmctld`, `slurmd`, `slurmdbd` y accounting.
- `docs/runbooks/cleanup-slurm-gpu.md`
  - Limpieza total (alto riesgo) de Slurm + Munge + NVIDIA/CUDA para reprovisionar desde cero.
- `docs/runbooks/munge.md`
  - Permisos de key, pruebas `munge -n | unmunge` y fallas comunes.
- `docs/runbooks/gpu-cuda.md`
  - Diagnóstico NVIDIA/CUDA (`nvidia-smi`, módulos, dmesg) + PyTorch (micromamba).
- `docs/runbooks/nfs.md`
  - Server exports + client mounts + troubleshooting (firewall/permisos).
- `docs/runbooks/network-firewall.md`
  - Interfaces/rutas + `firewalld` + verificación de reglas Slurm.

## Auditoria y operacion (entrypoint)

- `docs/audit/ansible-entrypoints.md`
  - Entrypoint unico (`site.yml`), orden recomendado por tags y advertencias HIGH-RISK.

- `docs/audit/plan.md`
  - Plan de cambios por paquetes (auditoria) y backlog priorizado.

- `docs/vault.md`
  - Como crear/editar Vault y ejecutar playbooks con `--ask-vault-pass` o `--vault-password-file`.

## Cobertura

Cobertura incluida:
- Archivos de raiz usados por la operacion.
- `group_vars/`, `host_vars/`.
- Todos los roles en `roles/`.

## Docs antiguas (histórico)

- `docs/docs_old/README.md`
  - Documentación histórica rescatada de iteraciones previas (no vigente).
