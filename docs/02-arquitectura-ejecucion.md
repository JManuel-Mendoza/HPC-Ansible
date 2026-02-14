# Arquitectura y ejecucion

## Vision general

`site.yml` orquesta el cluster en capas:
1. Baseline de sistema (paquetes + SSH).
2. Red/ruteo/firewall.
3. GPU/CUDA (solo nodos con GPU).
4. NFS (server export -> clients mount).
5. Base de datos de accounting (MariaDB + SlurmDB).
6. Capa Slurm (identidades, auth, facts, instalacion, servicios).
7. Entorno LLM (micromamba + torch).
8. Validacion general + validacion Slurm (incluye smoke tests).

## Diagrama de flujo (site.yml)

```mermaid
flowchart TD
  A[Inicio site.yml] --> B[Baseline: common + users_ssh (all)]
  B --> C[Red/ruteo/firewall (all)]
  C --> D[CUDA/Driver NVIDIA (all; solo GPU)]
  D --> E[NFS server export (hpc_master)]
  E --> F[NFS clients mount (all:!hpc_master)]
  F --> G[MariaDB (hpc_master)]
  G --> H[SlurmDB prep (hpc_master)]
  H --> I[slurm_identities (slurm_all)]
  I --> J[munge (slurm_all)]
  J --> K[slurm_facts (slurm_all)]
  K --> L[slurm_rpm_build + slurm_install + slurm_controller (hpc_master)]
  L --> M[slurm_install + slurm_compute (slurm_compute)]
  M --> N[llm_env (all)]
  N --> O[validate (all)]
  O --> P[slurm_validate (hpc_master)]
  P --> Q[Fin]
```

## Responsabilidades por capa

- Baseline (`common`, `users_ssh`): deja el SO listo para operación básica.
- Red (`network_internal`, `cluster_routing`, `firewall`): conectividad interna, ruteo entre subredes y puertos de Slurm.
- GPU/CUDA (`nvidia_cuda`): driver NVIDIA y prerequisitos (solo nodos con GPU; el rol omite hosts sin GPU).
- NFS (`nfs_hpc`): export en master y montaje en clientes.
- DB (`mariadb_server`, `slurm_db_prep`): habilita accounting de Slurm.
- Slurm core (`slurm_identities`, `munge`, `slurm_facts`, `slurm_rpm_build`, `slurm_install`, `slurm_controller`, `slurm_compute`): instala y activa scheduler.
- LLM (`llm_env`): micromamba + entorno torch/CUDA.
- Validacion (`validate`, `slurm_validate`): comprueba salud y ejecución real de jobs.

## Dependencias importantes

- `slurm_controller` depende de `slurm_install` y de `munge` operativo.
- `slurm_compute` depende de `slurm_install` y de `slurm.conf/gres.conf` ya desplegados.
- `slurm_validate` depende de particiones funcionales y comandos Slurm disponibles en master.
- `llm_env` depende de `nvidia_cuda` para validaciones CUDA consistentes en nodos con GPU.

## Decisiones tecnicas clave

- Configuracion declarativa por roles.
- Separacion de configuracion vs validacion.
- Preferencia por idempotencia (`state`, `creates`, `changed_when: false` en checks).
- Uso de facts (`slurm_facts`) para generar `slurm.conf`/`gres.conf` por nodo.

## Riesgos operativos a controlar

- Cambios de red (`network_internal`, `cluster_routing`) pueden cortar acceso si el inventario no coincide con interfaces reales.
- Cambios de driver NVIDIA pueden requerir reboot.
- Cambios de Slurm sin orden (controller/compute) pueden dejar nodos `DRAIN` o `INVALID_REG`.
