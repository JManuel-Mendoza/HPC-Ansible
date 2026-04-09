# Runbook: Munge (autenticación Slurm)

Este repo instala/configura Munge con:
- Key en `/etc/munge/munge.key`
- Servicio `munge` (systemd)
- Host “fuente” de la key: `munge_key_host` (ver `group_vars/all/vars.yml`)

## Checklist rápida (3 min)

En cualquier nodo:
```bash
systemctl status munge --no-pager
journalctl -u munge -n 200 --no-pager
```

Permisos esperados (según rol `roles/munge/tasks/main.yml`):
- Directorios `0700` y owner/group `munge:munge`:
  - `/etc/munge`, `/var/log/munge`, `/var/lib/munge`
- Key `0600` y owner/group `munge:munge`:
  - `/etc/munge/munge.key`
- Runtime `/run/munge` con permisos `0711` (RHEL/Rocky)

Verificación rápida:
```bash
stat -c '%U %G %a %n' /etc/munge /etc/munge/munge.key /run/munge 2>/dev/null || true
```

Test local (el rol valida esto):
```bash
munge -n | unmunge | grep STATUS
```

Test entre nodos (desde A hacia B):
```bash
munge -n | ssh <otro_nodo> unmunge | grep STATUS
```

## Problemas comunes

### 1) “STATUS” no aparece / `unmunge` falla

1. Ver logs:
```bash
journalctl -u munge -n 200 --no-pager
```
2. Revisar permisos/ownership:
```bash
stat -c '%U %G %a %n' /etc/munge /etc/munge/munge.key
```
3. Verificar `/run/munge` (tmpfiles):
```bash
ls -ld /run/munge || true
ls -l /etc/tmpfiles.d/munge.conf || true
sudo systemd-tmpfiles --create /etc/tmpfiles.d/munge.conf
sudo systemctl restart munge
```

Evidencia para escalar:
- `journalctl -u munge -n 200 --no-pager`
- `stat` de rutas anteriores

### 2) Funciona local pero falla entre nodos

Causa típica: keys distintas (mismatch) o firewall/ruta/tiempo.

1. Verificar hash de la key (NO compartas el contenido de la key):
```bash
sudo sha256sum /etc/munge/munge.key
```
2. Comparar hash entre nodos: deben ser iguales.
3. Verificar que la hora no esté muy desfasada (si aplica):
```bash
timedatectl status
```

Evidencia para escalar:
- hashes `sha256sum` (solo el hash)
- `journalctl -u munge -n 200 --no-pager` en ambos nodos
