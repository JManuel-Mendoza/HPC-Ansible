# Automatizacion de cluster HPC con Ansible

Este repositorio automatiza la instalacion, configuracion y validacion de un cluster HPC con nodo `master` y nodos `workers`.

Entrypoint unico:
- `site.yml`

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

## Requisitos minimos (nodo de control)

- Ansible instalado (recomendado: `>= 2.14`).
- Colecciones instaladas: ver `requirements.yml` y ejecutar `ansible-galaxy collection install -r requirements.yml`.
- Acceso SSH a los nodos (idealmente con llave).
- Vault configurado (ver `docs/vault.md`).

## Desde cero: instalación limpia -> clúster listo

Esta guía asume que ya tienes un SO limpio instalado en `master` y `workers` (paso fuera de este repo).
El entrypoint único del repositorio es `site.yml`.

### Prerrequisitos (control node)

1) Colecciones Ansible (obligatorio):
```bash
ansible-galaxy collection install -r requirements.yml
```

2) Vault (obligatorio):
- Guía: `docs/vault.md`
- Ejecución interactiva:
```bash
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
```
- Ejecución reproducible sin prompt (archivo local, no se commitea):
```bash
ANSIBLE_VAULT_PASSWORD_FILE=~/.config/hpc-ansible/vault-pass.txt ansible-playbook -i inventario.ini site.yml --syntax-check
```

### Configuración mínima para replicar

Archivos que normalmente debes editar para adaptar el clúster a tu laboratorio:
- `inventario.ini` (hosts/grupos y `ansible_host`/usuarios)
- `group_vars/all/vars.yml` (variables operacionales: red interna, Slurm, firewall, topología)
- `group_vars/all.yml` (baseline: paquetes, SSH, LLM)
- `group_vars/hpc_master.yml` (settings específicos del master: router/NFS/MariaDB/SlurmDBD)
- `host_vars/*.yml` (overrides por nodo, si aplica)
- `group_vars/all/vault.yml` (secretos cifrados; ver `docs/vault.md`)

Referencias:
- `docs/06-referencia-archivos.md`
- `docs/audit/vars-map.md`

### Preflight seguro (no cambia nodos)

```bash
ansible-inventory -i inventario.ini --graph --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --list-tasks --ask-vault-pass
```

### Orden recomendado de ejecución (por etapas/tags)

La fuente de verdad es `docs/audit/ansible-entrypoints.md`. Resumen:
- Baseline: `--tags common,ssh`
- Red/ruteo: `--tags network,routing` (HIGH-RISK)
- Firewall: `--tags firewall` (HIGH-RISK)
- CUDA: `--tags cuda` (HIGH-RISK; puede requerir reboot)
- NFS: `--tags nfs` (HIGH-RISK)
- Slurm: `--tags slurm,slurm_install,slurm_config,munge,identities,slurmdb` (HIGH-RISK)
- LLM: `--tags llm`
- Validación: `--tags validate,slurm_validate`

### Ejemplos seguros (recomendado con `--limit`)

Dry-run (preflight de idempotencia) sobre un solo nodo:
```bash
ansible-playbook -i inventario.ini site.yml --check --diff --limit worker1 --ask-vault-pass --skip-tags debug
```

Baseline en un solo nodo:
```bash
ansible-playbook -i inventario.ini site.yml --tags common,ssh --limit worker1 --ask-vault-pass --skip-tags debug
```

Ejecución completa (cuando ya probaste por etapas):
```bash
ansible-playbook -i inventario.ini site.yml --ask-vault-pass --skip-tags debug
```

## Configurar inventario (inventario.ini)

- Edita `inventario.ini` para reflejar tus IPs/usuarios y grupos (`hpc_master`, `workers_*`, `slurm_*`).
- Recomendado: ejecutar con `--limit` al inicio (un worker primero).

## Configuracion minima para adaptar a tu laboratorio

Edita estos archivos (en este orden) para replicar el despliegue:

1. `inventario.ini`
- IPs/hostnames reales (`ansible_host`), usuarios (`ansible_user`) y pertenencia a grupos.

2. `group_vars/all/vars.yml`
- Topologia operacional: CIDRs/subredes internas, puertos, particiones Slurm, UID/GID, etc.

3. `group_vars/hpc_master.yml`
- Interfaces internas del master (`hpc_router_internal_ifaces`) y settings del master (NFS/MariaDB/SlurmDBD).

4. `group_vars/all.yml`
- Paquetes base, SSH y entorno LLM (micromamba) segun lo que quieras instalar por defecto.

5. `group_vars/all/vault.yml` (cifrado) y `.secrets/` (local)
- Secretos via Vault. Ver `docs/vault.md`.
- El “vault password file” es local (no se commitea).

## Vault (secretos)

Este repo usa Ansible Vault.

- Guía: `docs/vault.md`
- Validación rápida:

```bash
ansible-inventory -i inventario.ini --graph --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
```

Alternativa reproducible sin prompt (archivo local fuera del repo):

