# Modelo de automatización e infraestructura como código (hechos del repo)

## 0) Ubicación y estructura base

- **Ruta del repositorio:** `/Users/juanma/Projects/HPC Repo`
- **Ubicación exacta de entrypoint principal:** `/Users/juanma/Projects/HPC Repo/site.yml`

Árbol de alto nivel (1-2 niveles, resumido):

```text
.
├── site.yml
├── cleanup_slurm_gpu.yml
├── ansible.cfg
├── inventario.ini
├── requirements.yml
├── group_vars/
│   ├── all/
│   └── hpc_master.yml
├── host_vars/
│   ├── master.yml
│   ├── worker1.yml
│   └── worker2.yml
├── roles/
│   ├── common/
│   ├── users_ssh/
│   ├── network_internal/
│   ├── cluster_routing/
│   ├── firewall/
│   ├── nfs_hpc/
│   ├── nvidia_cuda/
│   ├── mariadb_server/
│   ├── munge/
│   ├── slurm_*/
│   ├── llm_env/
│   └── validate/
├── docs/
└── Manual_ZINE_2026/
```

Fuentes: `site.yml`, `cleanup_slurm_gpu.yml`, `ansible.cfg`, `inventario.ini`, `group_vars/*`, `host_vars/*`, `roles/*`, `docs/*`.

---

## 1) Entry point y orquestación principal

### 1.1 Entry point único de orquestación

Hecho verificable:
- `site.yml` es el playbook de orquestación principal del clúster en 15 etapas.
- En la raíz solo hay 2 playbooks con `hosts:`: `site.yml` y `cleanup_slurm_gpu.yml`.

Evidencia:
- `site.yml` (15 plays, nombres de etapa en líneas 11, 25, 40, ... 206).
- `README.md` declara “entrypoint único: `site.yml`”.
- `cleanup_slurm_gpu.yml` existe como playbook auxiliar de limpieza.

### 1.2 Estructura real de `site.yml`

`site.yml` usa una secuencia explícita de 15 plays con:
- `gather_facts: false` en cada play.
- `pre_tasks` con `ansible.builtin.setup` para recolectar facts por etapa.
- Roles ordenados por fase operativa.

Resumen por etapa (hosts → roles):
1. `all` → `common`, `users_ssh`  
2. `all` → `network_internal`, `cluster_routing`, `firewall`  
3. `all` → `nvidia_cuda`  
4. `hpc_master` → `nfs_hpc` (server)  
5. `all:!hpc_master` → `nfs_hpc` (clientes)  
6. `hpc_master` → `mariadb_server`  
7. `hpc_master` → `slurm_db_prep`  
8. `slurm_all` → `slurm_identities`  
9. `slurm_all` → `munge`  
10. `slurm_all` → `slurm_facts`  
11. `hpc_master` → `slurm_rpm_build`, `slurm_install`, `slurm_controller`  
12. `slurm_compute` → `slurm_install`, `slurm_compute`  
13. `all` → `llm_env`  
14. `all` → `validate`  
15. `hpc_master` → `slurm_validate`

Fuente: `site.yml`.

### 1.3 Playbooks auxiliares

- `cleanup_slurm_gpu.yml`: playbook auxiliar de **limpieza/desaprovisionamiento** (Slurm, Munge, NVIDIA/CUDA y reglas asociadas), con `serial: 1` y tags de seguridad (`cleanup_safety`, etc.).  
  Fuente: `cleanup_slurm_gpu.yml`.

No se encontró otro playbook operativo en raíz con `hosts:` fuera de esos dos.

---

## 2) Capas / fases reales del despliegue

El repositorio sí está organizado por capas/fases operativas explícitas en `site.yml` (“Etapa 1..15”), reforzadas por nombres de roles y tags.

Fases operativas inferidas:

1. **Baseline SO y acceso**  
Roles: `common`, `users_ssh`  
Fuente: `site.yml`, `roles/common/tasks/main.yml`, `roles/users_ssh/tasks/main.yml`.

2. **Red interna y perímetro**  
Roles: `network_internal`, `cluster_routing`, `firewall`  
Fuente: `site.yml`, `roles/network_internal/tasks/main.yml`, `roles/cluster_routing/tasks/main.yml`, `roles/firewall/tasks/main.yml`.

3. **Aceleración GPU/CUDA**  
Rol: `nvidia_cuda` (con `meta: end_host` si no hay GPU).  
Fuente: `site.yml`, `roles/nvidia_cuda/tasks/main.yml`.

4. **Storage compartido NFS**  
Rol: `nfs_hpc` separado en server y clientes por plays distintos.  
Fuente: `site.yml`, `roles/nfs_hpc/tasks/main.yml`.

