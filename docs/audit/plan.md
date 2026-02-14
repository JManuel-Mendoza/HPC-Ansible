# plan.md

Fecha de auditoría: **12 de febrero de 2026**  
Modo: **solo auditoría y planificación** (sin cambios en archivos)

## 1) Evidencia verificable
- Inventario de archivos: `find . -path './.git' -prune -o -type f -print | sort`
- Entrypoints y orden operativo: `docs/audit/ansible-entrypoints.md:1`
- Ledger archivo-por-archivo: `docs/audit/file-ledger.md:5`
- Matriz de tasks: `docs/audit/task-matrix.md:1`
- Hallazgos accionables: `docs/audit/findings.md:1`
- `ansible-inventory -i inventario.ini --graph`: grupos detectados (`hpc_master`, `workers`, `slurm_compute`, etc.)
- `ansible-playbook -i inventario.ini site.yml --syntax-check`: válido con warnings de permisos del entorno sandbox
- `ansible-playbook -i inventario.ini site.yml --list-tasks`: OK (15 plays)

## 2) Plan de paquetes (máximo 10)

| Paquete | Objetivo | Archivos/roles afectados | Riesgo | Pruebas/validaciones sugeridas | Criterio de aceptación |
|---|---|---|---|---|---|
| P1: Baseline y entrypoints | Consolidar ejecución segura de `site.yml` y orden operativo por tags | `site.yml`, `ansible.cfg`, `docs/audit/ansible-entrypoints.md` | MEDIUM | `--syntax-check`, `--list-tasks`, `ansible-inventory --graph` | Orden de ejecución documentado y reproducible; sintaxis válida en entorno objetivo |
| P2: Secretos y datos sensibles | Eliminar credenciales en claro y preparar Vault | `inventario.ini`, `group_vars/hpc_master.yml` | HIGH | `ansible-vault view/edit`, `--check --diff` con `--limit` | Sin secretos en texto plano en repo; despliegue funcional con vars cifradas |
| P3: Red interna (network) | Hacer cambios de NM más predecibles e idempotentes | `group_vars/all/vars.yml`, `roles/network_internal/defaults/main.yml`, `roles/network_internal/tasks/main.yml`, `roles/network_internal/tasks/master_link.yml` | HIGH | `--list-tasks --tags network`, `--check --diff --limit worker1`, pruebas de conectividad | No pérdida de conectividad; segunda ejecución sin cambios inesperados |
| P4: Ruteo (routing) | Controlar rutas persistentes por nodo y rollback claro | `roles/cluster_routing/tasks/main.yml` | HIGH | `--tags routing --limit worker1`, `ip route`, validación inter-subred | Rutas correctas en workers; rollback probado |
| P5: Firewall | Reducir ruido y centralizar recargas/reinicios en handlers | `roles/firewall/tasks/main.yml`, `roles/slurm_install/tasks/main.yml`, `roles/nfs_hpc/tasks/main.yml` | HIGH | `--tags firewall,slurm_firewall,nfs_firewall --check --diff`, `firewall-cmd --list-all` | Reglas esperadas aplicadas una sola vez y recargas controladas |
| P6: NVIDIA/CUDA | Separar detección/diagnóstico de cambios kernel/driver; minimizar shell | `roles/nvidia_cuda/tasks/main.yml`, `roles/nvidia_cuda/handlers/main.yml` | HIGH | `--tags cuda --limit <1 nodo GPU>`, `nvidia-smi`, reboot controlado | Nodo GPU estable, driver correcto, reboot solo cuando corresponde |
| P7: NFS | Endurecer idempotencia en export/firewall y mantener rollback | `roles/nfs_hpc/tasks/main.yml`, `roles/nfs_hpc/handlers/main.yml`, `roles/nfs_hpc/templates/exports.j2` | HIGH | `--tags nfs --check --diff`, `exportfs -v`, montaje desde worker | Exportaciones consistentes y montajes operativos tras re-ejecución |
| P8: Slurm control plane + DB | Encapsular cambios `slurmdbd/slurmctld` con handlers y validación | `roles/mariadb_server/*`, `roles/slurm_db_prep/*`, `roles/slurm_controller/*`, `roles/slurm_install/*`, `group_vars/hpc_master.yml` | HIGH | `--tags slurm,slurmdbd,slurmctld --limit hpc_master`, `scontrol`, `sacctmgr` | Controller y accounting sanos; reinicios solo por notify |
| P9: Munge + identidades | Blindar autenticación entre nodos y procedimientos de rollback | `roles/munge/*`, `roles/slurm_identities/*` | HIGH | `--tags munge,identities --limit slurm_all`, prueba `munge -n \| unmunge` | Autenticación munge consistente en master/workers |
| P10: Validación y LLM | Separar validación rápida/profunda y reducir debug ruidoso | `roles/validate/*`, `roles/slurm_validate/*`, `roles/llm_env/*` | MEDIUM | `--tags validate,slurm_validate,llm --check`, smoke jobs CPU/GPU | Validaciones reproducibles, salida útil, sin ruido operativo |