```bash
ANSIBLE_VAULT_PASSWORD_FILE=~/.config/hpc-ansible/vault-pass.txt ansible-playbook -i inventario.ini site.yml --syntax-check
```

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
- `docs/audit/ansible-entrypoints.md`: entrypoint, orden recomendado y advertencias de riesgo.
- `docs/audit/plan.md`: plan de cambios por paquetes (auditoría).
- `docs/audit/vars-map.md`: mapa de variables operacionales y hardcodes detectados (auditoría).
- `docs/runbooks/`: runbooks operativos mínimos (Slurm/GPU/NFS/Munge/Network).

## Mapa del repositorio

- `site.yml`: entrypoint único (orquesta roles por etapas).
- `inventario.ini`: inventario por defecto (hosts, grupos y conexión).
- `group_vars/`: variables por alcance (`all`, `hpc_master`, etc.) y Vault (`group_vars/all/vault.yml`).
- `host_vars/`: overrides por nodo (cuando aplica).
- `roles/`: roles Ansible (state + validación), organizados por dominio (`common`, `firewall`, `nvidia_cuda`, `slurm_*`, `validate`, etc.).
- `docs/`: documentación principal (índice, arquitectura, referencia).
- `docs/runbooks/`: operación/diagnóstico por dominio (comandos y evidencia).
- `docs/audit/`: auditoría (entrypoints, ledger, matriz de tasks, plan).
- `tools/`: herramientas auxiliares de análisis (no tocan infraestructura).

## Inicio rapido

Instalar colecciones:

```bash
ansible-galaxy collection install -r requirements.yml
```

Quickstart (sin tocar nodos, solo validaciones locales):

```bash
ansible-inventory -i inventario.ini --graph --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --list-tasks --ask-vault-pass
```

Dry-run sobre un solo nodo:

```bash
ansible-playbook -i inventario.ini site.yml --check --diff --limit worker1 --ask-vault-pass --skip-tags debug
```

Ejecucion completa (recomendado por etapas):

```bash
ansible-playbook -i inventario.ini site.yml --ask-vault-pass --skip-tags debug
```

## Ejemplos por etapas (tags) y limites

Baseline (paquetes base, EPEL, SSH):

```bash
ansible-playbook -i inventario.ini site.yml --tags common,ssh --limit worker1 --ask-vault-pass
```

Red y ruteo (alto riesgo):

```bash
ansible-playbook -i inventario.ini site.yml --tags network,routing --limit worker1 --ask-vault-pass
```

GPU/CUDA (alto riesgo, puede requerir reinicio):

```bash
ansible-playbook -i inventario.ini site.yml --tags cuda --limit worker1 --ask-vault-pass
```

Slurm (master primero, luego compute):

```bash
ansible-playbook -i inventario.ini site.yml --tags slurm,munge,identities,slurm_install,slurm_config,slurmdb --limit hpc_master --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags slurm,slurm_install,slurm_config --limit slurm_compute --ask-vault-pass
```

Validación:

```bash
ansible-playbook -i inventario.ini site.yml --tags validate,slurm_validate --limit hpc_master --ask-vault-pass --skip-tags debug
```

## Diagnóstico (salida extra)

Habilitar diagnóstico junto con una etapa (recomendado):

```bash
ansible-playbook -i inventario.ini site.yml --tags validate,debug --limit worker1 --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags firewall,debug --limit worker1 --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags cuda,debug --limit worker1 --ask-vault-pass
```

Diagnóstico específico (sub-tags):

```bash
ansible-playbook -i inventario.ini site.yml --tags firewall,debug_firewall --limit worker1 --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags validate,debug_validate --limit worker1 --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags cuda,debug_cuda --limit worker1 --ask-vault-pass
```

Omitir diagnóstico (recomendado en ejecución normal):

```bash
ansible-playbook -i inventario.ini site.yml --skip-tags debug --ask-vault-pass
```

## Flujo recomendado (instalacion limpia -> HPC listo -> Slurm -> LLM)

1. Instalación limpia del SO (fuera de este repo).
2. Baseline HPC: `--tags common,ssh` (y luego `firewall/network/routing/nfs/cuda` según aplique).
3. Slurm: DB (master) -> identidades + munge -> install/controller/compute.
4. LLM: `--tags llm`.
5. Validación: `--tags validate,slurm_validate`.

## Validación y troubleshooting

Validaciones (rol `validate`) se pueden ejecutar por dominio:
```bash
ansible-playbook -i inventario.ini site.yml --tags validate --limit worker1 --ask-vault-pass --skip-tags debug
ansible-playbook -i inventario.ini site.yml --tags validate_slurm --limit slurm_all --ask-vault-pass --skip-tags debug
ansible-playbook -i inventario.ini site.yml --tags validate_cuda --limit worker1 --ask-vault-pass --skip-tags debug
```

Smoke tests de Slurm (rol `slurm_validate`, desde el master):
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm_validate --limit hpc_master --ask-vault-pass --skip-tags debug
```

Runbooks operativos (diagnóstico y evidencia):
- Slurm: `docs/runbooks/slurm.md`
- GPU/CUDA: `docs/runbooks/gpu-cuda.md`
- NFS: `docs/runbooks/nfs.md`
- Munge: `docs/runbooks/munge.md`
- Network/Firewall: `docs/runbooks/network-firewall.md`

## Nota de alcance documental

La documentacion cubre el proyecto activo. Notas/bitácoras históricas se preservan en `docs/docs_old/` (ver `docs/docs_old/README.md`).
