# Ansible Vault

## Estado actual

Vault no esta habilitado en este repositorio. Las credenciales residen en texto plano en:

- `inventario.ini`: `ansible_become_password` (grupo `workers_u`).
- `group_vars/hpc_master.yml`: `slurmdb_mysql_password`.

## Procedimiento para habilitar Vault

Si se decide cifrar los secretos del repositorio, seguir los pasos descritos a continuacion.

### Secretos que se recomienda migrar a Vault

Como minimo:

- `vault_ansible_become_password_workers_u`
- `vault_slurmdb_mysql_password`

El archivo cifrado destino seria:

- `group_vars/all/vault.yml`

### Puntos de consumo a actualizar

#### 1. `inventario.ini`

En el grupo `workers_u:vars`, reemplazar el valor literal por una referencia Vault:

```ini
[workers_u:vars]
ansible_become_password="{{ vault_ansible_become_password_workers_u }}"
```

#### 2. `group_vars/hpc_master.yml`

Reemplazar el valor literal de la contraseña de MariaDB:

```yaml
slurmdb_mysql_password: "{{ vault_slurmdb_mysql_password }}"
```

### Crear el archivo cifrado

Crear un archivo temporal en claro con los secretos:

```yaml
vault_ansible_become_password_workers_u: "CAMBIAR_ESTE_VALOR"
vault_slurmdb_mysql_password: "CAMBIAR_ESTE_VALOR"
```

Cifrarlo y moverlo a la ruta definitiva:

```bash
cat > /tmp/vault.yml <<'EOF'
vault_ansible_become_password_workers_u: "CAMBIAR_ESTE_VALOR"
vault_slurmdb_mysql_password: "CAMBIAR_ESTE_VALOR"
EOF

ansible-vault encrypt /tmp/vault.yml
mv /tmp/vault.yml group_vars/all/vault.yml
```

### Edicion posterior de secretos

```bash
ansible-vault edit group_vars/all/vault.yml
```

### Ejecucion habitual con Vault

Opcion interactiva:

```bash
ansible-inventory -i inventario.ini --graph --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --list-tags --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --check --diff --limit worker2 --ask-vault-pass
```

Opcion con archivo local de password no versionado:

```bash
mkdir -p ~/.config/hpc-ansible
chmod 700 ~/.config/hpc-ansible
printf '%s\n' 'TU_PASSWORD_DE_VAULT' > ~/.config/hpc-ansible/vault-pass.txt
chmod 600 ~/.config/hpc-ansible/vault-pass.txt

ansible-playbook -i inventario.ini site.yml \
  --vault-password-file ~/.config/hpc-ansible/vault-pass.txt
```

## Reglas operativas recomendadas

- No versionar archivos como `.secrets/` o `~/.config/hpc-ansible/vault-pass.txt`.
- Mantener en Vault solo secretos; no mezclar variables operativas comunes con datos sensibles.
- Antes de ejecutar sobre varios nodos, validar con `--syntax-check`, `--check --diff` y `--limit`.

## Pasos de migracion resumidos

1. Crear `group_vars/all/vault.yml` cifrado con las dos variables `vault_*`.
2. Reemplazar en `inventario.ini` el valor literal de `ansible_become_password` por `{{ vault_ansible_become_password_workers_u }}`.
3. Reemplazar en `group_vars/hpc_master.yml` el valor literal de `slurmdb_mysql_password` por `{{ vault_slurmdb_mysql_password }}`.
4. Ejecutar las validaciones basicas:

```bash
ansible-inventory -i inventario.ini --graph --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
```
