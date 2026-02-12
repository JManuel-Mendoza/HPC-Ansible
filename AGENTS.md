# Guías del repositorio (AGENTS.md)

Este repositorio aprovisiona y opera un clúster HPC (master + workers) con Ansible, incluyendo Slurm, firewall, CUDA/GPUs y validaciones.

## 0) Modo de trabajo con agentes (Codex/LLM)
Por defecto, el agente debe operar en modo **auditoría/verificación**:
- **No edites archivos** ni propongas refactors amplios, a menos que el usuario lo pida explícitamente.
- Primero **inspecciona** el repo, **detecta** inventario/playbooks reales y **ejecuta validaciones**.
- Si encuentras desviaciones, entrega:
  1) diagnóstico,
  2) evidencia (comandos + salida relevante),
  3) propuesta de **diff mínimo** (sin aplicarlo).
- **No hagas commits** salvo instrucción explícita del usuario.

## 1) Estructura del proyecto y organización
- `site.yml` es el playbook principal (baseline, validación).
- `roles/` contiene roles en capas (`common`, `users_ssh`, `firewall`, `nvidia_cuda`, `llm_env`, `llm_project`, `validate`, etc.), cada uno con estructura estándar (`tasks/`, `defaults/`, `vars/`, `handlers/`, `templates/`, `files/` según aplique).
- Variables:
- `group_vars/all.yml` y `group_vars/hpc_master.yml` concentran defaults por alcance.
  - Overrides específicos por host en `host_vars/<hostname>.yml`.
- Inventarios:
  - `inventario.ini` es el inventario por defecto (referenciado por `ansible.cfg`).
  - `inventario_glob.ini` existe para agrupaciones alternas.
- Material ad-hoc y artefactos: `playbooks sueltos/` y `llm-project/` (configs/scripts compartidos).

## 2) Principios operativos (Ansible + HPC)
- Cambios **mínimos y reversibles**: preferir diffs pequeños y bien acotados.
- **Idempotencia** como requisito: ejecutar el mismo playbook dos veces no debe causar cambios inesperados.
- **Separación de responsabilidades**: roles de instalación/configuración (state) separados de roles de validación (read-only).
- **Seguridad**: nunca introducir credenciales en texto plano; usar Vault cuando sea necesario.
- **No romper producción**: evitar cambios de red, firewall, Slurm o almacenamiento salvo solicitud explícita y validación previa.

## 3) Estándares de Ansible (mejores prácticas)
### 3.1 Estilo y calidad
- YAML: indentación 2 espacios, claves en minúscula, variables en `snake_case`.
- Preferir módulos con nombre totalmente calificado: `ansible.builtin.*`, `ansible.posix.*`, etc.
- Tareas con nombres en **español**, concisos y orientados a acción.
- Defaults sobrescribibles en `roles/<rol>/defaults/main.yml`; evitar hardcode en `tasks/`.
- Usar `handlers` para reinicios/reloads (p. ej. `systemd: state=restarted`) y dispararlos con `notify`.

### 3.2 Idempotencia y control de cambios
- Usar `state:` (present/absent/started/enabled) y/o `creates:` cuando aplique.
- Para tareas de validación: usar `changed_when: false`.
- Manejar fallas de forma explícita:
  - `failed_when:` cuando el comando devuelva códigos especiales.
  - `assert:` para condiciones esperadas.
- Evitar `ignore_errors: true` salvo justificación clara y acotada.

### 3.3 Uso correcto de command vs shell
- Preferir `ansible.builtin.command`.
- Usar `ansible.builtin.shell` **solo** si hay pipes/redirecciones/globs o expresiones de shell.
  - Si usas shell: `args: { executable: /bin/bash }` y encabezado `set -euo pipefail`.
  - Evitar `&&` encadenados salvo que sea imprescindible; preferir bloques multi-línea.

### 3.4 Ejecución segura en HPC
- Usar `--limit` para acotar hosts (p. ej. un worker primero, luego el resto).
- Considerar `serial:` para despliegues graduales en workers.
- No reiniciar servicios críticos en todos los nodos simultáneamente.
- Registrar salidas relevantes en PRs/bitácoras (comandos, inventario usado, tags, límites).

## 4) Slurm: operación correcta y buenas prácticas
### 4.1 Principios
- Slurm debe gestionarse como configuración declarativa:
  - Evitar “hotfixes” manuales no registrados en Ansible.
