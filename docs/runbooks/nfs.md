# Runbook: NFS (share HPC)

Este repo configura NFS con el rol `roles/nfs_hpc`.

Vars relevantes (ver `roles/nfs_hpc/defaults/main.yml`):
- Export (server): `nfs_export_path` (este repo: `/srv/nfs/llm` en `group_vars/all/vars.yml`)
- Mountpoint (clients): `nfs_client_mountpoint` (este repo: `/mnt/llm` en `group_vars/all/vars.yml`)
- Server IP: `nfs_server_ip` (deriva de `ansible_host` del `hpc_master` en `inventario.ini`; fallback por facts)
- Compat rol: `nfs_hpc_share_dir` (export), `nfs_hpc_mount_point` (mountpoint) y `nfs_hpc_server_host` (server addr)
- Export file: `nfs_hpc_export_file` (default: `/etc/exports.d/hpc-nfs.exports`)
- Clientes permitidos: `nfs_hpc_allowed_clients` (default: `{{ slurm_internal_cidr }}`)
- Servicio server:
  - RHEL/Rocky: `nfs-server`
  - Debian/Ubuntu: `nfs-kernel-server`

## Checklist rápida (server)

1) Servicio:
```bash
systemctl status nfs-server --no-pager || true
systemctl status nfs-kernel-server --no-pager || true
journalctl -u nfs-server -n 200 --no-pager || true
journalctl -u nfs-kernel-server -n 200 --no-pager || true
```

2) Exports:
```bash
exportfs -v
ls -l /etc/exports.d || true
cat /etc/exports.d/hpc-nfs.exports || true
```

3) Firewall (si `firewalld` está activo, el rol abre 2049/tcp):
```bash
systemctl is-active firewalld || true
firewall-cmd --permanent --query-port=2049/tcp || true
firewall-cmd --list-ports || true
```

## Checklist rápida (cliente)

1) ¿Está montado?
```bash
mount | grep -E ' nfs' || true
df -hT | grep -E ' nfs|/mnt/llm' || true
mountpoint -q /mnt/llm; echo $?
```

2) ¿Se puede leer/escribir? (según permisos del share)
```bash
ls -la /mnt/llm | head
```

## Problemas comunes

### 1) El cliente no monta / timeouts

1. Verifica conectividad al server:
```bash
ping -c 1 <server> || true
```
2. En server, verifica firewall y servicio:
```bash
systemctl status nfs-server --no-pager || true
firewall-cmd --permanent --query-port=2049/tcp || true
```
3. En cliente, evidencia del sistema:
```bash
journalctl -n 200 --no-pager | grep -Ei 'nfs|mount' || true
```

Evidencia para escalar:
- `exportfs -v` (server)
- `systemctl status nfs-...`
- logs del cliente (`journalctl ... | grep -Ei nfs`)

### 2) Export existe pero “permission denied”

1. Verifica export exacto:
```bash
exportfs -v
cat /etc/exports.d/hpc-nfs.exports
```
2. Verifica que el cliente esté dentro del rango permitido (`nfs_hpc_allowed_clients`, típicamente `slurm_internal_cidr`).
3. Verifica permisos del directorio del share:
```bash
ls -ld /srv/nfs/llm
```

## Remoción segura (tag `del_nfs`)

El rol `roles/nfs_hpc` incluye tareas de remoción bajo el tag `del_nfs`:
- En server (master): quita el archivo de exports del repo y cierra 2049/tcp si `firewalld` está activo.
- En clientes: desmonta `/mnt/llm`, limpia fstab y (si están vacíos) intenta borrar directorios de montaje legacy.

Ejemplos:
```bash
# Remover NFS solo en workers (recomendado primero)
ansible-playbook -i inventario.ini site.yml --tags del_nfs --limit workers

# Remover export NFS del master (no borra /srv/nfs/llm ni su contenido)
ansible-playbook -i inventario.ini site.yml --tags del_nfs --limit hpc_master
```
