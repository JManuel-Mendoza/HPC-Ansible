# Lint progresivo de Ansible

## Por qué
Este repositorio gestiona infraestructura crítica; la configuración de Ansible debe revisarse con cuidado. `.ansible-lint` contiene una configuración conservadora que sólo ejecuta reglas estándar y omite rutas sensibles para evitar falsos positivos en artefactos gestionados por vault o secretos locales.

## Instalación

Opción recomendada (aislado):

```bash
pipx install ansible-lint
```

Alternativa (pip):

```bash
python3 -m pip install --user ansible-lint
```

Antes de correr `ansible-lint` (o `ansible-playbook`), instala las colecciones declaradas por el repo:

```bash
ansible-galaxy collection install -r requirements.yml
```

`requirements.yml` fija `ansible.posix` en `1.5.4` para mantener compatibilidad con `ansible-core 2.14`.
Si agregas tags nuevos en un play de `site.yml`, actualiza también el `pre_tasks` de `setup` taggeado de ese play (esquema P16).

## Cómo ejecutar

Lint general del repo:

```bash
ansible-lint -c .ansible-lint .
```

Lint de un playbook:

```bash
ansible-lint -c .ansible-lint site.yml
```

Lint de un rol específico:

```bash
ansible-lint -c .ansible-lint roles/firewall
```

Use el mismo archivo de configuración para detectar regresiones de sintaxis y estilo antes de mezclar cambios. Si sólo está validando un rol o playbook, agregue su ruta final (`roles/firewall`, `docs`, etc.) a la orden, manteniendo `-c .ansible-lint`.

## Exclusiones críticas
- `.secrets/`: carpetas de claves y material temporal nunca deben linterse.
- `group_vars/all/vault.yml`: está cifrado; no queremos que ansible-lint consulte datos sensibles.

La configuración ya excluye estas rutas en `exclude_paths`. Si abre nuevos archivos cifrados, añádalos ahí en lugar de replicar limpieza manual.

## Estrategia progresiva
1. Parta del archivo `.ansible-lint` existente: perfil conservador + exclusiones + `skip_list` de reglas ruidosas.
2. Cada sprint, habilite una regla adicional desde [ansible-lint docs] (por ejemplo `task-uses-changed-when`). Ejecute `ansible-lint` localmente con `--diff` para identificar los ajustes necesarios y documente la decisión en el changelog correspondiente.
3. Cuando varias reglas nuevas estén estables, conviértalo en la nueva base del archivo y registre el cambio para la siguiente revisión.

## Interpretación de resultados

- Errores `fqcn`: indican que una tarea usa un módulo sin nombre totalmente calificado. En este repo se normaliza a `ansible.builtin.*` o `ansible.posix.*` cuando aplica.
- Errores de `yaml[...]` y nombres de tasks: se dejan en `skip_list` inicialmente para evitar ruido; se activarán en paquetes posteriores si se decide.

## Nota sobre colecciones
Este repositorio usa colecciones firmadas (ej. `ansible.posix`). No toca colecciones `community.*`; si necesita una de ellas, solicite que se agregue desde `requirements.yml` y que se verifique su mantenimiento antes de incorporarla al lint.

## Nota adicional
Las colecciones `community.*` permanecen fuera del alcance de este repositorio para evitar modificar código no auditado. Cualquier cambio en esas colecciones debe ser aprobado y documentado explícitamente.
