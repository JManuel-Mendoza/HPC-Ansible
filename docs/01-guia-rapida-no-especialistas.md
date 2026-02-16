# Guia rapida para no especialistas

## Que problema resuelve este repositorio

Un cluster HPC junta varios servidores para ejecutar trabajos pesados (simulaciones, IA, analitica) de forma coordinada.

Este proyecto usa Ansible para que toda la configuracion sea:
- Automatizada.
- Repetible.
- Auditable.

En lugar de configurar cada servidor a mano, se declara el estado deseado y Ansible lo aplica.

## Componentes explicados en lenguaje simple

- `master`: nodo de control. Coordina el cluster y Slurm.
- `workers`: nodos que ejecutan trabajos.
- Slurm: "orquestador" de trabajos; decide donde y cuando corre cada job.
- NFS: carpeta compartida entre nodos.
- NVIDIA/CUDA: stack para usar GPUs en computo.
- Munge: mecanismo de autenticacion interno entre nodos Slurm.

## Como se usa este repo en la practica

1. Definir hosts en `inventario.ini`.
2. Ajustar variables en `group_vars/` y `host_vars/`.
3. Ejecutar `site.yml` por etapas seguras.
4. Validar resultado con roles de validacion.

## Flujo minimo recomendado

```bash
ansible-galaxy collection install -r requirements.yml
ansible-inventory -i inventario.ini --graph
ansible-playbook -i inventario.ini site.yml --syntax-check
ansible-playbook -i inventario.ini site.yml --check --diff --limit <worker_activo>
ansible-playbook -i inventario.ini site.yml
ansible-playbook -i inventario.ini site.yml --tags validate --limit all
ansible-playbook -i inventario.ini site.yml --tags slurm_validate --limit hpc_master
```

Nota: se debe sustituir `<worker_activo>` por un host habilitado en `inventario.ini` (por ejemplo, `worker2`).

## Que no hacer

- No editar manualmente `slurm.conf`, firewall o red en produccion sin registrar el cambio en Ansible.
- No desplegar cambios de red/firewall/slurm a todos los nodos sin `--limit` y sin validacion previa.
- No dejar secretos en texto plano al compartir el repo.
