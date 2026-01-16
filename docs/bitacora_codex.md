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
