# Repository Guidelines

This repository provisions an HPC cluster (master + workers) with Ansible. Use the pointers below to contribute safely and consistently.

## Project Structure & Module Organization
- `site.yml` is the main playbook (baseline, NFS, validation); `base.yml` provides a lightweight pre-flight setup.
- `roles/` holds layered roles (`common`, `users_ssh`, `firewall`, `nvidia_cuda`, `llm_env`, `nfs_server`, `nfs_client`, `llm_project`, `validate`), each with the standard `tasks/`, `defaults/`, `vars/` folders as needed.
- `group_vars/all.yml`, `group_vars/hpc_master.yml`, and `group_vars/workers.yml` centralize defaults per scope; add host-specific overrides under `host_vars/<hostname>.yml`.
- `inventario.ini` is the default inventory (set in `ansible.cfg`); `inventario_glob.ini` is available for alternate groupings. Extra ad-hoc materials live in `playbooks sueltos/` and `llm-project/` (artifacts/configs/scripts shared via NFS).

## Build, Test, and Development Commands
- Install dependencies: `ansible-galaxy collection install -r requirements.yml`.
- Main run: `ansible-playbook -i inventario.ini site.yml` (narrow scope with `--limit workers` or `--tags cuda,llm`).
- Dry run: `ansible-playbook -i inventario.ini site.yml --check --diff` to confirm idempotence before touching hosts.
- Syntax check: `ansible-playbook -i inventario.ini site.yml --syntax-check`.
- Inventory sanity: `ansible-inventory -i inventario.ini --graph` to verify host grouping before executions.

## Coding Style & Naming Conventions
- YAML: 2-space indent, hyphenated lists, lowercase keys; keep task names concise in Spanish and action-oriented.
- Prefer fully qualified module names (`ansible.builtin.*`, `ansible.posix.*`), declare `state` for idempotence, and guard optional steps with booleans (e.g., `enable_chrony`).
- Variables use `snake_case`; defaults that can be overridden belong in `roles/<role>/defaults/main.yml`. Keep tags aligned with the role names defined in `site.yml` (`common`, `ssh`, `firewall`, `cuda`, `llm`, `nfs`, `llm_project`, `validate`).

## Testing Guidelines
- Before pushing, run syntax-check plus `--check` for the roles you changed; limit scope (`--limit hpc_master`, `--tags llm_project`) to shorten feedback.
- Use `--tags validate` after major changes to confirm NFS exports/mounts, CUDA visibility (`nvidia-smi`), and LLM env readiness.
- Capture and share relevant command outputs (especially validation steps) in PRs to document host-side effects.

## Commit & Pull Request Guidelines
- Commit messages in this repo are short, present-tense, and descriptive (e.g., `ajustes mínimos de variables del master`). Follow that tone; optionally prefix a scope (`role/llm_env: ajusta paquetes`).
- In PRs, include: what changed, which inventories/vars/roles you touched, the commands you ran (`--check`, `--tags validate`, etc.), and any host limits used. Link issues when relevant; add screenshots only if they clarify validation output.

## Security & Configuration Tips
- Avoid committing credentials or real host secrets; keep them in `host_vars` encrypted with Ansible Vault when needed.
- `ansible.cfg` disables host key checking for convenience—re-enable it for production or sensitive environments.
- Update `inventario*.ini` with sanitized hostnames/IPs before sharing externally to prevent leaking infrastructure details.
