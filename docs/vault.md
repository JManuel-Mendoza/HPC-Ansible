# Gestión de secretos con Ansible Vault

Este repositorio usa `group_vars/all/vault.yml` para secretos cifrados con `ansible-vault`.

## Variables sensibles migradas

- `vault_ansible_become_password_workers_u`
- `vault_slurmdb_mysql_password`

Las variables funcionales siguen en sus archivos originales:

- `inventario.ini`: `ansible_become_password` referencia `vault_ansible_become_password_workers_u`.
- `group_vars/hpc_master.yml`: `slurmdb_mysql_password` referencia `vault_slurmdb_mysql_password`.

## Crear o recrear el vault

1. Crear archivo con valores en claro (temporal):

```bash
cat > /tmp/vault.yml <<'EOF'
vault_ansible_become_password_workers_u: "CAMBIAR_ESTE_VALOR"
vault_slurmdb_mysql_password: "CAMBIAR_ESTE_VALOR"
EOF
```

2. Cifrarlo en la ruta del repo:

```bash
ANSIBLE_LOCAL_TEMP=/tmp ansible-vault encrypt /tmp/vault.yml
mv /tmp/vault.yml group_vars/all/vault.yml
```

## Editar secretos

```bash
ANSIBLE_LOCAL_TEMP=/tmp ansible-vault edit group_vars/all/vault.yml
```

## Ejecución de playbooks con Vault

Opción interactiva:

```bash
ansible-playbook -i inventario.ini site.yml --ask-vault-pass
```

Opción con archivo local de password (fuera del repo):

```bash
mkdir -p ~/.config/hpc-ansible
chmod 700 ~/.config/hpc-ansible
printf '%s\n' 'TU_PASSWORD_DE_VAULT' > ~/.config/hpc-ansible/vault-pass.txt
chmod 600 ~/.config/hpc-ansible/vault-pass.txt
ansible-playbook -i inventario.ini site.yml --vault-password-file ~/.config/hpc-ansible/vault-pass.txt
```

## Validaciones rápidas

```bash
ansible-inventory -i inventario.ini --graph --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --syntax-check --ask-vault-pass
```
