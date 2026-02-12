# Playbooks, roles y tags

## Playbooks de raiz

- `site.yml`
  - Orquestacion completa del cluster por capas.
- `base.yml`
  - Pre-flight simple para baseline minimo de paquetes.

## Orden real de plays en site.yml

1. Baseline en `all`:
   - `common`, `users_ssh`, `firewall`, `network_internal`, `cluster_routing`, `nfs_hpc`, `nvidia_cuda`, `llm_env`
2. `mariadb_server` en `hpc_master`
3. `slurm_db_prep` en `hpc_master`
4. `validate` en `all`
5. `slurm_identities` en `all`
6. `munge` en `all`
7. `slurm_facts` en `all`
8. En `hpc_master`:
   - `slurm_rpm_build`, `slurm_install`, `slurm_controller`
9. En `slurm_compute`:
   - `slurm_install`, `slurm_compute`
10. `slurm_validate` en `hpc_master`

## Tags mas utiles

- Baseline: `common`, `ssh`, `firewall`, `network`, `routing`, `nfs`, `cuda`, `llm`
- DB/accounting: `mariadb`, `slurmdb`
- Slurm: `slurm`, `slurm_install`, `slurm_config`, `slurmctld`, `slurmd`, `slurmdbd`
- Validacion: `validate`, `slurm_validate`, `slurm_validate_smoke`

## Ejecuciones parciales sugeridas

- Probar red en un worker:
```bash
ansible-playbook -i inventario.ini site.yml --tags network,routing --limit worker1
```

- Aplicar solo stack Slurm en master:
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm,slurm_install,slurm_config --limit hpc_master
```

- Ejecutar validacion Slurm:
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm_validate --limit hpc_master
```
