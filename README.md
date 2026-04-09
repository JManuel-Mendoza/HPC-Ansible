# Automatizacion de cluster HPC con Ansible

Este repositorio automatiza el aprovisionamiento y la operacion de un cluster HPC con Ansible.
La orquestacion principal vive en `site.yml` e integra red interna, firewall, NFS, CUDA/NVIDIA, Slurm, entorno LLM y validaciones.
El diseno separa fases de configuracion y fases de verificacion para reducir riesgo operativo.
La guia resume como configurar inventario y variables, ejecutar por etapas/tags y validar con smoke/canary.

## Caracteristicas principales

- Orquestacion declarativa por etapas en un entrypoint unico: `site.yml`.
- Playbook de limpieza controlada para reprovision (`cleanup_slurm_gpu.yml`) en escenarios de reconstruccion total.
- Ejecucion parcial por tags para despliegues controlados (`common`, `network`, `slurm`, `validate`, entre otros).
- Soporte de nodos de control y nodos de computo con grupos de inventario dedicados.
- Integracion de servicios base HPC: `firewalld`, rutas internas, NFS compartido, Slurm y Munge.
- Pipeline de validacion con checks generales (`validate`) y smoke jobs Slurm CPU/GPU (`slurm_validate_smoke`).
- Credenciales operativas definidas directamente en `inventario.ini` y `group_vars/hpc_master.yml`.

## Arquitectura resumida

### Nodos y grupos

- `hpc_master`: nodo de control principal (`master`).
- `workers`: conjunto de nodos de trabajo habilitados en inventario.
- `slurm_all`: nodos con componentes Slurm.
- `slurm_compute`: nodos objetivo para `slurmd` y configuracion de compute.
- `slurm_gpu`: nodos con capacidad GPU para validaciones y jobs acelerados.

Referencia: `inventario.ini`.

### Componentes operativos

- Baseline: hardening basico y acceso SSH (`common`, `users_ssh`).
- Red interna y ruteo: `network_internal`, `cluster_routing`.
- Firewall: reglas de `firewalld` para trafico de cluster.
- Storage compartido: `nfs_hpc` (export en master y mounts en clientes).
- GPU/CUDA: `nvidia_cuda`.
- Slurm: identidades, munge, facts, instalacion/controller/compute, validacion.
- Entorno LLM: `llm_env`.
- Verificacion: `validate` y `slurm_validate`.

## Prerrequisitos

- Nodo de control Linux con Ansible disponible.
- Compatibilidad esperada con `ansible-core 2.14` (ver comentario de version en `requirements.yml`).
- Coleccion requerida:
  - `ansible.posix` version `1.5.4` (definida en `requirements.yml`).
- Acceso SSH a nodos del inventario y permisos de elevacion cuando aplique.
- Resolucion de nombres/IP coherente para `master` y `workers` (DNS interno o `/etc/hosts` gestionado por `network_internal`).
- Interfaces internas y subredes declaradas en `network_internal_links` y `hpc_internal_subnets` antes de ejecutar cambios de red.
- Credenciales operativas configuradas directamente en:
  - `inventario.ini` para `ansible_become_password`.
  - `group_vars/hpc_master.yml` para `slurmdb_mysql_password`.

## Estructura del repositorio

```text
.
|-- site.yml
|-- cleanup_slurm_gpu.yml
|-- inventario.ini
|-- ansible.cfg
|-- requirements.yml
|-- group_vars/
|   |-- all/
|   |   `-- vars.yml
|   `-- hpc_master.yml
|-- host_vars/
|   |-- master.yml
|   |-- worker1.yml
|   `-- worker2.yml
|-- roles/
|   |-- common/
|   |-- users_ssh/
|   |-- network_internal/
|   |-- cluster_routing/
|   |-- firewall/
|   |-- nfs_hpc/
|   |-- nvidia_cuda/
|   |-- mariadb_server/
|   |-- slurm_identities/
|   |-- munge/
|   |-- slurm_facts/
|   |-- slurm_db_prep/
|   |-- slurm_rpm_build/
|   |-- slurm_install/
|   |-- slurm_controller/
|   |-- slurm_compute/
|   |-- slurm_validate/
|   |-- llm_env/
|   `-- validate/
`-- docs/
    |-- 00-indice.md
    |-- 07-verificacion-rapida.md
    |-- 07-runbooks-operativos.md
    `-- runbooks/
```

