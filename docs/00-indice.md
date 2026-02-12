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
6. `docs/08-validacion-y-evidencia.md`

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

- `docs/08-validacion-y-evidencia.md`
  - Como validar correctamente, que evidencia guardar y criterios de aceptacion.

- `docs/09-glosario.md`
  - Definiciones de terminos tecnicos usados en este repositorio.

## Cobertura

Cobertura incluida:
- Archivos de raiz usados por la operacion.
- `group_vars/`, `host_vars/`.
- Todos los roles en `roles/`.

Cobertura excluida:
- `archivo_no_en_uso/` (por requerimiento explicito).
