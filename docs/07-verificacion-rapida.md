# Verificación rápida (smoke)

## Propósito

Esta guía valida que el entrypoint `site.yml` está operativo en un nivel mínimo:
- inventario y sintaxis;
- disponibilidad de tags;
- checks rápidos de Slurm sin cambios de configuración;
- smoke jobs CPU/GPU de Slurm.

Esta guía NO valida rendimiento de clúster, tuning fino de Slurm/CUDA ni cobertura completa de todos los roles.

## Checklist (5 pasos)

1. Verificar inventario (sin cambios en nodos):

```bash
ansible-inventory -i inventario.ini --graph
```

2. Verificar sintaxis del playbook principal:

```bash
ansible-playbook -i inventario.ini site.yml --syntax-check
```

3. Verificar tags disponibles para ejecución parcial:

```bash
ansible-playbook -i inventario.ini site.yml --list-tags
```

4. Ejecutar validación rápida de red/Slurm (solo lectura):

```bash
ansible-playbook -i inventario.ini site.yml --tags validate_slurm --limit "hpc_master,slurm_compute"
```

5. Ejecutar smoke real de Slurm (CPU+GPU jobs):

```bash
ansible-playbook -i inventario.ini site.yml --tags slurm_validate_smoke
```

Nota: en waits del smoke pueden aparecer líneas `FAILED - RETRYING`; es esperable mientras el job sigue en cola y no implica fallo final por sí solo.

## Nota sobre credenciales

El repo ya no usa Ansible Vault. Las credenciales operativas viven directamente en `inventario.ini` y `group_vars/hpc_master.yml`.

## Qué hacer si falla

- Fallas de scheduler/control/compute/accounting: `docs/runbooks/slurm.md`
- Fallas de GPU/CUDA/PyTorch: `docs/runbooks/gpu-cuda.md`
- Fallas de red/rutas/firewall: `docs/runbooks/network-firewall.md`
- Fallas de export/mount NFS: `docs/runbooks/nfs.md`

## Prueba canary recomendada

```bash
ansible-playbook -i inventario.ini site.yml --limit "hpc_master,worker2" -f 10
```

Esta canary valida ejecución end-to-end en un subconjunto representativo antes de correr sobre toda la granja.
