# File Ledger

Auditoria archivo-por-archivo del repositorio (sin cambios de logica).

| Ruta | Tipo | Referenciado por | Recomendacion | Riesgo | Notas |
|---|---|---|---|---|---|
| `.DS_Store` | file | No determinado | DELETE | MEDIUM |  |
| `.agents/skills/code-documenter/SKILL.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/code-documenter/references/api-docs-fastapi-django.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/code-documenter/references/api-docs-nestjs-express.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/code-documenter/references/coverage-reports.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/code-documenter/references/documentation-systems.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/code-documenter/references/interactive-api-docs.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/code-documenter/references/python-docstrings.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/code-documenter/references/typescript-jsdoc.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/code-documenter/references/user-guides-tutorials.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/documentation-generation-doc-generate/SKILL.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/documentation-generation-doc-generate/resources/implementation-playbook.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/markdown-documentation/SKILL.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/mermaid-diagrams/SKILL.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/mermaid-diagrams/references/advanced-features.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/mermaid-diagrams/references/architecture-diagrams.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/mermaid-diagrams/references/c4-diagrams.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/mermaid-diagrams/references/class-diagrams.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/mermaid-diagrams/references/erd-diagrams.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/mermaid-diagrams/references/flowcharts.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/mermaid-diagrams/references/sequence-diagrams.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/technical-writing/SKILL.md` | doc | AGENTS.md / runtime de agente | KEEP | LOW |  |
| `.agents/skills/technical-writing/SKILL.toon` | file | AGENTS.md / runtime de agente | KEEP | MEDIUM |  |
| `.gitignore` | file | No determinado | KEEP | MEDIUM |  |
| `AGENTS.md` | doc | No determinado | KEEP | LOW |  |
| `README.md` | doc | No determinado | KEEP | LOW |  |
| `ansible.cfg` | file | ansible-playbook (autoload) | KEEP | MEDIUM |  |
| `docs/docs_old/README.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Documentación histórica; no vigente |
| `docs/docs_old/bitacora_codex.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Documentación histórica; no vigente |
| `docs/docs_old/codex-log.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Documentación histórica; no vigente |
| `docs/docs_old/contexto-actual-hpc-slurm.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Documentación histórica; no vigente |
| `docs/docs_old/runbooks/slurm-troubleshooting-log.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Documentación histórica; no vigente |
| `docs/docs_old/slurm-ansible-nvml.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Documentación histórica; no vigente |
| `docs/00-indice.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/01-guia-rapida-no-especialistas.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/02-arquitectura-ejecucion.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/03-inventario-y-variables.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/04-playbooks-roles-y-tags.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/05-referencia-roles.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/06-referencia-archivos.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/07-runbooks-operativos.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/08-validacion-y-evidencia.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/09-glosario.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/audit/ansible-entrypoints.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/audit/file-ledger.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/audit/findings.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `docs/audit/task-matrix.md` | doc | README.md / navegacion documental | KEEP | LOW |  |
| `group_vars/all.yml` | file | Ansible inventory vars autoload | KEEP | MEDIUM |  |
| `group_vars/all/vars.yml` | file | Ansible inventory vars autoload | KEEP | MEDIUM | Variables operacionales (topologia/red/firewall/slurm) para replicación |
| `group_vars/hpc_master.yml` | file | Ansible inventory vars autoload | KEEP | HIGH | Variables del master (router/NFS/MariaDB). Passwords deben venir de Vault (vault-backed). |
| `host_vars/master.yml` | file | Ansible inventory vars autoload | KEEP | MEDIUM |  |
| `host_vars/worker1.yml` | file | Ansible inventory vars autoload | KEEP | MEDIUM |  |
| `host_vars/worker2.yml` | file | Ansible inventory vars autoload | KEEP | MEDIUM |  |
| `inventario.ini` | file | ansible.cfg -> inventory | KEEP | HIGH | Contiene datos sensibles y credenciales en texto plano |
| `requirements.yml` | file | ansible-galaxy collection install | KEEP | MEDIUM |  |
| `roles/cluster_routing/tasks/main.yml` | role | site.yml (role cluster_routing) | KEEP | HIGH |  |
| `roles/common/tasks/main.yml` | role | site.yml (role common) | KEEP | MEDIUM |  |
| `roles/firewall/tasks/main.yml` | role | site.yml (role firewall) | KEEP | HIGH |  |
| `roles/llm_env/defaults/main.yml` | role | autoload de rol llm_env | KEEP | MEDIUM |  |
| `roles/llm_env/tasks/main.yml` | role | site.yml (role llm_env) | KEEP | MEDIUM |  |
| `roles/mariadb_server/defaults/main.yml` | role | autoload de rol mariadb_server | KEEP | MEDIUM |  |
| `roles/mariadb_server/tasks/main.yml` | role | site.yml (role mariadb_server) | KEEP | MEDIUM |  |
| `roles/munge/handlers/main.yml` | role | notify desde roles/munge/tasks/*.yml | KEEP | HIGH |  |
| `roles/munge/tasks/main.yml` | role | site.yml (role munge) | KEEP | HIGH |  |
| `roles/network_internal/defaults/main.yml` | role | autoload de rol network_internal | KEEP | HIGH |  |
| `roles/network_internal/tasks/main.yml` | role | site.yml (role network_internal) | KEEP | HIGH |  |
| `roles/network_internal/tasks/master_link.yml` | role | roles/network_internal/tasks/main.yml (include/import) | KEEP | HIGH |  |
| `roles/nfs_hpc/defaults/main.yml` | role | autoload de rol nfs_hpc | KEEP | HIGH |  |
| `roles/nfs_hpc/handlers/main.yml` | role | notify desde roles/nfs_hpc/tasks/*.yml | KEEP | HIGH |  |
| `roles/nfs_hpc/tasks/main.yml` | role | site.yml (role nfs_hpc) | KEEP | HIGH |  |
| `roles/nfs_hpc/templates/exports.j2` | template | roles/nfs_hpc/tasks/main.yml | KEEP | HIGH |  |
| `roles/nvidia_cuda/defaults/main.yml` | role | autoload de rol nvidia_cuda | KEEP | HIGH |  |
| `roles/nvidia_cuda/handlers/main.yml` | role | notify desde roles/nvidia_cuda/tasks/*.yml | KEEP | HIGH |  |
| `roles/nvidia_cuda/tasks/main.yml` | role | site.yml (role nvidia_cuda) | KEEP | HIGH |  |
| `roles/slurm_compute/tasks/main.yml` | role | site.yml (role slurm_compute) | KEEP | MEDIUM |  |
| `roles/slurm_controller/defaults/main.yml` | role | autoload de rol slurm_controller | KEEP | HIGH |  |
| `roles/slurm_controller/tasks/main.yml` | role | site.yml (role slurm_controller) | KEEP | HIGH |  |
| `roles/slurm_controller/templates/slurmdbd.conf.j2` | template | roles/slurm_controller/tasks/main.yml | KEEP | HIGH |  |
| `roles/slurm_db_prep/handlers/main.yml` | role | notify desde roles/slurm_db_prep/tasks/*.yml | KEEP | HIGH |  |
| `roles/slurm_db_prep/tasks/main.yml` | role | site.yml (role slurm_db_prep) | KEEP | HIGH |  |
| `roles/slurm_facts/tasks/main.yml` | role | site.yml (role slurm_facts) | KEEP | MEDIUM |  |
| `roles/slurm_identities/tasks/main.yml` | role | site.yml (role slurm_identities) | KEEP | MEDIUM |  |
| `roles/slurm_install/defaults/main.yml` | role | autoload de rol slurm_install | KEEP | HIGH |  |
| `roles/slurm_install/files/slurm.conf` | file | roles/slurm_install/tasks/main.yml | ARCHIVE | HIGH | No se observa consumo activo en tasks; existe template slurm.conf.j2 administrado |
| `roles/slurm_install/handlers/main.yml` | role | notify desde roles/slurm_install/tasks/*.yml | KEEP | HIGH |  |
| `roles/slurm_install/tasks/main.yml` | role | site.yml (role slurm_install) | KEEP | HIGH |  |
| `roles/slurm_install/tasks/slurmdbd_hygiene.yml` | role | roles/slurm_install/tasks/main.yml (include/import) | KEEP | HIGH |  |
| `roles/slurm_install/templates/gres.conf.j2` | template | roles/slurm_install/tasks/main.yml | KEEP | HIGH |  |
| `roles/slurm_install/templates/slurm.conf.j2` | template | roles/slurm_install/tasks/main.yml | KEEP | HIGH |  |
| `roles/slurm_rpm_build/tasks/main.yml` | role | site.yml (role slurm_rpm_build) | KEEP | MEDIUM |  |
| `roles/slurm_validate/defaults/main.yml` | role | autoload de rol slurm_validate | KEEP | MEDIUM |  |
| `roles/slurm_validate/tasks/main.yml` | role | site.yml (role slurm_validate) | KEEP | MEDIUM |  |
| `roles/slurm_validate/templates/slurm-smoke-cpu.sbatch.j2` | template | roles/slurm_validate/tasks/main.yml | KEEP | MEDIUM |  |
| `roles/slurm_validate/templates/slurm-smoke-gpu.sbatch.j2` | template | roles/slurm_validate/tasks/main.yml | KEEP | MEDIUM |  |
| `roles/users_ssh/defaults/main.yml` | role | autoload de rol users_ssh | KEEP | HIGH |  |
| `roles/users_ssh/handlers/main.yml` | role | notify desde roles/users_ssh/tasks/*.yml | KEEP | HIGH |  |
| `roles/users_ssh/tasks/main.yml` | role | site.yml (role users_ssh) | KEEP | HIGH |  |
| `roles/validate/defaults/main.yml` | role | autoload de rol validate | KEEP | MEDIUM |  |
| `roles/validate/tasks/main.yml` | role | site.yml (role validate) | KEEP | MEDIUM |  |
| `roles/validate/tasks/slurm.yml` | role | roles/validate/tasks/main.yml (include/import) | KEEP | MEDIUM |  |
| `site.yml` | playbook | CLI/operator | KEEP | MEDIUM | Entrypoint de ejecucion |
| `tools/generate_audit_docs.py` | script | No determinado | KEEP | MEDIUM |  |