## Quickstart reproducible

### 1) Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd hpc-ansible
```

### 2) Instalar colecciones

```bash
ansible-galaxy collection install -r requirements.yml
```

### 3) Preparar inventario y variables

- Ajustar hosts y grupos en `inventario.ini`.
- Ajustar parametros globales en `group_vars/all/vars.yml`.
- Ajustar parametros del master en `group_vars/hpc_master.yml`.
- Ajustar overrides por host en `host_vars/*.yml` cuando aplique.
- Revisar las credenciales directas en `inventario.ini` y `group_vars/hpc_master.yml`.

### 4) Preflight sin cambios

```bash
ansible-inventory -i inventario.ini --graph
ansible-playbook -i inventario.ini site.yml --syntax-check
ansible-playbook -i inventario.ini site.yml --list-tags
```

### 5) Ejecucion por fases/tags con limite controlado

```bash
ansible-playbook -i inventario.ini site.yml --check --diff --limit <host_habilitado>
ansible-playbook -i inventario.ini site.yml --tags common,ssh --limit <host_habilitado>
ansible-playbook -i inventario.ini site.yml --tags network,routing,firewall --limit <host_habilitado>
ansible-playbook -i inventario.ini site.yml --tags slurm,slurm_install,slurm_config --limit hpc_master
ansible-playbook -i inventario.ini site.yml --tags slurm,slurm_install,slurm_config --limit slurm_compute
```

Nota: `<host_habilitado>` se sustituye por un host activo en `inventario.ini` (ejemplo actual: `worker2`).

## Ejecucion por etapas (site.yml)

Las etapas canonicamente definidas en `site.yml` son:

1. `Etapa 1 | Baseline HPC (common + ssh)` en `all`.
2. `Etapa 2 | Red interna + ruteo + firewall` en `all`.
3. `Etapa 3 | CUDA/Driver NVIDIA (solo nodos con GPU)` en `all`.
4. `Etapa 4 | NFS HPC (server export)` en `hpc_master`.
5. `Etapa 5 | NFS HPC (clientes mount)` en `all:!hpc_master`.
6. `Etapa 6 | MariaDB en master` en `hpc_master`.
7. `Etapa 7 | Preparar SlurmDB en MariaDB (master)` en `hpc_master`.
8. `Etapa 8 | Configuracion de identidades SLURM` en `slurm_all`.
9. `Etapa 9 | Configuracion de Munge en nodos SLURM` en `slurm_all`.
10. `Etapa 10 | Recopilacion de hechos SLURM en nodos SLURM` en `slurm_all`.
11. `Etapa 11 | Configuracion de SLURM en nodo master` en `hpc_master`.
12. `Etapa 12 | Configuracion de SLURM en nodos compute` en `slurm_compute`.
13. `Etapa 13 | Entorno LLM (micromamba + torch)` en `all`.
14. `Etapa 14 | Validacion general de salud del cluster` en `all`.
15. `Etapa 15 | Validacion Slurm (sin cambios de configuracion)` en `hpc_master`.

## Playbook de limpieza total (alto riesgo)

`cleanup_slurm_gpu.yml` elimina servicios/paquetes/configuracion de Slurm, Munge, NVIDIA/CUDA y reglas de firewall asociadas, para reprovisionar desde cero.

Reglas operativas minimas:
- Ejecutar en ventana de mantenimiento.
- Empezar con `--limit` a un solo nodo.
- Verificar tags y alcance antes de ejecutar.

Comandos recomendados:

```bash
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --list-tags
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --limit <host_habilitado> --tags cleanup,cleanup_verify
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --limit <host_habilitado>
```

Referencia operativa: `docs/runbooks/cleanup-slurm-gpu.md`.

## Validacion y evidencia (smoke/canary)

### Verificacion rapida recomendada

```bash
ansible-playbook -i inventario.ini site.yml --tags validate_slurm --limit "hpc_master,slurm_compute"
ansible-playbook -i inventario.ini site.yml --tags slurm_validate_smoke
```

### Canary previo a despliegue amplio

```bash
ansible-playbook -i inventario.ini site.yml --limit "hpc_master,<host_habilitado>" -f 10
```

Ejemplo con host habilitado actual:

```bash
ansible-playbook -i inventario.ini site.yml --limit "hpc_master,worker2" -f 10
```

### Criterio de resultado "OK"

- `ansible-playbook` finaliza sin fallos en tareas criticas.
- `slurm_validate_smoke` confirma jobs CPU y GPU con estado `COMPLETED|0:0`.
- Los checks de particiones y estado de nodos Slurm no reportan `DOWN`, `DRAIN` o `FAIL`.

### Donde revisar evidencia y salidas

- Salida de Ansible en consola (incluye `debug` de validaciones).
- Runbooks de diagnostico en `docs/runbooks/*.md`.
- Para smoke Slurm, el rol inspecciona `StdOut`/`StdErr` de jobs via `scontrol show job` y los muestra en la ejecucion.
- Parametros de smoke (workdir, timeout, polling): `roles/slurm_validate/defaults/main.yml`.

## Runbooks operativos

- Orquestacion operativa general: `docs/07-runbooks-operativos.md`
- Verificacion rapida: `docs/07-verificacion-rapida.md`
- Slurm: `docs/runbooks/slurm.md`
- Limpieza total Slurm/GPU: `docs/runbooks/cleanup-slurm-gpu.md`
- Munge: `docs/runbooks/munge.md`
- GPU/CUDA: `docs/runbooks/gpu-cuda.md`
- NFS: `docs/runbooks/nfs.md`
- Red/Firewall: `docs/runbooks/network-firewall.md`
- Indice general de documentacion: `docs/00-indice.md`

## Troubleshooting minimo

1. Sintoma: `--syntax-check` falla.
   - Accion: validar inventario y revisar las credenciales directas en `inventario.ini` y `group_vars/hpc_master.yml`.

2. Sintoma: conectividad inter-nodos inestable tras cambios de red.
   - Accion: ejecutar por `--limit <host_habilitado>` y revisar `docs/runbooks/network-firewall.md`.

3. Sintoma: `slurmctld` o `slurmd` no inician.
   - Accion: usar `docs/runbooks/slurm.md` y relanzar `--tags slurm_validate`.

4. Sintoma: `nvidia-smi` no disponible o errores de driver.
   - Accion: revisar `docs/runbooks/gpu-cuda.md` y rerun `--tags cuda` en canary.

5. Sintoma: jobs GPU no asignan recursos.
   - Accion: verificar particion GPU y `--gres=gpu:1`; luego correr `--tags slurm_validate_smoke`.

6. Sintoma: mounts NFS no aparecen en nodos de computo.
   - Accion: revisar export/mount/firewall con `docs/runbooks/nfs.md`.

7. Sintoma: fallos de autenticacion entre componentes Slurm.
   - Accion: validar clave/permisos/servicio Munge segun `docs/runbooks/munge.md`.

8. Sintoma: drift entre corridas.
   - Accion: ejecutar `--check --diff` por fases y comparar salidas de validacion en `docs/08-validacion-y-evidencia.md`.

9. Sintoma: se requiere reconstruccion completa de Slurm + GPU/CUDA.
   - Accion: seguir `docs/runbooks/cleanup-slurm-gpu.md` y reprovisionar por etapas con `site.yml`.

## Licencia y creditos

- Licencia: no se encontro archivo `LICENSE` en la raiz al momento de esta revision. Consultar definicion de licencia con la persona propietaria del repositorio.
- Creditos: autoria y cambios disponibles en el historial de Git del repositorio.