5. **Base de datos de accounting**  
Roles: `mariadb_server`, `slurm_db_prep`.  
Fuente: `site.yml`, `roles/mariadb_server/tasks/main.yml`, `roles/slurm_db_prep/tasks/main.yml`.

6. **Identidad y autenticación Slurm**  
Roles: `slurm_identities`, `munge`.  
Fuente: `site.yml`, `roles/slurm_identities/tasks/main.yml`, `roles/munge/tasks/main.yml`.

7. **Descubrimiento de recursos para Slurm**  
Rol: `slurm_facts` (CPU/Mem/GPU/GRES por nodo).  
Fuente: `site.yml`, `roles/slurm_facts/tasks/main.yml`.

8. **Instalación/configuración Slurm control y cómputo**  
Roles: `slurm_rpm_build`, `slurm_install`, `slurm_controller`, `slurm_compute`.  
Fuente: `site.yml`, `roles/slurm_install/tasks/main.yml`, `roles/slurm_controller/tasks/main.yml`, `roles/slurm_compute/tasks/main.yml`.

9. **Entorno de aplicación LLM**  
Rol: `llm_env`.  
Fuente: `site.yml`, `roles/llm_env/tasks/main.yml`.

10. **Validación operativa**  
Roles: `validate` (salud general) + `slurm_validate` (read-only + smoke jobs CPU/GPU).  
Fuente: `site.yml`, `roles/validate/tasks/*`, `roles/slurm_validate/tasks/main.yml`.

---

## 3) Estrategia de tags por fases

### 3.1 Tags relevantes detectadas

Tags únicas encontradas en `site.yml`, `roles/*` y `cleanup_slurm_gpu.yml`:

`common`, `ssh`, `network`, `network_internal`, `routing`, `sysctl`, `nmcli`, `firewall`, `slurm_firewall`, `cuda`, `nfs`, `nfs_server`, `nfs_client`, `nfs_permissions`, `nfs_firewall`, `del_nfs`, `mariadb`, `slurmdb`, `munge`, `identities`, `slurm`, `slurm_build`, `slurm_install`, `slurm_config`, `slurm_facts`, `slurm_gres`, `slurm_env`, `slurm_rpm_build`, `slurmctld`, `slurmd`, `slurmdbd`, `slurmdbd_hygiene`, `llm`, `validate`, `validate_ssh`, `validate_cuda`, `validate_slurm`, `validate_firewall`, `slurm_validate`, `slurm_validate_smoke`, `verify`, `debug`, `debug_cuda`, `debug_firewall`, `debug_validate`, y en limpieza: `cleanup`, `cleanup_safety`, `cleanup_services`, `cleanup_packages`, `cleanup_files`, `cleanup_firewall`, `cleanup_verify`.

Fuentes: `site.yml`, `roles/*/tasks/*.yml`, `cleanup_slurm_gpu.yml`.

### 3.2 Intención operativa de tags

- **Instalación/bootstrapping:** `common`, `ssh`, `network*`, `routing`, `firewall`, `cuda`, `nfs*`, `mariadb`, `munge`, `identities`, `slurm*`, `llm`.
- **Configuración declarativa:** `slurm_config`, `slurm_env`, `slurm_gres`, `slurmdbd_hygiene`, `nfs_permissions`.
- **Validación:** `validate*`, `verify`, `slurm_validate`, `slurm_validate_smoke`.
- **Depuración/observabilidad:** `debug*`.
- **Limpieza/desinstalación:** `del_nfs` (subconjunto del rol NFS) y playbook auxiliar con `cleanup*`.

### 3.3 Ejemplos típicos de ejecución (basados en tags reales)

```bash
ansible-playbook -i inventario.ini site.yml --tags common,ssh --limit worker2 --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags network,routing,firewall --limit worker2 --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags slurm,slurm_install,slurm_config --limit hpc_master --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags validate,validate_slurm --skip-tags debug --ask-vault-pass
ansible-playbook -i inventario.ini site.yml --tags slurm_validate_smoke --ask-vault-pass
ansible-playbook -i inventario.ini cleanup_slurm_gpu.yml --tags cleanup,cleanup_verify --limit worker2 --ask-vault-pass
```

---

## 4) Jerarquía y precedencia de variables aplicada

### 4.1 Dónde viven variables críticas

- **Globales de clúster:** `group_vars/all/vars.yml`.
- **Overrides de grupo master:** `group_vars/hpc_master.yml`.
- **Secretos cifrados:** `group_vars/all/vault.yml`.
- **Overrides por host:** `host_vars/master.yml`, `host_vars/worker1.yml`, `host_vars/worker2.yml` (actualmente mayormente comentados).
- **Defaults por rol:** `roles/*/defaults/main.yml`.
- **`roles/*/vars`:** no se encontraron archivos `vars/main.yml` en roles.

