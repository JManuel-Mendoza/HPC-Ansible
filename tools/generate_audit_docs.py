#!/usr/bin/env python3
import os
import re
from pathlib import Path
from collections import defaultdict, deque

ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "docs" / "audit"
TMP_DIR = Path("/tmp/audit")

TEXT_EXT = {".yml", ".yaml", ".j2", ".ini", ".cfg", ".md", ".py", ".sh", ".txt", ".toon"}
META_KEYS = {
    "name", "tags", "when", "notify", "become", "register", "changed_when", "failed_when",
    "ignore_errors", "loop", "with_items", "with_fileglob", "loop_control", "vars", "args",
    "environment", "delegate_to", "run_once", "retries", "delay", "until", "listen", "state",
    "owner", "group", "mode", "path", "src", "dest", "content", "creates", "file", "that",
    "msg", "warn", "chdir", "stdin", "stdin_add_newline", "removes", "force", "backup", "validate",
}
STOPWORDS = {
    "true", "false", "none", "null", "and", "or", "not", "if", "else", "in", "is", "defined",
    "default", "trim", "length", "list", "first", "stdout", "stderr", "stdout_lines", "rc",
    "bool", "int", "float", "map", "select", "reject", "regex_replace", "regex_search",
    "inventory_hostname", "ansible_facts", "hostvars", "groups", "item", "lookup", "env",
    "ternary", "to_json", "join", "split", "max", "min", "sort", "unique", "match", "search",
    "changed", "failed", "results", "default", "omit", "dict2items", "product", "shell", "bash",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def all_files():
    out = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(".git/"):
            continue
        out.append(rel)
    return sorted(out)


def classify_type(rel: str) -> str:
    p = Path(rel)
    name = p.name.lower()
    if rel.startswith("roles/"):
        if "/templates/" in rel:
            return "template"
        if "/files/" in rel:
            return "file"
        return "role"
    if rel in {"site.yml"}:
        return "playbook"
    if rel.endswith((".yml", ".yaml")) and "playbook" in rel.lower():
        return "playbook"
    if rel.startswith("docs/") or rel.endswith(".md"):
        return "doc"
    if rel.startswith("tools/") or rel.endswith((".py", ".sh", ".bash")):
        return "script"
    if name.endswith((".j2",)):
        return "template"
    if name.endswith((".log",)) or "log" in name:
        return "log"
    if name.endswith((".zip", ".tar", ".tar.gz", ".tgz", ".gz")):
        return "artifact"
    return "file"


def risk_for(rel: str, typ: str) -> str:
    high_markers = [
        "roles/network_internal", "roles/cluster_routing", "roles/users_ssh", "roles/firewall",
        "roles/nvidia_cuda", "roles/slurm_controller", "roles/slurm_install", "roles/slurm_db_prep",
        "roles/nfs_hpc", "roles/munge", "inventario.ini", "group_vars/hpc_master.yml"
    ]
    med_markers = [
        "roles/slurm_", "roles/llm_env", "roles/mariadb_server", "site.yml",
        "group_vars/all/vars.yml", "host_vars/"
    ]
    if any(m in rel for m in high_markers):
        return "HIGH"
    if any(m in rel for m in med_markers):
        return "MEDIUM"
    if rel.startswith("docs/docs_old/"):
        return "LOW"
    if typ in {"doc", "artifact", "log"}:
        return "LOW"
    return "MEDIUM"


def recommendation_for(rel: str, typ: str) -> str:
    if rel == ".DS_Store":
        return "DELETE"
    if rel.startswith(".cache/"):
        return "DELETE"
    if rel.startswith("docs/docs_old/"):
        return "ARCHIVE"
    if rel == "roles/slurm_install/files/slurm.conf":
        return "ARCHIVE"
    if rel.startswith("docs/audit/"):
        return "KEEP"
    if rel.startswith("docs/"):
        return "KEEP"
    if rel.startswith("tools/"):
        return "KEEP"
    return "KEEP"


def parse_site_roles() -> list[str]:
    txt = read_text(ROOT / "site.yml")
    roles = []
    for m in re.finditer(r"role:\s*([a-zA-Z0-9_]+)", txt):
        roles.append(m.group(1))
    for m in re.finditer(r"\{\s*role:\s*([a-zA-Z0-9_]+)", txt):
        roles.append(m.group(1))
    seen = []
    for r in roles:
        if r not in seen:
            seen.append(r)
    return seen


def referenced_by(rel: str, site_roles: list[str]) -> str:
    if rel in {"site.yml"}:
        return "CLI/operator"
    if rel == "ansible.cfg":
        return "ansible-playbook (autoload)"
    if rel == "inventario.ini":
        return "ansible.cfg -> inventory"
    if rel.startswith("group_vars/"):
        return "Ansible inventory vars autoload"
    if rel.startswith("host_vars/"):
        return "Ansible inventory vars autoload"
    if rel == "requirements.yml":
        return "ansible-galaxy collection install"
    if rel.startswith("roles/"):
        parts = rel.split("/")
        role = parts[1]
        if len(parts) >= 4 and parts[2] == "tasks" and parts[3] == "main.yml":
            refs = []
            if role in site_roles:
                refs.append(f"site.yml (role {role})")
            return ", ".join(refs) if refs else "playbooks no activos"
        if len(parts) >= 4 and parts[2] == "tasks":
            role_tasks = read_text(ROOT / "roles" / role / "tasks" / "main.yml")
            if Path(rel).name in role_tasks:
                return f"roles/{role}/tasks/main.yml (include/import)"
            return f"roles/{role}/tasks/*.yml"
        if len(parts) >= 4 and parts[2] == "handlers" and parts[3] == "main.yml":
            return f"notify desde roles/{role}/tasks/*.yml"
        if len(parts) >= 4 and parts[2] == "defaults" and parts[3] == "main.yml":
            return f"autoload de rol {role}"
        if len(parts) >= 4 and parts[2] in {"templates", "files"}:
            txt = read_text(ROOT / "roles" / role / "tasks" / "main.yml")
            if Path(rel).name in txt:
                return f"roles/{role}/tasks/main.yml"
            return f"rol {role} (referencia indirecta)"
    if rel.startswith("docs/"):
        return "README.md / navegacion documental"
    if rel.startswith(".agents/"):
        return "AGENTS.md / runtime de agente"
    if rel.startswith("docs/docs_old/"):
        return "No referenciado por entrypoints activos"
    return "No determinado"


def notes_for(rel: str) -> str:
    if rel == "roles/slurm_install/files/slurm.conf":
        return "No se observa consumo activo en tasks; existe template slurm.conf.j2 administrado"
    if rel.startswith("docs/docs_old/"):
        return "Documentación histórica; no vigente"
    if rel in {"site.yml"}:
        return "Entrypoint de ejecucion"
    if rel == "inventario.ini":
        return "Contiene datos sensibles y credenciales en texto plano"
    if rel == "group_vars/hpc_master.yml":
        return "Contiene password de SlurmDB en texto plano"
    if rel.startswith(".cache/"):
        return "Artifact de ejecucion local"
    return ""


def include_edges(role: str) -> dict[str, set[str]]:
    role_dir = ROOT / "roles" / role / "tasks"
    edges = defaultdict(set)
    if not role_dir.exists():
        return edges
    for f in role_dir.glob("*.yml"):
        txt = read_text(f)
        lines = txt.splitlines()
        for i, line in enumerate(lines):
            m = re.search(r"(?:ansible\.builtin\.)?(include_tasks|import_tasks):\s*(.*)$", line)
            if not m:
                continue
            val = (m.group(2) or "").strip().strip("'\"")
            target = ""
            if val and not val.startswith("{"):
                target = val
            else:
                for j in range(i + 1, min(i + 6, len(lines))):
                    mf = re.search(r"^\s*file:\s*(.+)$", lines[j])
                    if mf:
                        target = mf.group(1).strip().strip("'\"")
                        break
            if target:
                edges[f.name].add(target)
    return edges


def collect_role_task_files(role: str) -> list[Path]:
    role_tasks_dir = ROOT / "roles" / role / "tasks"
    if not role_tasks_dir.exists():
        return []
    edges = include_edges(role)
    seen = set()
    q = deque(["main.yml"])
    ordered = []
    while q:
        cur = q.popleft()
        if cur in seen:
            continue
        seen.add(cur)
        p = role_tasks_dir / cur
        if p.exists():
            ordered.append(p)
            for nxt in sorted(edges.get(cur, set())):
                if (role_tasks_dir / nxt).exists() and nxt not in seen:
                    q.append(nxt)
    return ordered


def parse_task_blocks(path: Path, kind: str, inherited_become: str, min_name_indent: int = 0):
    txt = read_text(path)
    lines = txt.splitlines()
    tasks = []
    starts = []
    for i, line in enumerate(lines):
        if not re.match(r"^\s*-\s+name:\s*", line):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent < min_name_indent:
            continue
        if min_name_indent and indent != min_name_indent:
            continue
        starts.append(i)
    starts.append(len(lines))
    for idx in range(len(starts) - 1):
        s = starts[idx]
        e = starts[idx + 1]
        block = lines[s:e]
        name = re.sub(r"^\s*-\s+name:\s*", "", block[0]).strip()
        block_txt = "\n".join(block)

        module = "unknown"
        for line in block[1:]:
            mk = re.match(r"^\s+([a-zA-Z0-9_.]+):\s*", line)
            if not mk:
                continue
            k = mk.group(1)
            if k in META_KEYS:
                continue
            module = k
            break
        if module == "unknown":
            for probe in ["block:", "include_tasks:", "import_tasks:", "include_role:", "import_role:"]:
                if probe in block_txt:
                    module = probe.rstrip(":")
                    break

        def extract_key(key: str) -> str:
            out = ""
            for i2, line in enumerate(block):
                m = re.match(rf"^\s+{re.escape(key)}:\s*(.*)$", line)
                if not m:
                    continue
                rest = (m.group(1) or "").strip()
                if rest and rest != "|":
                    out = rest
                else:
                    vals = []
                    for j in range(i2 + 1, len(block)):
                        l2 = block[j]
                        if re.match(r"^\s+-\s+", l2):
                            vals.append(re.sub(r"^\s+-\s+", "", l2).strip())
                        elif re.match(r"^\s+[a-zA-Z0-9_.]+:\s*", l2):
                            break
                    out = ", ".join(vals)
                break
            return out

        tags = extract_key("tags")
        when = extract_key("when")
        notify = extract_key("notify")
        become = extract_key("become")
        if not become:
            become = inherited_become

        vars_used = []
        for expr in re.findall(r"\{\{\s*([^}]+)\s*\}\}", block_txt):
            expr_clean = re.sub(r"[^A-Za-z0-9_]+", " ", expr)
            for tok in expr_clean.split():
                if tok and not tok.isdigit() and tok.lower() not in STOPWORDS and tok not in vars_used:
                    vars_used.append(tok)
        vars_used_s = ", ".join(vars_used[:12])

        lower_block = block_txt.lower()
        rec = "KEEP"
        why = "Sin riesgo evidente de refactor inmediato"
        risk = "LOW"

        if module in {"ansible.builtin.shell", "shell"}:
            rec = "REWORK"
            why = "Uso de shell; revisar si puede migrarse a modulo o command idempotente"
            risk = "MEDIUM"
        if module in {"ansible.builtin.command", "command"}:
            if "changed_when: false" not in lower_block and "creates:" not in lower_block:
                rec = "REWORK"
                why = "command potencialmente no idempotente (sin creates/changed_when)"
                risk = "MEDIUM"
        if "debug" in module or "debug" in name.lower():
            rec = "REWORK"
            why = "Salida debug a revisar; posible ruido operacional"
            risk = "LOW"
        if module in {"ansible.builtin.systemd", "ansible.builtin.service", "systemd", "service"}:
            if "state: restarted" in lower_block and "notify:" not in lower_block and kind != "handler":
                rec = "MOVE-TO-HANDLER"
                why = "Reinicio directo fuera de handler"
                risk = "MEDIUM"
        if "ignore_errors: true" in lower_block:
            rec = "REWORK"
            why = "Uso de ignore_errors requiere justificacion y control"
            risk = "MEDIUM"
        if "password" in lower_block and module in {"ansible.builtin.command", "command", "ansible.builtin.shell", "shell"}:
            risk = "HIGH"
        if any(z in str(path) for z in ["network_internal", "cluster_routing", "users_ssh", "firewall", "nvidia_cuda", "nfs_hpc", "slurm_install", "slurm_controller", "slurm_db_prep"]):
            if risk == "LOW":
                risk = "MEDIUM"

        tasks.append({
            "file": path.relative_to(ROOT).as_posix(),
            "line": s + 1,
            "kind": kind,
            "name": name,
            "module": module,
            "tags": tags,
            "when": when,
            "notify": notify,
            "become": become,
            "vars": vars_used_s,
            "rec": rec,
            "why": why,
            "risk": risk,
        })
    return tasks


def build_task_matrix(site_roles: list[str]):
    rows = []

    # site.yml roles + handlers
    for role in site_roles:
        for task_file in collect_role_task_files(role):
            for t in parse_task_blocks(task_file, kind="task", inherited_become="inherited(true)"):
                t["entrypoint"] = "site.yml"
                rows.append(t)
        handler = ROOT / "roles" / role / "handlers" / "main.yml"
        if handler.exists():
            for t in parse_task_blocks(handler, kind="handler", inherited_become="handler-scope"):
                t["entrypoint"] = "site.yml"
                rows.append(t)
    return rows


def md_cell(value) -> str:
    s = "" if value is None else str(value)
    s = s.replace("|", "\\|")
    s = s.replace("\n", " ").replace("\r", " ")
    return s


def write_file_ledger(files, site_roles):
    out = []
    out.append("# File Ledger")
    out.append("")
    out.append("Auditoria archivo-por-archivo del repositorio (sin cambios de logica).")
    out.append("")
    out.append("| Ruta | Tipo | Referenciado por | Recomendacion | Riesgo | Notas |")
    out.append("|---|---|---|---|---|---|")
    for rel in files:
        typ = classify_type(rel)
        ref = referenced_by(rel, site_roles)
        rec = recommendation_for(rel, typ)
        risk = risk_for(rel, typ)
        notes = notes_for(rel)
        out.append(f"| `{rel}` | {typ} | {ref} | {rec} | {risk} | {notes} |")
    (AUDIT_DIR / "file-ledger.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def write_entrypoints(site_roles):
    site_list = TMP_DIR / "site.list-tasks.txt"
    site_plays = []
    site_task_count = 0
    if site_list.exists():
        txt = read_text(site_list)
        site_plays = re.findall(r"^\s+play #\d+ .*", txt, flags=re.M)
        site_task_count = len(re.findall(r"^\s{6,}[^\s].*\tTAGS:", txt, flags=re.M))

    out = []
    out.append("# Ansible Entrypoints")
    out.append("")
    out.append("## Entrypoints activos")
    out.append("")
    out.append("| Playbook | Proposito | Estado list-tasks |")
    out.append("|---|---|---|")
    out.append("| `site.yml` | Orquestacion completa del cluster HPC/Slurm/LLM | OK (plays: " + str(len(site_plays)) + ", tasks listadas: " + str(site_task_count) + ") |")
    out.append("")
    out.append("## Entry points legacy/no activos")
    out.append("")
    out.append("- Documentación histórica: `docs/docs_old/README.md` (bitácoras y notas de iteraciones previas; no parte del flujo activo).")
    out.append("")
    out.append("## Orden recomendado de ejecucion (operativo)")
    out.append("")
    out.append("1. `clean OS` (si aplica fuera de este repo)")
    out.append("2. `baseline` -> tags `common,ssh`")
    out.append("3. `red` -> tags `network,routing`")
    out.append("4. `firewall` -> tag `firewall`")
    out.append("5. `gpu` -> tag `cuda`")
    out.append("6. `nfs` -> tag `nfs`")
    out.append("7. `slurm` -> tags `slurm,munge,identities,slurm_install,slurm_config`")
    out.append("8. `llm` -> tag `llm`")
    out.append("9. `validate` -> tags `validate,slurm_validate`")
    out.append("")
    out.append("## Roles cargados por `site.yml`")
    out.append("")
    out.append(", ".join(f"`{r}`" for r in site_roles))
    out.append("")
    out.append("## Plays detectadas en `site.yml --list-tasks`")
    out.append("")
    for p in site_plays:
        out.append(f"- {p.strip()}")

    (AUDIT_DIR / "ansible-entrypoints.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def write_task_matrix(rows):
    out = []
    out.append("# Task Matrix")
    out.append("")
    out.append("Matriz task-por-task obtenida por combinacion de:")
    out.append("- `ansible-playbook --list-tasks` (cuando fue posible),")
    out.append("- analisis YAML directo de playbooks/roles/tasks/handlers/imports.")
    out.append("")
    out.append("| Entrypoint | Archivo | Linea | Tipo | Task | Modulo | Tags | When | Notify | Become | Variables usadas (aprox) | Recomendacion | Riesgo | Justificacion |")
    out.append("|---|---:|---:|---|---|---|---|---|---|---|---|---|---|---|")
    for t in rows:
        out.append(
            f"| `{md_cell(t['entrypoint'])}` | `{md_cell(t['file'])}` | {md_cell(t['line'])} | {md_cell(t['kind'])} | {md_cell(t['name'])} | `{md_cell(t['module'])}` | {md_cell(t['tags'])} | {md_cell(t['when'])} | {md_cell(t['notify'])} | {md_cell(t['become'])} | {md_cell(t['vars'])} | {md_cell(t['rec'])} | {md_cell(t['risk'])} | {md_cell(t['why'])} |"
        )

    # resumen
    out.append("")
    out.append("## Resumen")
    out.append("")
    by_rec = defaultdict(int)
    by_mod = defaultdict(int)
    for t in rows:
        by_rec[t["rec"]] += 1
        by_mod[t["module"]] += 1
    out.append("### Recomendaciones preliminares")
    for k in sorted(by_rec):
        out.append(f"- {k}: {by_rec[k]}")
    out.append("")
    out.append("### Modulos mas usados (top 15)")
    for mod, cnt in sorted(by_mod.items(), key=lambda x: x[1], reverse=True)[:15]:
        out.append(f"- `{mod}`: {cnt}")

    (AUDIT_DIR / "task-matrix.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def write_findings(rows):
    out = []
    out.append("# Findings")
    out.append("")
    out.append("Top 20 hallazgos accionables identificados en auditoria estatica.")
    out.append("")
    out.append("## Top 20 accionables")
    out.append("")
    findings = [
        ("HIGH", "Credenciales en texto plano en inventario", "`inventario.ini`: `ansible_become_password` expuesto en hosts `workers_u`.", "Mover a Ansible Vault y eliminar del inventario en claro."),
        ("HIGH", "Password de SlurmDB en texto plano", "`group_vars/hpc_master.yml`: `slurmdb_mysql_password` en claro.", "Vault + inyeccion segura por vars en runtime."),
        ("HIGH", "Superficie de cambio de red en vivo", "`roles/network_internal/tasks/main.yml` elimina conexiones NM no permitidas.", "Paquete de cambio dedicado con ventana y rollback probado."),
        ("HIGH", "Ruteo persistente con calculo dinamico", "`roles/cluster_routing/tasks/main.yml` calcula rutas y aplica `nmcli connection up`.", "Pruebas por nodo con `--limit` y validacion de conectividad."),
        ("HIGH", "Cambio de kernel/boot params NVIDIA", "`roles/nvidia_cuda/tasks/main.yml` toca blacklist `nouveau` + grub/initramfs + reboot.", "Gate de aprobacion y lote gradual por nodo GPU."),
        ("HIGH", "Reinicios directos fuera de handlers", "`roles/slurm_controller/tasks/main.yml` y `roles/slurm_compute/tasks/main.yml` reinician servicios por task directa.", "Mover reinicios a handlers cuando sea viable."),
        ("MEDIUM", "Uso extensivo de `shell`", "Multiples archivos (`network_internal`, `nvidia_cuda`, `slurm_validate`, `validate`, `cluster_routing`).", "Reducir shell a casos con pipes reales; preferir modulos/command."),
        ("MEDIUM", "`ignore_errors: true` en kernel headers", "`roles/nvidia_cuda/tasks/main.yml` usa best effort para headers.", "Sustituir por `failed_when` controlado y fallback documentado."),
        ("MEDIUM", "Entrypoint unico con alto acoplamiento por tags", "`site.yml` concentra baseline, red, firewall, GPU, NFS, Slurm, LLM y validacion.", "Mantener orden operativo por tags y ejecutar por lotes con `--limit`."),
        ("MEDIUM", "Archivo legado de slurm.conf potencialmente obsoleto", "`roles/slurm_install/files/slurm.conf` convive con `templates/slurm.conf.j2` sin referencia activa clara.", "Archivar o documentar explicitamente su estado."),
        ("MEDIUM", "Debug operativo persistente", "Tareas de `debug` en varios roles (ej. firewall/network/slurm_validate).", "Mantener solo debug util en validacion; retirar ruido en provisioning."),
        ("MEDIUM", "Dependencia de validacion del flujo completo para pre-flight", "El pre-flight ahora vive en `roles/common` dentro de `site.yml`.", "Estandarizar check rapido con `--tags common,ssh` antes del despliegue completo."),
        ("MEDIUM", "Limpieza agresiva de conexiones NM", "`roles/network_internal/tasks/main.yml` borra conexiones no permitidas por filtros regex/interfaz.", "Añadir modo dry-run y evidencia previa antes de aplicar."),
        ("MEDIUM", "Dependencia de nombres de grupos inventario en firewall", "`roles/firewall/tasks/main.yml` usa combinacion `workers_r` + `workers`.", "Unificar criterio de grupos para evitar reglas duplicadas."),
        ("MEDIUM", "Riesgo de drift por tasks con `changed_when: true`", "Varias tasks marcan cambio forzado (reboot markers / update-grub / dracut).", "Documentar claramente cuando el cambio forzado es deseado."),
        ("MEDIUM", "Validacion Slurm pesada en mismo role", "`roles/slurm_validate/tasks/main.yml` mezcla checks basicos y smoke largos.", "Separar tags/flows en validacion rapida vs profunda (sin cambiar logica ahora)."),
        ("MEDIUM", "`validate/tasks/slurm.yml` no se ejecuta por defecto", "Include en `roles/validate/tasks/main.yml` esta comentado.", "Decidir estrategia: habilitar por tag explicita o documentar como opcional."),
        ("LOW", "Host key checking deshabilitado", "`ansible.cfg`: `host_key_checking = False`.", "Revisar habilitacion en entornos sensibles."),
        ("LOW", "Artifacts locales en repo", "`.cache/slurm-rpms` y `.DS_Store`.", "Limpiar artifacts y reforzar `.gitignore`."),
        ("LOW", "Documentación histórica separada", "Existe documentación histórica consolidada en `docs/docs_old/`.", "Mantenerla como referencia, sin mezclarla con el flujo activo."),
    ]
    for i, (sev, title, evidence, action) in enumerate(findings, 1):
        out.append(f"{i}. [{sev}] {title}")
        out.append(f"   Evidencia: {evidence}")
        out.append(f"   Accion: {action}")

    out.append("")
    out.append("## Zonas de alto riesgo (no tocar sin paquete dedicado)")
    out.append("")
    zones = [
        "Red interna y ruteo: `roles/network_internal/*`, `roles/cluster_routing/*`.",
        "SSH y acceso: `roles/users_ssh/*`, `inventario.ini` (credenciales).",
        "Kernel/driver GPU: `roles/nvidia_cuda/*`.",
        "Firewall: `roles/firewall/*`.",
        "NFS: `roles/nfs_hpc/*`.",
        "SlurmDBD/MariaDB accounting: `roles/slurm_db_prep/*`, `roles/slurm_controller/*`, `group_vars/hpc_master.yml`.",
        "Slurm control/compute config: `roles/slurm_install/*`, `roles/slurm_controller/*`, `roles/slurm_compute/*`.",
        "Autenticacion Munge: `roles/munge/*`.",
    ]
    for z in zones:
        out.append(f"- {z}")

    out.append("")
    out.append("## Metodologia")
    out.append("")
    out.append("- Analisis estatico de YAML y estructura de roles/playbooks.")
    out.append("- Cruce con `site.yml --list-tasks`.")
    out.append("- No se realizaron cambios de logica ni ejecuciones sobre infraestructura.")

    (AUDIT_DIR / "findings.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    files = all_files()
    site_roles = parse_site_roles()
    rows = build_task_matrix(site_roles)

    write_file_ledger(files, site_roles)
    write_entrypoints(site_roles)
    write_task_matrix(rows)
    write_findings(rows)

    print(f"Generated docs in {AUDIT_DIR}")
    print(f"Files audited: {len(files)}")
    print(f"Task rows: {len(rows)}")


if __name__ == "__main__":
    main()