### Orden priorizado de ejecución (target)
1. clean OS (fuera de repo)
2. baseline (`common,ssh`)
3. red (`network`, `routing`)
4. firewall (`firewall`)
5. gpu (`cuda`)
6. nfs (`nfs`)
7. slurm (`slurm`, `munge`, `identities`, `slurm_install`, `slurm_config`)
8. llm (`llm`)
9. validate (`validate`, `slurm_validate`)

## 3) Lista priorizada de cambios (backlog)
1. Vault para `inventario.ini` y `group_vars/hpc_master.yml`.
2. Paquete dedicado de red/routing con rollback por host.
3. Mover reinicios directos de Slurm a handlers.
4. Reducir `shell` en provisioning (network/nvidia/slurm_install).
5. Controlar `ignore_errors` en instalación de headers NVIDIA.
6. Encapsular cambios de kernel/reboot NVIDIA por nodos y lotes.
7. Normalizar recargas de firewall como handlers.
8. Etiquetar (`TAG`) tareas debug para no ensuciar salida productiva.
9. Separar validación Slurm rápida vs smoke profunda.
10. Revisar y archivar `roles/slurm_install/files/slurm.conf` (no activo).
11. Asegurar idempotencia en tasks `command` sin guardas.
12. Establecer política de `--limit` obligatoria en zonas HIGH.
13. Añadir evidencia mínima estandarizada por paquete (`syntax-check`, `list-tasks`, `check`).
14. Revisar `host_key_checking=False` según entorno.
15. Limpiar artifacts no útiles (`.DS_Store`, zips históricos).
16. Formalizar rollback runbook de firewall.
17. Formalizar rollback runbook de NFS.
18. Formalizar rollback runbook de SlurmDB.
19. Formalizar rollback runbook de Munge.
20. Mantener `site.yml --syntax-check` y `--list-tasks` como puerta de calidad mínima.

## 4) Inventario archivo-por-archivo (KEEP/MOVE/ARCHIVE/DELETE)

Resumen actual (desde `docs/audit/file-ledger.md:5`):
- `KEEP`: 94
- `ARCHIVE`: 61
- `DELETE`: 3
- `MOVE`: 0

Inventario completo verificable: `docs/audit/file-ledger.md:7` a `docs/audit/file-ledger.md:164`.

Decisiones críticas:
- `DELETE`: `.DS_Store` y artefactos binarios/históricos no necesarios para operación.
- `ARCHIVE`: documentación histórica consolidada en `docs/docs_old/**` + `roles/slurm_install/files/slurm.conf`
- `KEEP`: entrypoint (`site.yml`), roles activos bajo `roles/**`, vars de inventario, docs activas y herramientas de auditoría

## 5) Tasks marcadas REWORK (o equivalente), agrupadas por rol, con propuesta

### `roles/firewall`
- `roles/firewall/tasks/main.yml:60` — `Firewall | Slurm | Show rich rules (debug)`  
  Propuesta: `TAG`  
  Justificación: salida diagnóstica; conviene ejecutarla solo bajo tag de depuración.

### `roles/network_internal`
- `roles/network_internal/tasks/main.yml:14` — obtener conexiones NM  
  Propuesta: `REWORK`  
  Justificación: `shell`; migrable a consulta más robusta/parseable.
- `roles/network_internal/tasks/main.yml:43` — mostrar conexiones a borrar  
  Propuesta: `TAG`  
  Justificación: debug operativo.
- `roles/network_internal/tasks/main.yml:47` — borrar conexiones no permitidas  
  Propuesta: `REWORK`  
  Justificación: `command` sensible, requiere guardas y rollback explícito.
- `roles/network_internal/tasks/main.yml:74` — crear conexión int-master  
  Propuesta: `REWORK`  
  Justificación: operación de red crítica, idempotencia mejorable.
- `roles/network_internal/tasks/main.yml:106` — ajustar int-master  
  Propuesta: `REWORK`
- `roles/network_internal/tasks/main.yml:159` — mostrar estado conexiones  
  Propuesta: `TAG`
