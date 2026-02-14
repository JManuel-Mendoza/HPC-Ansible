# SLURM – Bitácora de problemas y soluciones (hasta 2026-01-21)

Contexto
- Cluster: master, worker1, worker2 (Rocky Linux 9.x), worker3, worker4 (Ubuntu 22.04)
- Objetivo: instalar/configurar MUNGE + SLURM (+ slurmdbd/mariadb)
- Restricción relevante: nombres/hosts y redes múltiples (interfaces internas /28) + presencia de Tailscale en master.

---

## Estado actual (checkpoint al final de esta bitácora)

- master:
  - munge: active
  - slurmctld: active
  - slurmdbd: active
  - slurmd: inactive (esperado si master solo es controller)
- worker1/worker2 (Rocky):
  - munge: active
  - slurmd: active
  - Estado en SLURM: `IDLE` tras forzar RESUME
- worker3/worker4 (Ubuntu):
  - munge: active
  - slurmd/slurm packages: NO instalados (NO_SLURM_PKGS)
  - hostname actual reportado: `sistemas-Precision-3440` (NO coincide con inventario `worker3/worker4`, pendiente)

Observación importante:
- `slurm.conf` todavía tiene NodeName con valores default (CPUs=1, RealMemory=1024). Se creó `roles/slurm_install/tasks/facts.yml` para corregir esto usando `slurmd -C`, pero aún falta integrarlo al flujo de render del template.

---

## Incidencias y soluciones

### 1) MUNGE no inicia en Rocky: permisos en /run/munge
**Síntoma**
- `munge.service` falla al iniciar.
- `journalctl -xeu munge` muestra:
  - `Socket is inaccessible: execute permissions for all required on "/run/munge"`

**Causa raíz**
- Directorio `/run/munge` sin permisos de ejecución adecuados para atravesar el path (bit x).

**Solución aplicada**
- Asegurar propietarios/permisos correctos en paths de MUNGE:
  - `chown -R munge: /etc/munge/ /var/log/munge/ /var/lib/munge/ /run/munge/`
  - `chmod 0700 /etc/munge/ /var/log/munge/ /var/lib/munge/ /run/munge/`
  - Validar `chmod 600 /etc/munge/munge.key`
- Tras esto, `systemctl start munge` queda `active` y la prueba:
  - `munge -n | unmunge | grep STATUS` devuelve `Success (0)` en todos los nodos.

**Verificación**
- `systemctl is-active munge` → `active` en todos los nodos
- `munge -n | unmunge | grep STATUS` → `Success (0)`


### 2) slurmctld no arranca: nodos inválidos / parse error en slurm.conf
**Síntoma**
- `slurmctld` falla con:
  - `Invalid node names in partition debug`
- Luego aparece:
  - `Parse error in file /etc/slurm/slurm.conf line 187: "PartitionName=gpu ..."`

**Causa raíz**
- El template estaba generando **dos particiones en la misma línea** (concatenación):
  - `PartitionName=debug ... PartitionName=gpu ...`
- Además había indentación/whitespace que rompía el parseo.

**Solución aplicada**
- Corregir el template para que emita **una partición por línea**, sin espacios residuales.
- Resultado: `scontrol ping` pasó a `Slurmctld(primary) at master is UP`.

**Verificación**
- `systemctl status slurmctld` → `active`
- `scontrol ping` → `UP`
- `nl -ba /etc/slurm/slurm.conf | sed -n '170,200p'` confirma particiones en líneas separadas.


### 3) Workers en `UNKNOWN*` / `NOT_RESPONDING`: slurmd no registra contra el controller
**Síntoma**
- En master: `sinfo -lN` muestra nodos como `unknown*`
- `scontrol show node worker1`:
  - `State=UNKNOWN+NOT_RESPONDING`
  - `SlurmdStartTime=None` (en fase inicial)

**Causas raíz (múltiples)**
A) Resolución DNS errónea por Tailscale
- En worker1, `master` resolvía a:
  - `100.98.68.22 master.tail...` (Tailscale)
- `TCP(master:6817)` fallaba por ese camino.

B) Firewall bloqueando puertos SLURM
- En master, `firewalld` activo y sin puertos (zona public solo ssh/cockpit).
- En workers, `firewalld` activo y también bloqueaba.

