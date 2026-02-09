# NFS LLM

## Ejecutar

```bash
ansible-playbook -i inventario.ini playbooks/llm-nfs.yml
```

## Verificar

Master:

```bash
df -hT | grep /srv/nfs
exportfs -v
ls -la /srv/nfs
```

Worker:

```bash
mount | grep /mnt/llm
touch /mnt/llm/_ok
```

## Deshabilitar NFS auxiliar

```bash
ansible-playbook -i inventario.ini playbooks/nfs-aux-disable.yml --tags nfs_auxiliar
```

Nota: el NFS LLM limpia TODO el contenido dentro de `/srv/nfs`; solo usar si `/srv/nfs` debe estar vacío.

Nota: el rol `nfs_hpc` queda opt-in y solo corre si se invoca con `--tags nfs_auxiliar` en `site.yml`.