- `roles/network_internal/tasks/master_link.yml:6` — crear int-{{ link_item.key }}  
  Propuesta: `REWORK`
- `roles/network_internal/tasks/master_link.yml:38` — ajustar int-{{ link_item.key }}  
  Propuesta: `REWORK`

### `roles/cluster_routing`
- `roles/cluster_routing/tasks/main.yml:134` — añadir rutas persistentes  
  Propuesta: `REWORK`  
  Justificación: alta criticidad; requiere idempotencia + rollback.
- `roles/cluster_routing/tasks/main.yml:148` — activar conexión  
  Propuesta: `REWORK`  
  Justificación: acoplar a cambio real y ejecutar en modo controlado.

### `roles/nfs_hpc`
- `roles/nfs_hpc/tasks/main.yml:84` — abrir 2049/tcp en firewalld  
  Propuesta: `REWORK`  
  Justificación: mejor con módulo idempotente y notify.
- `roles/nfs_hpc/handlers/main.yml:2` — recargar exports  
  Propuesta: `KEEP`  
  Justificación: handler correcto por naturaleza; mantener.
- `roles/nfs_hpc/handlers/main.yml:5` — recargar firewalld  
  Propuesta: `KEEP`

### `roles/nvidia_cuda`
- `roles/nvidia_cuda/tasks/main.yml:41` — informar sin GPU  
  Propuesta: `TAG`
- `roles/nvidia_cuda/tasks/main.yml:144` — resetear stream  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:152` — cambiar stream fijado  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:167` — instalar headers/devel (RHEL best effort)  
  Propuesta: `SPLIT`  
  Justificación: separar detección, instalación y manejo de error.
- `roles/nvidia_cuda/tasks/main.yml:215` — instalar headers (Ubuntu best effort)  
  Propuesta: `SPLIT`
- `roles/nvidia_cuda/tasks/main.yml:242` — detectar paquetes 590 (RHEL)  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:257` — detectar módulos abiertos (Ubuntu)  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:275` — detectar paquetes 590 (Ubuntu)  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:343` — agregar args kernel nouveau  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:394` — actualizar GRUB (Ubuntu)  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:426` — marcar reinicio requerido  
  Propuesta: `REWORK`  
  Justificación: sustituible por marca idempotente (archivo/fact) + handler.
- `roles/nvidia_cuda/tasks/main.yml:431` — verificar ausencia paquetes 590 (RHEL)  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:437` — forzar stream 580-dkms  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:445` — cambiar a 580-dkms  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:453` — rebuild initramfs tras ajuste  
  Propuesta: `MOVE-TO-HANDLER`
- `roles/nvidia_cuda/tasks/main.yml:471` — programar reinicio tras ajuste  
  Propuesta: `MOVE-TO-HANDLER`
