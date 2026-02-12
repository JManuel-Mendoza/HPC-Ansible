# Automatizacion de cluster HPC con Ansible

Este repositorio automatiza la instalacion, configuracion y validacion de un cluster HPC con nodo `master` y nodos `workers`.

Objetivo operativo:
- Infraestructura declarativa (sin hotfixes manuales).
- Cambios repetibles e idempotentes.
- Operacion segura de servicios criticos (red, firewall, Slurm, GPU, NFS).

Alcance tecnico:
- Baseline de sistema, SSH y firewall.
- Red interna entre subredes y ruteo entre nodos.
- NFS compartido para trabajo HPC.
- Driver NVIDIA/CUDA y entorno LLM con micromamba.
- Slurm completo (identidades, munge, build, install, controller, compute).
- Validaciones generales y smoke tests CPU/GPU.

## Documentacion completa

Toda la documentacion detallada esta en `docs/`.

- `docs/00-indice.md`: mapa completo de la documentacion.
- `docs/01-guia-rapida-no-especialistas.md`: introduccion para personas fuera de HPC.
- `docs/02-arquitectura-ejecucion.md`: arquitectura y flujo de `site.yml`.
- `docs/03-inventario-y-variables.md`: inventario, `group_vars` y `host_vars`.
- `docs/04-playbooks-roles-y-tags.md`: playbooks, roles y tags.
- `docs/05-referencia-roles.md`: comportamiento de cada rol.
- `docs/06-referencia-archivos.md`: referencia de todos los archivos activos.
- `docs/07-runbooks-operativos.md`: runbooks de despliegue y operacion segura.
- `docs/08-validacion-y-evidencia.md`: validacion, evidencia y criterios de salud.
- `docs/09-glosario.md`: terminos HPC/Slurm explicados en lenguaje simple.

## Inicio rapido

Instalar colecciones:

```bash
ansible-galaxy collection install -r requirements.yml
```

Verificar inventario y sintaxis:

```bash
ansible-inventory -i inventario.ini --graph
ansible-playbook -i inventario.ini site.yml --syntax-check
```

Dry-run sobre un solo nodo:

```bash
ansible-playbook -i inventario.ini site.yml --check --diff --limit worker1
```

Ejecucion completa:

```bash
ansible-playbook -i inventario.ini site.yml
```

## Seguridad

Este repositorio contiene valores sensibles en texto plano (por ejemplo, password de `become` en `inventario.ini` y password de SlurmDB en `group_vars/hpc_master.yml`).

Recomendacion:
- mover secretos a Ansible Vault antes de usar el repositorio fuera de un entorno controlado.

## Nota de alcance documental

La documentacion cubre todo el proyecto activo y excluye explicitamente `archivo_no_en_uso/`.