Fuentes: `group_vars/*`, `host_vars/*`, `roles/*/defaults/main.yml`.

### 4.2 Variables núcleo por dominio (sin exponer secretos)

- **Red/interfaces:** `network_internal_links`, `network_internal_keep_if`, `hpc_internal_supernet`, `hpc_internal_subnets`, `hpc_router_internal_ifaces`.  
  Fuentes: `group_vars/all/vars.yml`, `group_vars/hpc_master.yml`, `roles/network_internal/defaults/main.yml`.
- **Usuarios/SSH:** `ssh_port`, `ssh_permit_root_login`, `ssh_password_authentication`, `ssh_pubkey_authentication`, `ssh_allow_groups`.  
  Fuentes: `group_vars/all/vars.yml`, `roles/users_ssh/defaults/main.yml`.
- **NFS:** `nfs_export_path`, `nfs_client_mountpoint`, `nfs_server_ip`, `nfs_hpc_*`.  
  Fuentes: `group_vars/all/vars.yml`, `group_vars/hpc_master.yml`, `roles/nfs_hpc/defaults/main.yml`.
- **Slurm (particiones/nodos/GRES):** `slurm_partitions`, `slurm_control_machine`, `slurm_node_gres`, `slurm_*cpu/mem*`, `slurm_srun_port_range`.  
  Fuentes: `group_vars/all/vars.yml`, `roles/slurm_facts/tasks/main.yml`, `roles/slurm_install/templates/slurm.conf.j2`.
- **DB / SlurmDBD:** `slurmdb_mysql_db`, `slurmdb_mysql_user`, `slurmdb_mysql_password`, `slurmdbd_*`.  
  Fuentes: `group_vars/hpc_master.yml`, `roles/slurm_db_prep/tasks/main.yml`, `roles/slurm_controller/templates/slurmdbd.conf.j2`.
- **GPU/CUDA:** `nvidia_driver_stream`, `nvidia_cuda_reboot`, `nvidia_cuda_validate`, `nvidia_cuda_*`.  
  Fuentes: `roles/nvidia_cuda/defaults/main.yml`, `roles/nvidia_cuda/tasks/main.yml`.

### 4.3 Modelo real de precedencia observado

Aplicación práctica en este repo:
1. Defaults de rol (`roles/<rol>/defaults/main.yml`) como base.
2. `group_vars/all/vars.yml` para baseline global.
3. `group_vars/<grupo>.yml` (ej. `hpc_master.yml`) sobreescribe global.
4. `host_vars/<host>.yml` sobreescribe grupo/global.
5. Variables de inventario por grupo/host (ej. `inventario.ini` en `[workers_u:vars]`).

Evidencia explícita en comentario del repo: `group_vars/all/vars.yml` indica que `host_vars` sobreescribe `group_vars/*` y `group_vars/<grupo>` sobreescribe `group_vars/all`.

---

## 5) Vault (uso real)

### 5.1 Archivos cifrados detectados

- `group_vars/all/vault.yml` está cifrado (`$ANSIBLE_VAULT;1.1;AES256`).

### 5.2 Tipo de secretos guardados (inferido por referencias)

No se puede leer contenido cifrado sin contraseña.  
Por referencias en código/docs, se usan al menos:
- `vault_ansible_become_password_workers_u`
- `vault_slurmdb_mysql_password`

Consumo real:
- `inventario.ini` usa `ansible_become_password: "{{ vault_ansible_become_password_workers_u }}"`.
- `group_vars/hpc_master.yml` usa `slurmdb_mysql_password: "{{ vault_slurmdb_mysql_password }}"`.

Fuentes: `group_vars/all/vault.yml`, `inventario.ini`, `group_vars/hpc_master.yml`, `docs/vault.md`.

### 5.3 Flujo operativo para ejecutar con Vault

Documentado en repo:
- Interactivo: `--ask-vault-pass`
- Archivo local: `--vault-password-file ...`

Fuentes: `docs/vault.md`, `README.md`, `docs/07-verificacion-rapida.md`.

### 5.4 Verificación de secretos en texto plano (hallazgos)

Hallazgo:
- Existe `.secrets/wd.txt` con contenido en claro (`sistemashpc`) y el archivo está versionado (`git ls-files .secrets/wd.txt`).
- `.gitignore` no ignora `.secrets/`.

Fuentes: `.secrets/wd.txt`, `.gitignore`.

Nota: no se detectaron contraseñas en claro en `inventario.ini` ni `group_vars/hpc_master.yml` actuales; apuntan a variables vault.

---

## 6) Idempotencia y seguridad operativa (patrones presentes)

### 6.1 Patrones de idempotencia

