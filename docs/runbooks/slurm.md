# Runbook: Slurm (controller/compute/accounting)

Este repositorio gestiona Slurm con servicios:
- `slurmctld` (controller, en `hpc_master`)
- `slurmd` (compute, en `slurm_compute`)
- `slurmdbd` (accounting, en `hpc_master`) + `mariadb` (DB)

Rutas/vars relevantes (ver `docs/audit/vars-map.md`):
- Configs: `slurm_etc_dir` (default: `/etc/slurm`)
- Logs: `slurm_log_dir` (default: `/var/log/slurm`)
- Controller host: `slurm_control_machine` (default: `master`)
- Puertos: `slurmctld_port=6817`, `slurmd_port=6818`, `slurmdbd_port=6819`
- DB users: `slurmdb_mysql_user` (string o lista; `slurmdbd_storage_user` usa el primer usuario efectivo)

Nota: los comandos usan los defaults (`/etc/slurm`, `/var/log/slurm`, `master`). Si el laboratorio los sobrescribio en `group_vars/*`, se recomienda ajustar esos literales.

## Checklist rápida (5 min)

En master (`hpc_master`):
```bash
systemctl status slurmctld slurmdbd mariadb --no-pager
journalctl -u slurmctld -n 200 --no-pager
journalctl -u slurmdbd -n 200 --no-pager
journalctl -u mariadb -n 200 --no-pager

scontrol ping
sinfo -lN
squeue
```

En un compute (`slurm_compute`):
```bash
systemctl status slurmd --no-pager
journalctl -u slurmd -n 200 --no-pager
```

Puertos (útil para “no conecta”):
```bash
ss -lntp | egrep ':(6817|6818|6819)\\b' || true
```

## Reconfiguración segura (sin reiniciar servicios)

Usa `scontrol reconfigure` cuando:
- cambiaste `/etc/slurm/slurm.conf` o `/etc/slurm/gres.conf`, y
- `slurmctld` está activo, pero necesitas aplicar la config sin restart.

```bash
scontrol reconfigure
```

No uses `reconfigure` si el controller no levanta; primero corrige el motivo (logs/config/munge).

## Problemas comunes

### 1) `slurmctld` no levanta (master)

1. Ver estado y logs:
```bash
systemctl status slurmctld --no-pager
journalctl -u slurmctld -n 200 --no-pager
```
2. Verifica configs y permisos:
```bash
ls -la /etc/slurm
ls -l /etc/slurm/slurm.conf
```
3. Verifica Munge (debe estar OK para Slurm):
```bash
systemctl status munge --no-pager
munge -n | unmunge | grep STATUS
```
4. Verifica resolución del controller y /etc/hosts:
```bash
getent hosts master
grep -n \"Red interna HPC\" /etc/hosts || true
```

Evidencia para escalar:
- `journalctl -u slurmctld -n 200 --no-pager`
- `/etc/slurm/slurm.conf`
- `systemctl status slurmctld --no-pager`

### 2) Nodos `DOWN` / `DRAIN` (master)

1. Ver motivo:
```bash
sinfo -R
scontrol show node -o <NODE>
```
2. En el nodo afectado, revisar `slurmd`:
```bash
systemctl status slurmd --no-pager
journalctl -u slurmd -n 200 --no-pager
```
3. Verificar que el nodo tenga config y Munge:
```bash
ls -l /etc/slurm/slurm.conf
systemctl status munge --no-pager
munge -n | unmunge | grep STATUS
```

Evidencia para escalar:
- `scontrol show node -o <NODE>`
- `journalctl -u slurmd -n 200 --no-pager` (en el nodo)

### 3) Accounting no funciona (`slurmdbd`/MariaDB)

Síntomas típicos:
- `sacctmgr` falla
- `slurmdbd` no conecta a DB / credenciales incorrectas

1. Verifica servicios:
```bash
systemctl status slurmdbd mariadb --no-pager
journalctl -u slurmdbd -n 200 --no-pager
journalctl -u mariadb -n 200 --no-pager
```
2. Verifica el archivo de config de SlurmDBD:
```bash
ls -l /etc/slurm/slurmdbd.conf
sudo grep -nE \"Storage(User|Pass|Loc|Host)\" /etc/slurm/slurmdbd.conf || true
```
3. Prueba de `sacctmgr` (si está instalado/configurado):
```bash
sacctmgr -n show cluster || true
```

Acción si falla por credenciales:
- Verifica el valor literal de `slurmdb_mysql_password` en `group_vars/hpc_master.yml` y que coincida con la cuenta `slurm` en MariaDB.

Evidencia para escalar:
- `journalctl -u slurmdbd -n 200 --no-pager`
- `journalctl -u mariadb -n 200 --no-pager`
- (sanitizado) extracto de `StorageHost/StorageUser/StorageLoc` (no compartas secretos)