- Separar claramente responsabilidades:
  - Master/controller: `slurmctld`, contabilidad (`slurmdbd` si aplica), herramientas `sacct/squeue/sinfo`.
  - Workers/compute: `slurmd`, GRES/GPU, y dependencias de runtime (CUDA driver/toolkit según diseño).

### 4.2 Orden y seguridad de cambios
- Cambios de configuración: realizar en ventana de mantenimiento cuando sea posible.
- Reinicios/reconfiguraciones:
  - Preferir `scontrol reconfigure` cuando aplique, pero solo si está justificado y probado.
  - Si se requiere restart: hacerlo en orden controlado (controller vs compute según caso) y validando estado.
- Mantener consistencia de `munge` (clave idéntica) y permisos correctos.
- Firewall:
  - No modificar reglas salvo que el cambio esté solicitado y documentado.
  - Mantener explícitos puertos y redes permitidas (reglas ricas y/o servicios según estándar del repo).

### 4.3 GPU/GRES y particiones
- Validar que GRES reporta correctamente:
  - `sinfo -o "%N %G"` y/o `scontrol show node`.
- Particiones:
  - Mantener partición CPU (p. ej. `debug`) y partición GPU (p. ej. `gpu`) con políticas claras.
- Jobs:
  - Para GPU, exigir `--gres=gpu:<n>` y validar `nvidia-smi` dentro de la asignación.
- Directorio de trabajo:
  - Establecer `--chdir`/`#SBATCH --chdir` consistente para evitar fallas por rutas inexistentes.

### 4.4 Validación reproducible (sin tocar configuración)
- Toda validación debe vivir en un rol/tag de “solo lectura” (p. ej. `slurm_validate` o `validate`).
- Validaciones mínimas recomendadas:
  - `sinfo`/`squeue` accesibles.
  - `srun hostname` en partición CPU.
  - `srun nvidia-smi -L` en partición GPU con `--gres=gpu:1`.
  - “smoke jobs” con `sbatch` para CPU y GPU; verificación con `sacct` (estado COMPLETED y exit 0:0).
  - PyTorch CUDA: ejecutar solo si el entorno está presente (modo auto), sin forzar instalaciones.

## 5) Comandos de build, prueba y desarrollo
- Dependencias:
  - `ansible-galaxy collection install -r requirements.yml`
- Ejecución principal:
  - `ansible-playbook -i inventario.ini site.yml`
  - Acotar alcance: `--limit workers` o `--tags cuda,llm`
- Dry-run (idempotencia previa):
  - `ansible-playbook -i inventario.ini site.yml --check --diff`
- Syntax-check:
  - `ansible-playbook -i inventario.ini site.yml --syntax-check`
- Sanidad de inventario:
  - `ansible-inventory -i inventario.ini --graph`

Recomendación operativa:
- Antes de ejecutar sobre todo el clúster, probar en:
  - un solo worker (`--limit worker1`) o un grupo reducido.

## 6) Convenciones de tags
- Mantener tags alineados con roles/playbooks: `common`, `ssh`, `firewall`, `cuda`, `llm`, `llm_project`, `validate`.
- Si se añade un rol de validación nuevo (p. ej. `slurm_validate`), incluir tag propio y evitar colisiones con tags existentes.

## 7) Guías de testing (qué reportar)
Antes de proponer cambios o abrir PR:
- Ejecutar `--syntax-check` y `--check --diff` para lo que se tocó.
- Limitar alcance y reportar:
  - inventario utilizado,
  - límites (`--limit`),
  - tags ejecutados,
  - salida relevante de validaciones (CUDA/Slurm según aplique).
- Evitar ruido: incluir solo evidencia útil (no dumps completos sin necesidad).

## 8) Commits y Pull Requests
- No commits por defecto.
- Mensajes cortos, en presente y descriptivos (ej.: `ajustes mínimos de variables del master`).
- En PRs incluir:
  - qué cambió,
  - qué archivos/roles/vars se tocaron,
  - comandos ejecutados (`--check`, `--tags validate`, etc.),
  - alcance/limit usado.

## 9) Seguridad y configuración
- No commitear secretos ni credenciales. Usar Ansible Vault para material sensible.
- Si `ansible.cfg` desactiva host key checking por conveniencia, considerar reactivarlo para entornos sensibles.
- Sanitizar IPs/hostnames en `inventario*.ini` antes de compartir el repo fuera del entorno controlado.

## 10) Regla de oro
Si no puedes demostrar con evidencia (salida de comandos/validaciones) que el cambio es seguro, no lo apliques: propón un diff mínimo y solicita confirmación del usuario.
