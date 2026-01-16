# Bitacora Codex

## Table of Contents
- TBD

## 2026-01-16 11:04 (America/Bogota) — micromamba missing on PATH
**Context:** hosts: all; playbook: site.yml; tags: llm; branch: codex
**Symptom:** bash: micromamba: command not found
**Root cause:** micromamba binary is installed under /opt/micromamba/bin but not on shell PATH.
**Fix:** add an Ansible task to symlink /opt/micromamba/bin/micromamba to /usr/local/bin/micromamba.
**Files changed:** roles/llm_env/tasks/main.yml, docs/bitacora_codex.md
**Validation:** run `which micromamba` (expect `/usr/local/bin/micromamba`), then `micromamba --version` (expect version output); fallback ` /opt/micromamba/bin/micromamba --version`.
**Rollback:** remove symlink (`rm /usr/local/bin/micromamba`) and revert the task in `roles/llm_env/tasks/main.yml`.
**Notes:** none.

## 2026-01-16 11:29 (America/Bogota) — llm env missing in micromamba
**Context:** hosts: all; playbook: site.yml; tags: llm; branch: codex
**Symptom:** `micromamba env list` shows only `base`; `micromamba run -n llm ...` fails because env does not exist.
**Root cause:** llm env creation was not enforced with a root prefix and idempotent check, so env was never created on the expected root.
**Fix:** add an idempotent env creation task using `MAMBA_ROOT_PREFIX=/opt/micromamba`, plus a pip install step gated by a marker file; set the same root prefix for validate's torch check.
**Files changed:** roles/llm_env/tasks/main.yml, roles/validate/tasks/main.yml, docs/bitacora_codex.md
**Validation:** run `micromamba env list` (expect `llm` present), `micromamba run -n llm python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"` (expect torch import and CUDA boolean), and `ansible-playbook -i inventario.ini site.yml --tags llm`.
**Rollback:** remove the new tasks from `roles/llm_env/tasks/main.yml` and the env prefix from `roles/validate/tasks/main.yml`, then remove the env with `/opt/micromamba/bin/micromamba env remove -n llm` if needed.
**Notes:** fallback commands: `/opt/micromamba/bin/micromamba env list` and `/opt/micromamba/bin/micromamba run -n llm ...`.

## 2026-01-16 12:01 (America/Bogota) — conda changed status + pip hash marker
**Context:** hosts: all; playbook: site.yml; tags: llm; branch: codex
**Symptom:** "Install/update conda packages in existing env" reports changed even when micromamba prints "All requested packages already installed"; pip install is skipped due to a static marker.
**Root cause:** command module marks changed unless overridden; pip marker used a fixed filename, so it never re-runs when the package list changes.
**Fix:** set `changed_when` to false when micromamba reports no changes; compute a sha1 hash of `llm_pip_packages` and use a hashed marker file so pip installs re-run only when the package list changes.
**Files changed:** roles/llm_env/tasks/main.yml, docs/bitacora_codex.md
**Validation:** `ansible-playbook -i inventario.ini site.yml --limit hpc_master --tags llm` (expect conda task OK when no changes; pip install skips unless package list changes).
**Rollback:** revert the `changed_when` and hash marker edits in `roles/llm_env/tasks/main.yml`, then remove any `/.llm_pip_installed_*` marker files if needed.
**Notes:** none.
