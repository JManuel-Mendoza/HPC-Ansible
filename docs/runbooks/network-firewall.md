# Runbook: Network + Firewall (HIGH-RISK)

Este runbook es para diagnóstico operativo. No aplica cambios.

Vars relevantes (ver `docs/audit/vars-map.md`):
- Red interna declarativa (NetworkManager): `network_internal_*` en `group_vars/all/vars.yml`
- Ruteo: `hpc_internal_supernet`, `hpc_internal_subnets`, `hpc_router_internal_ifaces`
- Firewall Slurm: `slurm_firewalld_zone`, `slurm_internal_cidr`, `slurmctld_port`, `slurmd_port`

## Checklist rápida (interfaces/rutas)

```bash
ip a
ip r
```

Conexiones internas `nmcli` (el rol crea conexiones `int-*`):
```bash
nmcli con show
nmcli -t -f NAME,DEVICE,TYPE,STATE con show --active | grep -E '^int-' || true
```

Si el nodo enruta (master):
```bash
sysctl net.ipv4.ip_forward
```

## Checklist rápida (firewalld)

```bash
systemctl status firewalld --no-pager
firewall-cmd --state
firewall-cmd --list-all
firewall-cmd --list-rich-rules
```

Verificar reglas Slurm (ejecuta en master y en compute):
- Debe haber rich rules que permitan desde `slurm_internal_cidr` hacia:
  - `slurmctld_port` (6817) en master
  - `slurmd_port` (6818) en compute

Comando útil:
```bash
firewall-cmd --list-rich-rules | grep -E '6817|6818|192\\.168\\.' || true
```

## Problemas comunes

### 1) Un worker no llega al master (SSH/Slurm)

1. DNS/hosts:
```bash
getent hosts master || true
grep -n \"Red interna HPC\" /etc/hosts || true
```
2. Rutas:
```bash
ip r
```
3. Firewall:
```bash
firewall-cmd --state
firewall-cmd --list-rich-rules
```

Evidencia para escalar:
- `ip a` + `ip r`
- `nmcli ... --active` (líneas `int-*`)
- `firewall-cmd --list-rich-rules`

### 2) Slurm no conecta (puertos)

En master:
```bash
ss -lntp | egrep ':(6817|6819)\\b' || true
```

En compute:
```bash
ss -lntp | egrep ':(6818)\\b' || true
```

Si el puerto escucha pero no conecta: revisar rich rules y el CIDR interno (`slurm_internal_cidr`).
