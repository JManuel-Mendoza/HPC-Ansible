# Referencia de archivos

Esta referencia cubre los archivos de codigo y operacion del proyecto. Documentación histórica se conserva en `docs/docs_old/` (ver `docs/docs_old/README.md`).

## Raiz

- `site.yml`: playbook principal de orquestacion por capas.
- `ansible.cfg`: defaults de ejecucion (inventario, callbacks, become).
- `inventario.ini`: grupos/hosts y vars globales de conexion.
- `requirements.yml`: colecciones Ansible requeridas.
- `README.md`: entrada principal del repositorio.
- `AGENTS.md`: reglas operativas para agentes en este repo.

## Soporte para agentes/documentacion

- `.agents/skills/code-documenter/SKILL.md`: skill para documentar codigo/API.
- `.agents/skills/code-documenter/references/*`: referencias para documentacion de API y guias.
- `.agents/skills/documentation-generation-doc-generate/SKILL.md`: skill de generacion documental.
- `.agents/skills/documentation-generation-doc-generate/resources/implementation-playbook.md`: playbook de implementacion documental.
- `.agents/skills/markdown-documentation/SKILL.md`: buenas practicas de Markdown.
- `.agents/skills/mermaid-diagrams/SKILL.md`: guias para diagramas Mermaid.
- `.agents/skills/mermaid-diagrams/references/*`: referencias de diagramas (flow, sequence, C4, etc.).
- `.agents/skills/technical-writing/SKILL.md`: skill para redaccion tecnica.
- `.agents/skills/technical-writing/SKILL.toon`: variante de configuracion para el skill de redaccion.

Nota:
- Estos archivos no cambian la logica de aprovisionamiento HPC; son guias para agentes/LLM.

## Variables

- `group_vars/all.yml`: defaults globales de baseline (paquetes, chrony, SSH, LLM).
- `group_vars/all/vars.yml`: variables operacionales para replicabilidad (Slurm, red interna, firewall).
- `group_vars/all/vault.yml`: secretos cifrados con Ansible Vault (no editar sin `ansible-vault`).
- `group_vars/hpc_master.yml`: ajustes especificos del master (router, NFS server, MariaDB/SlurmDBD).
- `host_vars/master.yml`: ejemplos de override de recursos Slurm.
- `host_vars/worker1.yml`: ejemplos de override por nodo.
- `host_vars/worker2.yml`: ejemplos de override por nodo.

## Para replicar en otro HPC (que editar)

Edicion recomendada (en este orden):

1. `inventario.ini`
- IPs/hostnames reales, usuario SSH y pertenencia a grupos (`hpc_master`, `workers_*`, `slurm_*`).
- Vars de conexion en `[all:vars]` (p. ej. `ansible_ssh_private_key_file`).

2. `group_vars/all/vars.yml`
- CIDRs/subredes internas, puertos, particiones Slurm, UID/GID y topologia del controller.

3. `group_vars/hpc_master.yml`
- Interfaces del master que enruta (`hpc_router_internal_ifaces`) y servicios del master (NFS/MariaDB/SlurmDBD).

4. `group_vars/all.yml`
- Paquetes base, SSH y entorno LLM (micromamba) segun el perfil de tu laboratorio.

5. `group_vars/all/vault.yml`
- Secretos (solo via Vault). Ver `docs/vault.md`.

## Roles

### common
- `roles/common/tasks/main.yml`: paquetes base + chrony.

### users_ssh
- `roles/users_ssh/defaults/main.yml`: defaults SSH.
- `roles/users_ssh/tasks/main.yml`: include/drop-in de sshd y validacion.
- `roles/users_ssh/handlers/main.yml`: restart sshd.

### firewall
- `roles/firewall/tasks/main.yml`: firewalld + reglas Slurm.

### network_internal
- `roles/network_internal/defaults/main.yml`: mapa de enlaces internos por host.
- `roles/network_internal/tasks/main.yml`: lifecycle de conexiones NM y `/etc/hosts`.
- `roles/network_internal/tasks/master_link.yml`: subflujo de enlace master-<worker>.

### cluster_routing
- `roles/cluster_routing/tasks/main.yml`: forwarding y rutas persistentes entre subredes.

### nfs_hpc
- `roles/nfs_hpc/defaults/main.yml`: defaults NFS (server/client/share/permisos).
- `roles/nfs_hpc/tasks/main.yml`: provision NFS.
- `roles/nfs_hpc/handlers/main.yml`: recarga exports/firewalld.
- `roles/nfs_hpc/templates/exports.j2`: linea de export NFS.

### nvidia_cuda
- `roles/nvidia_cuda/defaults/main.yml`: defaults driver/repo/validacion.
- `roles/nvidia_cuda/tasks/main.yml`: instalacion y validacion GPU/CUDA.
- `roles/nvidia_cuda/handlers/main.yml`: initramfs/reboot.

### llm_env
- `roles/llm_env/defaults/main.yml`: defaults de micromamba/env.
- `roles/llm_env/tasks/main.yml`: entorno Python/torch CUDA.

### mariadb_server
- `roles/mariadb_server/defaults/main.yml`: version minima y flags base.
- `roles/mariadb_server/tasks/main.yml`: instalacion/validacion MariaDB.

### slurm_db_prep
- `roles/slurm_db_prep/tasks/main.yml`: DB+usuarios+grants para Slurm.
- `roles/slurm_db_prep/handlers/main.yml`: restart MariaDB.

### validate
- `roles/validate/defaults/main.yml`: toggles de validacion.
- `roles/validate/tasks/main.yml`: checks generales.
- `roles/validate/tasks/slurm.yml`: checks de puertos/conectividad Slurm.

### slurm_identities
- `roles/slurm_identities/tasks/main.yml`: usuarios/grupos slurm/munge.

### munge
- `roles/munge/tasks/main.yml`: instalacion y distribucion de key.
- `roles/munge/handlers/main.yml`: restart munge.

### slurm_facts
- `roles/slurm_facts/tasks/main.yml`: facts de CPU/mem/GPU para templates.

### slurm_rpm_build
- `roles/slurm_rpm_build/tasks/main.yml`: build de RPMs Slurm.

### slurm_install
- `roles/slurm_install/defaults/main.yml`: rutas de cache/staging RPM.
- `roles/slurm_install/tasks/main.yml`: instalacion y config Slurm.
- `roles/slurm_install/tasks/slurmdbd_hygiene.yml`: higiene runtime slurmdbd.
- `roles/slurm_install/handlers/main.yml`: tmpfiles/restart slurmdbd.
- `roles/slurm_install/templates/slurm.conf.j2`: configuracion Slurm completa por facts.
- `roles/slurm_install/templates/gres.conf.j2`: configuracion GRES/NVML.
- `roles/slurm_install/files/slurm.conf`: archivo de referencia historico.

### slurm_controller
- `roles/slurm_controller/defaults/main.yml`: toggles reconfigure/autoresume.
- `roles/slurm_controller/tasks/main.yml`: gestion de slurmctld/slurmdbd.
- `roles/slurm_controller/templates/slurmdbd.conf.j2`: config slurmdbd.

### slurm_compute
- `roles/slurm_compute/tasks/main.yml`: gestion de slurmd en compute.

### slurm_validate
- `roles/slurm_validate/defaults/main.yml`: defaults de validacion/smoke.
- `roles/slurm_validate/tasks/main.yml`: pruebas read-only Slurm.
- `roles/slurm_validate/templates/slurm-smoke-cpu.sbatch.j2`: smoke CPU.
- `roles/slurm_validate/templates/slurm-smoke-gpu.sbatch.j2`: smoke GPU.
