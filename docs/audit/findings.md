# Findings

Top 20 hallazgos accionables identificados en auditoria estatica.

## Top 20 accionables

1. [HIGH] Credenciales en texto plano en inventario
   Evidencia: `inventario.ini`: `ansible_become_password` expuesto en hosts `workers_u`.
   Accion: Mover a Ansible Vault y eliminar del inventario en claro.
2. [HIGH] Password de SlurmDB en texto plano
   Evidencia: `group_vars/hpc_master.yml`: `slurmdb_mysql_password` en claro.
   Accion: Vault + inyeccion segura por vars en runtime.
3. [HIGH] Superficie de cambio de red en vivo
   Evidencia: `roles/network_internal/tasks/main.yml` elimina conexiones NM no permitidas.
   Accion: Paquete de cambio dedicado con ventana y rollback probado.
4. [HIGH] Ruteo persistente con calculo dinamico
   Evidencia: `roles/cluster_routing/tasks/main.yml` calcula rutas y aplica `nmcli connection up`.
   Accion: Pruebas por nodo con `--limit` y validacion de conectividad.
5. [HIGH] Cambio de kernel/boot params NVIDIA
   Evidencia: `roles/nvidia_cuda/tasks/main.yml` toca blacklist `nouveau` + grub/initramfs + reboot.
   Accion: Gate de aprobacion y lote gradual por nodo GPU.
6. [HIGH] Reinicios directos fuera de handlers
   Evidencia: `roles/slurm_controller/tasks/main.yml` y `roles/slurm_compute/tasks/main.yml` reinician servicios por task directa.
   Accion: Mover reinicios a handlers cuando sea viable.
7. [MEDIUM] Uso extensivo de `shell`
   Evidencia: Multiples archivos (`network_internal`, `nvidia_cuda`, `slurm_validate`, `validate`, `cluster_routing`).
   Accion: Reducir shell a casos con pipes reales; preferir modulos/command.
8. [MEDIUM] `ignore_errors: true` en kernel headers
   Evidencia: `roles/nvidia_cuda/tasks/main.yml` usa best effort para headers.
   Accion: Sustituir por `failed_when` controlado y fallback documentado.
9. [MEDIUM] `base.yml` usa modulos no FQCN
   Evidencia: `base.yml` usa `dnf` sin `ansible.builtin.*`.
   Accion: Estandarizar FQCN en playbook base.
10. [MEDIUM] Archivo legado de slurm.conf potencialmente obsoleto
   Evidencia: `roles/slurm_install/files/slurm.conf` convive con `templates/slurm.conf.j2` sin referencia activa clara.
   Accion: Archivar o documentar explicitamente su estado.
11. [MEDIUM] Debug operativo persistente
   Evidencia: Tareas de `debug` en varios roles (ej. firewall/network/slurm_validate).
   Accion: Mantener solo debug util en validacion; retirar ruido en provisioning.
12. [MEDIUM] List-task de `base.yml` falla en entorno auditado
   Evidencia: `ansible-playbook --list-tasks base.yml` retorna excepcion de permisos/plugin.
   Accion: Corregir entorno de control o pin de colecciones para auditorias CI.
13. [MEDIUM] Limpieza agresiva de conexiones NM
   Evidencia: `roles/network_internal/tasks/main.yml` borra conexiones no permitidas por filtros regex/interfaz.
   Accion: Añadir modo dry-run y evidencia previa antes de aplicar.
14. [MEDIUM] Dependencia de nombres de grupos inventario en firewall
   Evidencia: `roles/firewall/tasks/main.yml` usa combinacion `workers_r` + `workers`.
   Accion: Unificar criterio de grupos para evitar reglas duplicadas.
15. [MEDIUM] Riesgo de drift por tasks con `changed_when: true`
   Evidencia: Varias tasks marcan cambio forzado (reboot markers / update-grub / dracut).
   Accion: Documentar claramente cuando el cambio forzado es deseado.
16. [MEDIUM] Validacion Slurm pesada en mismo role
   Evidencia: `roles/slurm_validate/tasks/main.yml` mezcla checks basicos y smoke largos.
   Accion: Separar tags/flows en validacion rapida vs profunda (sin cambiar logica ahora).
17. [MEDIUM] `validate/tasks/slurm.yml` no se ejecuta por defecto
   Evidencia: Include en `roles/validate/tasks/main.yml` esta comentado.
   Accion: Decidir estrategia: habilitar por tag explicita o documentar como opcional.
18. [LOW] Host key checking deshabilitado
   Evidencia: `ansible.cfg`: `host_key_checking = False`.
   Accion: Revisar habilitacion en entornos sensibles.
19. [LOW] Artifacts locales en repo
   Evidencia: `.cache/slurm-rpms` y `.DS_Store`.
   Accion: Limpiar artifacts y reforzar `.gitignore`.
20. [LOW] Legacy tree extensa
   Evidencia: `archivo_no_en_uso/` contiene playbooks/scripts/artifacts historicos.
   Accion: Conservar en archivo, no mezclar con flujo activo.

## Zonas de alto riesgo (no tocar sin paquete dedicado)

- Red interna y ruteo: `roles/network_internal/*`, `roles/cluster_routing/*`.
- SSH y acceso: `roles/users_ssh/*`, `inventario.ini` (credenciales).
- Kernel/driver GPU: `roles/nvidia_cuda/*`.
- Firewall: `roles/firewall/*`.
- NFS: `roles/nfs_hpc/*`.
- SlurmDBD/MariaDB accounting: `roles/slurm_db_prep/*`, `roles/slurm_controller/*`, `group_vars/hpc_master.yml`.
- Slurm control/compute config: `roles/slurm_install/*`, `roles/slurm_controller/*`, `roles/slurm_compute/*`.
- Autenticacion Munge: `roles/munge/*`.

## Metodologia

- Analisis estatico de YAML y estructura de roles/playbooks.
- Cruce con `site.yml --list-tasks` (base.yml con fallo de entorno auditado).
- No se realizaron cambios de logica ni ejecuciones sobre infraestructura.
