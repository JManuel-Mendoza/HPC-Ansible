# HPC-Ansible

Automatización de un clúster HPC (master + workers) usando Ansible y roles.

## Estructura

- `site.yml`: playbook principal
- `roles/`: roles por capa (common, ssh, firewall, llm_env, validate)
- `group_vars/`: variables por grupo
- `inventario.ini`: inventario de nodos (ajustar según entorno)

## Requisitos

- Ansible Core 2.14.x
- Colecciones definidas en `requirements.yml`

## Instalación de colecciones

```bash
ansible-galaxy collection install -r requirements.yml
```
