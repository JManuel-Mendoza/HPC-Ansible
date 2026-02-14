# Runbook: NFS (share HPC)

Este repo configura NFS con el rol `roles/nfs_hpc`.

Vars relevantes (ver `roles/nfs_hpc/defaults/main.yml`):
- Share: `nfs_hpc_share_dir` (default: `/nfs-hpc`)
- Export file: `nfs_hpc_export_file` (default: `/etc/exports.d/hpc-nfs.exports`)
- Server host: `nfs_hpc_server_host` (default: `{{ slurm_control_machine }}` / `master`)
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
df -hT | grep -E ' nfs|/nfs-hpc' || true
mountpoint -q /nfs-hpc; echo $?
```

2) ¿Se puede leer/escribir? (según permisos del share)
```bash
ls -la /nfs-hpc | head
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
ls -ld /nfs-hpc
```
