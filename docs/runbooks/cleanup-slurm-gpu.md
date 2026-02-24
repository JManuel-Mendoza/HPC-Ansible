# Runbook: cleanup_slurm_gpu.yml (alto riesgo)

Este runbook documenta el uso de `cleanup_slurm_gpu.yml`, playbook de limpieza total para reprovisionar Slurm + GPU/CUDA desde cero.

## Alcance real de la limpieza

El playbook:
- detiene y deshabilita `slurmctld`, `slurmd`, `slurmdbd`, `munge`, `nvidia-persistenced`,
- elimina paquetes `slurm*`, `munge*`, `nvidia*`, `cuda*`,
- elimina configuraciones/directorios de Slurm y Munge (`/etc/slurm`, `/var/log/slurm`, `/etc/munge`, etc.),
- limpia reglas de firewall asociadas a Slurm (`6817`, `6818`, `SrunPortRange`),
- preserva acceso SSH si `cleanup_preserve_ssh=true` (default).

No es un runbook de mantenimiento rutinario. Se usa en recuperación o reconstrucción.

## Reglas de seguridad operativa

- Ejecutar solo en ventana de mantenimiento.
- Empezar por un único nodo con `--limit`.
- Validar tags antes de ejecutar (`--list-tags`).
- Confirmar conectividad SSH al final de cada corrida.
- Reprovisionar inmediatamente con `site.yml` por etapas una vez finalizada la limpieza.

## Ejecución recomendada

1. Inspeccionar tags:
```bash
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --list-tags
```

2. Prueba de limpieza/verificación en un solo nodo:
```bash
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --limit <host_habilitado> --tags cleanup,cleanup_verify
```

3. Limpieza completa en el nodo:
```bash
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --limit <host_habilitado>
```

4. Reprovision del nodo:
```bash
ansible-playbook -i inventario.ini site.yml --tags slurm,cuda,llm,validate --limit <host_habilitado>
ansible-playbook -i inventario.ini site.yml --tags slurm_validate --limit hpc_master
```

## Tags útiles del playbook

- `cleanup`: ejecución general de limpieza.
- `cleanup_safety`: tareas para preservar acceso remoto.
- `cleanup_services`, `cleanup_packages`, `cleanup_files`: limpieza por capa.
- `cleanup_firewall`: limpieza de reglas de firewall.
- `cleanup_verify`: evidencia de residuos y estado final.

## Reversión

No hay rollback transaccional del estado previo. La recuperación esperada es:
- volver a aprovisionar con `site.yml` por etapas,
- validar con `validate` y `slurm_validate`.

## Evidencia mínima a guardar

- comando ejecutado con inventario/limit/tags,
- hosts afectados,
- salida de `cleanup_verify`,
- resultado de validación posterior (`slurm_validate` y checks CUDA).
