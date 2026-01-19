# STATUS

## Grupos y hosts (inventario.ini)
- hpc_master: master (10.195.34.17) [ansible_user=sistemas]
- workers: worker1 (192.168.34.2), worker2 (192.168.34.18)
- workers (comentados): worker3 (192.168.34.34), worker4 (192.168.34.50)

## Grupos y hosts (inventario_glob.ini)
- hpc_master: master (10.195.34.17)
- workers: worker1 (10.195.20.52), worker2 (10.195.34.19), worker3 (10.195.34.38), worker4 (10.195.20.29)

## Decisiones actuales
- NFS export: /export/llm-project (group_vars/hpc_master.yml) clientes 192.168.34.0/24(rw,sync,no_subtree_check)
- NFS mount: master:/export/llm-project -> /mnt/llm-project (group_vars/workers.yml) opts _netdev,nofail,x-systemd.device-timeout=10
- Micromamba: no se encontro ruta definida en este repo.
- Entorno LLM: venv en /opt/llm-env (playbooks sueltos/python env/llm_env*.yml). Nombre de env conda/micromamba no definido.
- Llm-project dentro del share: no hay subruta declarada; se usa el root del share (/export/llm-project en master, /mnt/llm-project en workers).

## Entrypoints recomendados
- Stack base HPC: site.yml (playbook principal; roles common/users_ssh/firewall/nfs/validate).
- Stack LLM: site.yml con --tags llm (role llm_env). Alternativas especificas: playbooks sueltos/python env/llm_env.yml (CUDA 11.8) o playbooks sueltos/python env/llm_env311.yml (Python 3.11 CPU).
