# Validacion y evidencia

## Objetivo de validacion

Demostrar que el cluster esta operativo sin introducir cambios no controlados.

## Validaciones implementadas

- `validate`:
  - `uname -a`
  - `sshd -T` (parametros clave)
  - `nvidia-smi -L`
  - prueba torch CUDA en env `llm`

- `slurm_validate`:
  - `sinfo --version`
  - presencia de particiones CPU/GPU
  - ausencia de estados `DOWN/DRAIN/FAIL`
  - `srun` CPU y GPU
  - smoke jobs `sbatch` CPU/GPU
  - `sacct` esperado `COMPLETED|0:0`

## Comandos de evidencia recomendados

```bash
ansible-inventory -i inventario.ini --graph
ansible-playbook -i inventario.ini site.yml --syntax-check
ansible-playbook -i inventario.ini site.yml --check --diff --limit <worker_activo>
ansible-playbook -i inventario.ini site.yml --tags validate --limit all
ansible-playbook -i inventario.ini site.yml --tags slurm_validate --limit hpc_master
```

Nota: se debe sustituir `<worker_activo>` por un host habilitado en `inventario.ini` (por ejemplo, `worker2`).

## Que guardar en bitacora/PR

- Inventario usado.
- `--limit` aplicado.
- Tags ejecutados.
- Salidas relevantes:
  - `sinfo`, `squeue`, `sacct` (resumen),
  - resultado smoke CPU/GPU,
  - resultado torch CUDA.

## Criterios de aceptacion operativa

- Validacion general sin fallos.
- `slurm_validate` sin fallos.
- smoke CPU y GPU completan con `ExitCode 0:0`.
- segunda corrida en `--check --diff` sin drift inesperado.

## Nota de entorno de pruebas local

En este entorno de trabajo se observo:
- `ansible-inventory --graph`: OK.
- `ansible-playbook --syntax-check`: OK con warnings de permisos del sandbox al cargar plugins.

Los warnings de sandbox no describen por si mismos un error del repositorio, pero deben distinguirse de fallas reales en un host objetivo.
