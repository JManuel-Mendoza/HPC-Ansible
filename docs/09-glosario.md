# Glosario

- HPC: High Performance Computing. Uso coordinado de varios nodos para computo intensivo.
- Nodo master: servidor de control del cluster.
- Nodo worker/compute: servidor que ejecuta jobs.
- Slurm: scheduler de trabajos HPC.
- `slurmctld`: daemon controlador de Slurm.
- `slurmd`: daemon de ejecucion en nodos compute.
- `slurmdbd`: daemon de accounting de Slurm.
- Particion Slurm: cola logica de nodos con politicas de ejecucion.
- GRES: Generic RESources, recurso especial (por ejemplo GPU).
- Munge: autenticacion entre servicios Slurm en el cluster.
- NVML: libreria NVIDIA para consultar estado de GPU.
- `nvidia-smi`: CLI para diagnostico/estado de GPUs NVIDIA.
- NFS: Network File System, sistema de archivos compartido por red.
- Idempotencia: ejecutar dos veces y obtener el mismo estado final sin cambios inesperados.
- `--check --diff`: simulacion de Ansible para prever cambios.
- `--limit`: restringe ejecucion a hosts/grupos especificos.
- `--tags`: ejecuta solo subconjuntos de tareas/roles etiquetados.