C) Resolución de workers en master hacia IP “equivocada”
- En master, `worker1` resolvía a IP externa (ej. `10.195.20.52`) y fallaba el reach hacia `slurmd:6818`.

**Soluciones aplicadas**
A) Forzar resolución correcta con `/etc/hosts` (por subred /28)
- worker1:
  - `/etc/hosts`: `192.168.34.1 master`
- worker2:
  - `/etc/hosts`: `192.168.34.17 master`
(Esto es necesario porque cada worker está en una /28 distinta y el master tiene una IP distinta en cada /28.)

B) Abrir puertos mínimos SLURM con firewalld (restringido a red interna)
- En master: permitir `6817/tcp` desde `192.168.34.0/24`
- En worker1/worker2: permitir `6818/tcp` desde `192.168.34.0/24`

C) Forzar resolución correcta de workers en el master
- En master `/etc/hosts`:
  - `192.168.34.2 worker1`
  - (y asegurar worker2 ya resolvía correcto: `192.168.34.18 worker2`)

**Verificaciones clave**
- Desde worker1/2:
  - `getent hosts master` apunta a IP interna correcta.
  - `</dev/tcp/master/6817` → OK
- Desde master:
  - `ss -ltnp | egrep ":(6817|6819)\b"` muestra escucha en `0.0.0.0:6817` y `0.0.0.0:6819`
  - `</dev/tcp/worker{1,2}/6818` → OK
- `journalctl -u slurmd` deja de mostrar:
  - `Unable to contact slurm controller (connect failure)`
  - `Unable to resolve "master"`


### 4) Nodos quedan `DOWN*` tras incidentes: recuperación con RESUME
**Síntoma**
- `sinfo -lN` muestra `down* Not responding` o `Reason=Node unexpectedly rebooted`.

**Causa**
- Registro inconsistente durante las fases de DNS/firewall; y/o reinicios de slurmd.

**Solución aplicada**
- Forzar recuperación desde master:
  - `scontrol update NodeName=worker1 State=RESUME`
  - `scontrol update NodeName=worker2 State=RESUME`

**Verificación**
- `sinfo -lN` pasa a `idle*` para worker1 y worker2.


### 5) slurm.conf reporta CPUs/Mem incorrectos (CPUs=1, RealMemory=1024)
**Síntoma**
- En master `/etc/slurm/slurm.conf`:
  - `NodeName=worker1 CPUs=1 RealMemory=1024`
- En cambio, en worker1/2:
  - `slurmd -C` reporta:
    - `CPUs=20 ... CoresPerSocket=10 ThreadsPerCore=2 RealMemory=63739`

**Causa raíz**
- El template estaba usando defaults porque **no existían variables `slurm_*` en hostvars**.
- `ansible -m debug ... | grep slurm_*` no mostraba variables.

**Solución parcial aplicada (pendiente de integrar)**
- Se creó `roles/slurm_install/tasks/facts.yml` para:
  - Ejecutar `slurmd -C`
  - Parsear `CPUs` y `RealMemory`
  - Guardar `slurm_cpus` y `slurm_real_memory` vía `set_fact`
- Falta: importar `facts.yml` antes de renderizar `slurm.conf` y actualizar el template para usar esas variables.

**Verificación**
- `slurmd -C` en worker1/2 devuelve valores correctos (20 CPUs, 63739 MB RAM aprox).
- `slurm.conf` todavía no refleja esos valores → pendiente.

---

## Pendientes / siguientes pasos sugeridos

1) Integrar `facts.yml` al rol `slurm_install` (antes del template de slurm.conf)
2) Regenerar `slurm.conf` y reiniciar servicios (controlado):
   - `slurmctld` en master
   - `slurmd` en worker1/2
3) Incorporar worker3/4 (Ubuntu):
   - Decidir: cambiar hostname a `worker3/worker4` o reflejar hostname real en slurm.conf.
   - Instalar Slurm en Ubuntu (paquetes o build equivalente) y abrir puertos (6818).
4) Normalizar resolución (evitar depender de Tailscale para nombres críticos):
   - Mantener `/etc/hosts` o crear DNS interno consistente.
   - Ideal: definir explícitamente `SlurmctldHost=master(<IP-interno>)` por nodo o por entorno si aplica.

---