- `roles/nvidia_cuda/tasks/main.yml:480` — verificar ausencia paquetes 590 (Ubuntu)  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:495` — validar módulos cargados  
  Propuesta: `REWORK`
- `roles/nvidia_cuda/tasks/main.yml:680` — capturar paquetes cuando falla nvidia-smi  
  Propuesta: `TAG`
- `roles/nvidia_cuda/tasks/main.yml:689` — capturar paquetes cuando falla nvidia-smi (Ubuntu)  
  Propuesta: `TAG`
- `roles/nvidia_cuda/tasks/main.yml:736` — resumen final  
  Propuesta: `TAG`
- `roles/nvidia_cuda/tasks/main.yml:746` — resumen final (Ubuntu)  
  Propuesta: `TAG`
- `roles/nvidia_cuda/handlers/main.yml:2` — Rebuild initramfs (RHEL)  
  Propuesta: `KEEP`
- `roles/nvidia_cuda/handlers/main.yml:8` — Rebuild initramfs (Ubuntu)  
  Propuesta: `KEEP`

### `roles/llm_env`
- `roles/llm_env/tasks/main.yml:113` — install/update conda packages  
  Propuesta: `REWORK`
- `roles/llm_env/tasks/main.yml:124` — instalar stack PyTorch CUDA  
  Propuesta: `REWORK`
- `roles/llm_env/tasks/main.yml:152` — instalar pip packages  
  Propuesta: `REWORK`

### `roles/validate`
- `roles/validate/tasks/main.yml:7` — print uname  
  Propuesta: `TAG`
- `roles/validate/tasks/main.yml:11` — check sshd -T  
  Propuesta: `REWORK`
- `roles/validate/tasks/main.yml:20` — print sshd relevantes  
  Propuesta: `TAG`
- `roles/validate/tasks/main.yml:30` — print nvidia-smi  
  Propuesta: `TAG`
- `roles/validate/tasks/main.yml:52` — print torch check  
  Propuesta: `TAG`
- `roles/validate/tasks/slurm.yml:8` — master escucha 6817/6819  
  Propuesta: `REWORK`
- `roles/validate/tasks/slurm.yml:20` — workers escuchan 6818  
  Propuesta: `REWORK`

### `roles/munge`
- `roles/munge/tasks/main.yml:115` — verify munge local STATUS  
  Propuesta: `REWORK`

### `roles/slurm_facts`
- `roles/slurm_facts/tasks/main.yml:91` — advertir mezcla de modelos  
  Propuesta: `KEEP`  
  Justificación: warning útil, sin cambio de estado.

### `roles/slurm_install`
- `roles/slurm_install/tasks/main.yml:2` — see locally built RPMs  
  Propuesta: `TAG`
- `roles/slurm_install/tasks/main.yml:199` — add SrunPortRange firewall  
  Propuesta: `REWORK`
- `roles/slurm_install/tasks/main.yml:207` — reload firewalld  
  Propuesta: `MOVE-TO-HANDLER`
- `roles/slurm_install/tasks/main.yml:305` — advertir mezcla de modelos fallback  
  Propuesta: `TAG`

### `roles/slurm_controller`
- `roles/slurm_controller/tasks/main.yml:51` — restart slurmdbd  
  Propuesta: `MOVE-TO-HANDLER`
- `roles/slurm_controller/tasks/main.yml:65` — restart slurmctld  
  Propuesta: `MOVE-TO-HANDLER`
- `roles/slurm_controller/tasks/main.yml:121` — reanudar nodos GRES corregido  
  Propuesta: `TAG`  
  Justificación: acción operacional sensible; mejor bajo tag explícito.

### `roles/slurm_compute`
- `roles/slurm_compute/tasks/main.yml:15` — skip slurmd management (debug)  
  Propuesta: `TAG`
- `roles/slurm_compute/tasks/main.yml:61` — restart slurmd  
  Propuesta: `MOVE-TO-HANDLER`

### `roles/slurm_validate`
- `roles/slurm_validate/tasks/main.yml:11` — listar particiones  
  Propuesta: `REWORK`
- `roles/slurm_validate/tasks/main.yml:42` — asegurar no DOWN/DRAIN/FAIL  
  Propuesta: `REWORK`
- `roles/slurm_validate/tasks/main.yml:88` — mostrar sonda Torch  
  Propuesta: `TAG`
- `roles/slurm_validate/tasks/main.yml:121` — mostrar smoke Torch CUDA  
  Propuesta: `TAG`
- `roles/slurm_validate/tasks/main.yml:152` — esperar cola job CPU  
  Propuesta: `REWORK`
- `roles/slurm_validate/tasks/main.yml:166` — verificar sacct job CPU  
  Propuesta: `REWORK`
- `roles/slurm_validate/tasks/main.yml:236` — mostrar salida job CPU  
  Propuesta: `TAG`
- `roles/slurm_validate/tasks/main.yml:264` — esperar cola job GPU  
  Propuesta: `REWORK`
- `roles/slurm_validate/tasks/main.yml:278` — verificar sacct job GPU  
  Propuesta: `REWORK`
- `roles/slurm_validate/tasks/main.yml:348` — mostrar salida job GPU  
  Propuesta: `TAG`

## 6) Zonas HIGH y paquete dedicado con rollback

| Zona HIGH | Paquete dedicado | Rollback mínimo propuesto |
|---|---|---|
| network | P3 | Snapshot previo de `nmcli con show`, `ip a`, `ip route`; rollback aplicando conexiones previas y levantando perfil anterior por host |
| routing | P4 | Backup de rutas actuales por nodo; rollback quitando rutas agregadas y reactivando conexión original |
| nvidia | P6 | Snapshot de paquetes/stream/kernel args; rollback a stream/driver previo + regenerar initramfs + reboot controlado por nodo |
| firewall | P5 | Backup `firewall-cmd --list-all` (runtime/permanent); rollback eliminando reglas nuevas y `--reload` |
| nfs | P7 | Backup `/etc/exports` y estado de mounts; rollback restaurando exports previos y recargando servicios |
| slurmdb/slurmctld | P8 | Backup config + dump DB; rollback restaurando `slurmdbd.conf`/DB y reinicio ordenado de servicios |
| munge | P9 | Backup clave/permisos; rollback restaurando clave y reiniciando `munge` en orden master->workers |

---

Estado final de esta entrega: **solo planificación/auditoría; no se modificó ningún archivo**.
