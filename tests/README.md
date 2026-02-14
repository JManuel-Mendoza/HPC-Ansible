# Campaña de pruebas E2E (Ansible + HPC)

Objetivo: ejecutar una campaña end-to-end para verificar que el repo y el clúster están operativos (Ansible, NFS, Slurm, GPU/CUDA y validaciones).

Reglas operativas:
- No exponer secretos: no imprimir Vault ni credenciales.
- Guardar logs bajo `tests/results/<YYYYMMDD-HHMM>/`.
- Canary primero: `hpc_master` + 1 worker; si falla, detener antes de full cluster.
- Evitar cuelgues: usar `timeout 15` en `df`/`showmount` cuando aplique.

## Requisitos (control node)

1) Colecciones:
```bash
ansible-galaxy collection install -r requirements.yml
```

2) Vault:
- El repo usa `group_vars/all/vault.yml` (cifrado). Ver `docs/vault.md`.
- Recomendado para automatizar sin prompt:
```bash
export ANSIBLE_VAULT_PASSWORD_FILE=~/.config/hpc-ansible/vault-pass.txt
```

## Dónde se guardan los resultados

- Logs: `tests/results/<ts>/preflight/`, `tests/results/<ts>/canary/`, `tests/results/<ts>/full/`
- Reporte final: `docs/audit/test-report-<ts>.md`

Nota: `tests/results/` no se commitea (está ignorado por git).

## Comandos clave (manual)

Preflight (sin tocar nodos):
```bash
ansible-inventory -i inventario.ini --graph --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --list-tasks --ask-vault-pass
```

Canary (recomendado: master + 1 worker):
```bash
ansible -i inventario.ini 'master:<worker_canary>' -m ping --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --limit 'master,<worker_canary>' --ask-vault-pass --skip-tags debug
ansible-playbook -i inventario.ini site.yml --limit 'master,<worker_canary>' --tags validate --ask-vault-pass --skip-tags debug
```

Full (solo si canary pasa):
```bash
ansible-playbook -i inventario.ini site.yml --ask-vault-pass --skip-tags debug
ansible-playbook -i inventario.ini site.yml --ask-vault-pass --skip-tags debug
ansible-playbook -i inventario.ini site.yml --tags validate --ask-vault-pass --skip-tags debug
```

