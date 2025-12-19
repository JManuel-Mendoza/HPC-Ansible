ansible -i inventario.ini hpc_master:workers -b -m command -a "lsblk -f | egrep 'sda1|sda2'" --ask-become-pass
ansible -i inventario.ini hpc_master:workers -b -m command -a "df -h | egrep '/data|/scratch'" --ask-become-pass
ansible -i inventario.ini hpc_master:workers -b -m command -a "grep -E ' /data | /scratch ' /etc/fstab" --ask-become-pass
