# Automatizacion de cluster HPC con Ansible

Este repositorio automatiza el aprovisionamiento y la operacion de un cluster HPC con Ansible.
La orquestacion principal vive en `site.yml` e integra red interna, firewall, NFS, CUDA/NVIDIA, Slurm, entorno LLM y validaciones.
El diseno separa fases de configuracion y fases de verificacion para reducir riesgo operativo.
La guia resume como configurar inventario y variables, ejecutar por etapas/tags y validar con smoke/canary.

## Caracteristicas principales

- Orquestacion declarativa por etapas en un entrypoint unico: `site.yml`.
- Ejecucion parcial por tags para despliegues controlados (`common`, `network`, `slurm`, `validate`, entre otros).
- Soporte de nodos de control y nodos de computo con grupos de inventario dedicados.
- Integracion de servicios base HPC: `firewalld`, rutas internas, NFS compartido, Slurm y Munge.
- Pipeline de validacion con checks generales (`validate`) y smoke jobs Slurm CPU/GPU (`slurm_validate_smoke`).
- Manejo de secretos con Ansible Vault (`group_vars/all/vault.yml`).

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
- Secretos Vault disponibles (`group_vars/all/vault.yml`) y metodo de desbloqueo:
  - `--ask-vault-pass`, o
  - `--vault-password-file` con archivo local no versionado.

## Estructura del repositorio

```text
.
|-- site.yml
|-- inventario.ini
|-- ansible.cfg
|-- requirements.yml
|-- group_vars/
|   |-- all/
|   |   |-- vars.yml
|   |   `-- vault.yml
|   `-- hpc_master.yml
|-- host_vars/
|   |-- master.yml
|   |-- worker1.yml
|   `-- worker2.yml
|-- roles/
|   |-- common/
|   |-- network_internal/
|   |-- cluster_routing/
|   |-- firewall/
|   |-- nfs_hpc/
|   |-- nvidia_cuda/
|   |-- slurm_*/
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
- Preparar Vault segun `docs/vault.md`.

### 4) Preflight sin cambios

```bash
ansible-inventory -i inventario.ini --graph --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --list-tags --ask-vault-pass
```

### 5) Ejecucion por fases/tags con limite controlado

```bash
ansible-playbook -i inventario.ini site.yml --check --diff --limit <host_habilitado> --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags common,ssh --limit <host_habilitado> --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags network,routing,firewall --limit <host_habilitado> --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags slurm,slurm_install,slurm_config --limit hpc_master --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags slurm,slurm_install,slurm_config --limit slurm_compute --ask-vault-pass
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

## Validacion y evidencia (smoke/canary)

### Verificacion rapida recomendada

```bash
ansible-playbook -i inventario.ini site.yml --ask-vault-pass --tags validate_slurm --limit "hpc_master,slurm_compute"
ansible-playbook -i inventario.ini site.yml --ask-vault-pass --tags slurm_validate_smoke
```

### Canary previo a despliegue amplio

```bash
ansible-playbook -i inventario.ini site.yml --ask-vault-pass --limit "hpc_master,<host_habilitado>" -f 10
```

Ejemplo con host habilitado actual:

```bash
ansible-playbook -i inventario.ini site.yml --ask-vault-pass --limit "hpc_master,worker2" -f 10
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
- Munge: `docs/runbooks/munge.md`
- GPU/CUDA: `docs/runbooks/gpu-cuda.md`
- NFS: `docs/runbooks/nfs.md`
- Red/Firewall: `docs/runbooks/network-firewall.md`
- Indice general de documentacion: `docs/00-indice.md`

## Troubleshooting minimo

1. Sintoma: `--syntax-check` falla.
   - Accion: validar inventario y Vault (`ansible-inventory --graph`, `docs/vault.md`).

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

## Licencia y creditos

- Licencia: no se encontro archivo `LICENSE` en la raiz al momento de esta revision. Consultar definicion de licencia con la persona propietaria del repositorio.
- Creditos: autoria y cambios disponibles en el historial de Git del repositorio.
