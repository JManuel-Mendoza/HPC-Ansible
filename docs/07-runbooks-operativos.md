# Runbooks operativos

## Runbook 1: bootstrap controlado de cluster

1. Validar inventario:
```bash
ansible-inventory -i inventario.ini --graph
```
2. Verificar sintaxis:
```bash
ansible-playbook -i inventario.ini site.yml --syntax-check
```
3. Dry-run acotado:
```bash
ansible-playbook -i inventario.ini site.yml --check --diff --limit <worker_activo>
```
Nota: en los ejemplos con `<worker_activo>`, se debe sustituir por un host habilitado en `inventario.ini` (por ejemplo, `worker2`).
4. Baseline por capas:
```bash
ansible-playbook -i inventario.ini site.yml --tags common,ssh,firewall,network,routing,nfs,cuda,llm --limit all
```
5. Slurm master:
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm,munge,identities,slurm_install,slurm_config --limit hpc_master
```
6. Slurm compute:
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm,munge,identities,slurm_install,slurm_config --limit slurm_compute
```
7. Validaciones:
```bash
ansible-playbook -i inventario.ini site.yml --tags validate --limit all
ansible-playbook -i inventario.ini site.yml --tags slurm_validate --limit hpc_master
```

## Runbook 2: cambio de red interna

- Riesgo alto: puede afectar conectividad.
- Procedimiento:
  1. Ajustar `network_internal_links` y/o `hpc_internal_subnets`.
  2. Aplicar primero en un worker:
```bash
ansible-playbook -i inventario.ini site.yml --tags network,routing --limit <worker_activo>
```
  3. Verificar acceso SSH y rutas.
  4. Escalar gradualmente al resto.

## Runbook 3: cambio de driver NVIDIA/CUDA

1. Probar en un nodo GPU:
```bash
ansible-playbook -i inventario.ini site.yml --tags cuda --limit <worker_activo>
```
2. Validar:
```bash
ansible-playbook -i inventario.ini site.yml --tags validate --limit <worker_activo>
```
3. Revisar si el rol solicita reboot.
4. Escalar a otros nodos por lotes pequenos.

## Runbook 4: cambio de configuracion Slurm

1. Aplicar en master:
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm,slurm_install,slurm_config --limit hpc_master
```
2. Aplicar en compute:
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm,slurm_install,slurm_config --limit slurm_compute
```
3. Validar particiones/jobs:
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm_validate --limit hpc_master
```

## Runbook 5: troubleshooting rapido

- `slurmd` no arranca:
  - revisar `slurm.conf` y `gres.conf` desplegados,
  - revisar permisos en `/var/spool/slurmd` y `/var/log/slurm`.
- `nvidia-smi` falla:
  - revisar modulos `nvidia`/`nouveau`,
  - revisar reboot pendiente,
  - revisar paquetes 590 conflictivos.
- Jobs GPU fallan:
  - confirmar particion `gpu`,
  - confirmar `--gres=gpu:1`,
  - correr `slurm_validate` smoke.

## Runbook 6: limpieza total de Slurm/GPU (alto riesgo)

Usar solo para reprovisionar desde cero cuando el estado del nodo no es recuperable con reconfiguracion normal.

1. Revisar tags disponibles:
```bash
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --list-tags
```
2. Ejecutar primero en un solo nodo:
```bash
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --limit <host_habilitado> --tags cleanup,cleanup_verify
```
3. Si la limpieza fue correcta, ejecutar limpieza completa en el mismo nodo:
```bash
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --limit <host_habilitado>
```
4. Reprovisionar el nodo con `site.yml` por etapas (`slurm`, `cuda`, `validate`, `slurm_validate`).

Referencia detallada: `docs/runbooks/cleanup-slurm-gpu.md`.
