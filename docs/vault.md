# Guía rápida de Ansible Vault

Esta guía define el uso recomendado de Ansible Vault en este proyecto para evitar credenciales en claro dentro del repositorio.

## Objetivo

Los secretos deben mantenerse cifrados en un único archivo:

- `group_vars/all/vault.yml`

Las referencias funcionales deben permanecer en:

- `inventario.ini`
- `group_vars/hpc_master.yml`

## Secretos que deben vivir en Vault

Para el estado actual del repositorio, como mínimo:

- `vault_ansible_become_password_workers_u`
- `vault_slurmdb_mysql_password`

## Puntos de consumo recomendados

### 1. `inventario.ini`

En el grupo `workers_u:vars`, la contraseña de elevación debe referenciar Vault:

```ini
[workers_u:vars]
ansible_become_password="{{ vault_ansible_become_password_workers_u }}"
```

### 2. `group_vars/hpc_master.yml`

La contraseña de MariaDB para Slurm debe referenciar Vault:

```yaml
slurmdb_mysql_password: "{{ vault_slurmdb_mysql_password }}"
```

## Estructura recomendada del archivo cifrado

Se recomienda crear un archivo temporal en claro con este contenido:

```yaml
vault_ansible_become_password_workers_u: "CAMBIAR_ESTE_VALOR"
vault_slurmdb_mysql_password: "CAMBIAR_ESTE_VALOR"
```

Después debe cifrarse y moverse a la ruta definitiva:

```bash
cat > /tmp/vault.yml <<'EOF'
vault_ansible_become_password_workers_u: "CAMBIAR_ESTE_VALOR"
vault_slurmdb_mysql_password: "CAMBIAR_ESTE_VALOR"
EOF

ansible-vault encrypt /tmp/vault.yml
mv /tmp/vault.yml group_vars/all/vault.yml
```

## Edición posterior de secretos

```bash
ansible-vault edit group_vars/all/vault.yml
```

## Ejecución habitual con Vault

Opción interactiva:

```bash
ansible-inventory -i inventario.ini --graph --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --list-tags --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --check --diff --limit worker2 --ask-vault-pass
```

Opción con archivo local de password no versionado:

```bash
mkdir -p ~/.config/hpc-ansible
chmod 700 ~/.config/hpc-ansible
printf '%s\n' 'TU_PASSWORD_DE_VAULT' > ~/.config/hpc-ansible/vault-pass.txt
chmod 600 ~/.config/hpc-ansible/vault-pass.txt

ansible-playbook -i inventario.ini site.yml \
  --vault-password-file ~/.config/hpc-ansible/vault-pass.txt
```

## Reglas operativas recomendadas

- No dejar credenciales literales en `inventario.ini`, `group_vars/` ni `host_vars/`.
- Mantener en Vault solo secretos; no mezclar variables operativas comunes con datos sensibles.
- No versionar archivos como `.secrets/` o `~/.config/hpc-ansible/vault-pass.txt`.
- Antes de ejecutar sobre varios nodos, validar con `--syntax-check`, `--check --diff` y `--limit`.

## Migración mínima esperada en este repo

Si el repositorio se encuentra temporalmente con secretos en claro, la migración mínima esperada es:

1. Crear `group_vars/all/vault.yml` cifrado con las dos variables `vault_*`.
2. Reemplazar en `inventario.ini` el valor literal de `ansible_become_password` por `{{ vault_ansible_become_password_workers_u }}`.
3. Reemplazar en `group_vars/hpc_master.yml` el valor literal de `slurmdb_mysql_password` por `{{ vault_slurmdb_mysql_password }}`.
4. Ejecutar las validaciones básicas:

```bash
ansible-inventory -i inventario.ini --graph --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
```
