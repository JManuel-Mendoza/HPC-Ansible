# Playbooks, roles y tags

## Playbooks de raiz

- `site.yml`
  - Orquestacion completa del cluster por capas.
- `cleanup_slurm_gpu.yml`
  - Limpieza total (alto riesgo) para reprovision de Slurm/GPU desde cero.

## Orden real de plays en site.yml

1. `Etapa 1 | Baseline HPC (common + ssh)` en `all`
2. `Etapa 2 | Red interna + ruteo + firewall` en `all`
3. `Etapa 3 | CUDA/Driver NVIDIA (solo nodos con GPU)` en `all`
4. `Etapa 4 | NFS HPC (server export)` en `hpc_master`
5. `Etapa 5 | NFS HPC (clientes mount)` en `all:!hpc_master`
6. `Etapa 6 | MariaDB en master` en `hpc_master`
7. `Etapa 7 | Preparar SlurmDB en MariaDB (master)` en `hpc_master`
8. `Etapa 8 | Configuración de identidades SLURM` en `slurm_all`
9. `Etapa 9 | Configuración de Munge en nodos SLURM` en `slurm_all`
10. `Etapa 10 | Recopilación de hechos SLURM en nodos SLURM` en `slurm_all`
11. `Etapa 11 | Configuración de SLURM en nodo master` en `hpc_master`
12. `Etapa 12 | Configuración de SLURM en nodos compute` en `slurm_compute`
13. `Etapa 13 | Entorno LLM (micromamba + torch)` en `all`
14. `Etapa 14 | Validación general de salud del clúster` en `all`
15. `Etapa 15 | Validación Slurm (sin cambios de configuración)` en `hpc_master`

Nota: la secuencia canonica es la definida en `site.yml`; cualquier cambio en `site.yml` se debe reflejar en esta seccion.

## Tags mas utiles

- Baseline: `common`, `ssh`
- Red/ruteo/firewall: `network`, `network_internal`, `routing`, `firewall`
- Storage: `nfs`, `nfs_server`, `nfs_client`
- GPU/CUDA: `cuda`
- LLM: `llm`
- DB/accounting: `mariadb`, `slurmdb`
- Slurm: `slurm`, `slurm_install`, `slurm_config`, `slurmctld`, `slurmd`, `slurmdbd`
- Validacion: `validate`, `slurm_validate`, `slurm_validate_smoke`
- Limpieza: `cleanup`, `cleanup_safety`, `cleanup_services`, `cleanup_packages`, `cleanup_files`, `cleanup_firewall`, `cleanup_verify`

## Ejecuciones parciales sugeridas

- Probar red en un worker:
```bash
ansible-playbook -i inventario.ini site.yml --tags network,routing --limit <worker_activo>
```
Nota: se debe sustituir `<worker_activo>` por un host habilitado en `inventario.ini` (por ejemplo, `worker2`).

- Aplicar solo stack Slurm en master:
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm,slurm_install,slurm_config --limit hpc_master
```

- Ejecutar validacion Slurm:
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm_validate --limit hpc_master
```

- Ejecutar limpieza total de Slurm/GPU en un solo nodo (alto riesgo):
```bash
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --limit <host_habilitado> --tags cleanup,cleanup_verify
```
