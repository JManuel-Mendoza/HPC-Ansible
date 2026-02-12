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
| `archivo_no_en_uso/docs/bitacora_codex.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/docs/codex-log.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/docs/contexto-actual-hpc-slurm.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/docs/runbooks/slurm-troubleshooting-log.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/docs/slurm-ansible-nvml.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/extras/HPC-Status.txt` | log | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/extras/STATUS.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/extras/historial-comandos-master-26-01.txt` | log | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/extras/hpc-repo-snapshot.zip` | artifact | No referenciado por entrypoints activos | DELETE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/extras/mastersys-status.txt` | log | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/extras/node-hw-short.txt` | log | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/extras/node-hw.txt` | log | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/extras/worker1.txt` | log | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/inventario-glob.ini` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/README.md` | doc | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/artifacts/.gitkeep` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/configs/finetune_lora.yml` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/configs/pretrain_tiny.yml` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/data/processed/.gitkeep` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/data/raw/.gitkeep` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/scripts/00_env_check.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/scripts/00_smoke_gpu.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/scripts/01_prepare_dataset.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/scripts/02_train_tokenizer.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/scripts/03_pretrain_from_scratch.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/scripts/04_finetune_lora.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/scripts/05_infer.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/scripts/_config.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm-project/scripts/_data.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm/code/compare_base_vs_ckpt.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm/code/infer_gpt2.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm/code/run_clm.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm/code/train_clm_with_end.py` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm/slurm tests/llm_clm_endings_3h.sbatch` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm/slurm tests/llm_compare_gpt2.sbatch` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm/slurm tests/llm_express_3h_gpt2.sbatch` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm/slurm tests/llm_express_gpt2.sbatch` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm/slurm tests/llm_infer_endings.sbatch` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm/slurm tests/llm_infer_gpt2.sbatch` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm_project/defaults/main.yml` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/llm_project/tasks/main.yml` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/Acceso/bootstrap_sudo_nopasswd.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/Acceso/workers_lock.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/Acceso/workers_unlock.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/NFS/nfs_hpc.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/Particiones/set_boot_mount_data_scratch.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/Particiones/storage.bash` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/Particiones/storage_data_scratch.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/Red/limpiar_red.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/Red/red_interna.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/Red/redconf.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/Red/w1_w2_link.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/ansible0.cfg` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/inventarios/inventario.ini` | artifact | No referenciado por entrypoints activos | ARCHIVE | HIGH | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/inventarios/inventario_glob.ini` | artifact | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/python env/llm_env.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/python env/llm_env311.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks sueltos/python env/llm_env_reset.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks/ssh-password-toggle.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/playbooks/storage_survey.yml` | playbook | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/slurm-test.sh` | script | No referenciado por entrypoints activos | ARCHIVE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `archivo_no_en_uso/slurm-tests/slurm-tests.zip` | artifact | No referenciado por entrypoints activos | DELETE | LOW | Fuera del flujo activo; conservar solo para trazabilidad historica |
| `base.yml` | playbook | CLI/operator | KEEP | MEDIUM | Entrypoint de ejecucion |
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
| `group_vars/hpc_master.yml` | file | Ansible inventory vars autoload | KEEP | HIGH | Contiene password de SlurmDB en texto plano |
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