- Uso extensivo de `state: present/absent/started/enabled` en módulos declarativos.
- Uso de `creates:` para operaciones no idempotentes por defecto (ej. build RPM, generación de clave/artefactos).
- Uso de `changed_when: false` en checks/validaciones (`validate`, `slurm_validate`, múltiples comandos de consulta).
- Uso de `failed_when:` explícito cuando el retorno no estándar es aceptable.

Fuentes: `roles/*/tasks/*.yml` (ej. `slurm_rpm_build`, `munge`, `validate`, `slurm_validate`, `nfs_hpc`).

### 6.2 Guards y control de riesgo

- `assert` temprano para evitar ejecución peligrosa sin topología definida (`network_internal`).
- Gating por contexto/tags: remoción NFS solo si `'del_nfs' in ansible_run_tags`.
- Salida temprana por host sin GPU con `meta: end_host` en `nvidia_cuda`.
- Uso acotado de `ignore_errors: true` en tareas “best effort” de headers kernel.
- `no_log: true` en tareas de DB que manejan password.
- Playbook de limpieza con `serial: 1` y tareas de preservación SSH (`cleanup_preserve_ssh`).

Fuentes: `roles/network_internal/tasks/main.yml`, `roles/nfs_hpc/tasks/main.yml`, `roles/nvidia_cuda/tasks/main.yml`, `roles/slurm_db_prep/tasks/main.yml`, `cleanup_slurm_gpu.yml`.

### 6.3 Reinicios controlados

- Reinicios mediante handlers (`notify`) para `sshd`, `firewalld`, `munge`, `mariadb`, `slurmctld/slurmd/slurmdbd`, `initramfs/reboot`.
- Uso de `meta: flush_handlers` en puntos críticos antes de validaciones o reconfigure.

Fuentes: `roles/*/handlers/main.yml`, `roles/firewall/tasks/main.yml`, `roles/slurm_controller/tasks/main.yml`, `roles/slurm_compute/tasks/main.yml`, `roles/nvidia_cuda/tasks/main.yml`.

---

## 7) Síntesis técnica: “Modelo de automatización”

### 7.1 Qué significa IaC en este proyecto

En este repo, IaC significa que el estado del clúster HPC se define declarativamente en:
- playbook principal por etapas (`site.yml`),
- roles especializados por dominio (`roles/*`),
- variables jerárquicas (`group_vars`, `host_vars`, `defaults`),
- plantillas de configuración (`slurm.conf.j2`, `gres.conf.j2`, `slurmdbd.conf.j2`, `exports.j2`).

El resultado operativo se reconstruye ejecutando Ansible sobre inventario, sin depender de cambios manuales no versionados.

### 7.2 Cómo se controla el cambio

Control del cambio combinado:
- **Fases**: 15 etapas con orden explícito (base → red → GPU → NFS → DB → Slurm → LLM → validación).
- **Tags**: ejecución parcial por dominio (`--tags`) y filtrado de ruido/debug (`--skip-tags debug*`).
- **Variables**: sobreescritura por alcance (all → grupo → host).
- **Vault**: secretos fuera de archivos funcionales en claro, consumidos por referencia.

### 7.3 Cómo se mantiene consistencia entre nodos

- Recolección de facts por etapa (`pre_tasks setup`) para decisiones consistentes.
- Configuración de red interna y `/etc/hosts` generada desde mapa declarativo `network_internal_links`.
- Slurm unificado por plantillas y facts por nodo (`slurm_facts` + `slurm_install`).
- Distribución centralizada de artefactos (RPMs Slurm desde master a workers con `delegate_to` y `run_once`).

### 7.4 Cómo se reduce riesgo operativo

- Validaciones separadas (`validate`, `slurm_validate`) con patrón read-only (`changed_when: false`).
- Guards explícitos (`assert`, `failed_when`, `meta end_host`, tags de remoción).
- Reinicios diferidos por handlers y aplicados en momentos controlados (`flush_handlers`).
- Limpieza total aislada en playbook auxiliar con `serial: 1` y preservación de SSH.
- Runbooks/documentación operativa para ejecución canary/limitada (`README.md`, `docs/07-verificacion-rapida.md`).

---

## Anexo breve de evidencia (comandos usados en esta auditoría)

Comandos de verificación (solo lectura) usados para sustentar estos hechos:

- `nl -ba site.yml`
- `rg -l -U "^- name:.*\n\s+hosts:" *.yml`
- `nl -ba inventario.ini`
- `find group_vars host_vars -type f ...`
- `find roles -path '*/defaults/main.yml' ...`
- `rg -n "tags:|changed_when:|creates:|failed_when:|assert:|notify:" ...`
- `nl -ba docs/vault.md`
- `rg --hidden -n "sistemashpc"`
- `git ls-files .secrets/wd.txt`

